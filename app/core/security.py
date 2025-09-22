import os, json, logging
from datetime import datetime, timedelta, timezone
from typing import Optional, Dict
import jwt
from jwt import InvalidTokenError
from passlib.context import CryptContext

log = logging.getLogger("app.security")

ENV = os.getenv("APP_ENV", "dev").lower()

ALGORITHM = os.getenv("JWT_ALG", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("JWT_EXPIRE_MIN", "60"))

ACTIVE_KID = os.getenv("JWT_ACTIVE_KID") 
KEYS: Dict[str, str] = {}

_raw_keys = (os.getenv("JWT_KEYS") or "").strip()
if _raw_keys:
    try:
        KEYS = json.loads(_raw_keys)
        if not isinstance(KEYS, dict) or not all(isinstance(k, str) and isinstance(v, str) for k, v in KEYS.items()):
            raise ValueError("JWT_KEYS must be a JSON object mapping {str: str}")
    except Exception as e:
        log.error("Invalid JWT_KEYS JSON: %s", e)
        KEYS = {}

if ENV in {"prod", "production", "staging", "stage"}:
    if not KEYS:
        raise RuntimeError("In non-dev environments, configure JWT_KEYS with at least one key.")
    if not ACTIVE_KID or ACTIVE_KID not in KEYS:
        raise RuntimeError("ACTIVE_KID must be set and present in JWT_KEYS for non-dev environments.")

if ENV == "dev" and not KEYS:
    KEYS = {"dev": "dev-secret-change-me"}
    if not ACTIVE_KID:
        ACTIVE_KID = "dev"
    log.warning("Using development JWT secret. Set JWT_KEYS/JWT_ACTIVE_KID for non-dev environments.")

if ENV == "dev" and not ACTIVE_KID and KEYS:
    ACTIVE_KID = next(iter(KEYS))

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)

def create_access_token(sub: str, expires_delta: Optional[timedelta] = None) -> str:
    if not ACTIVE_KID or ACTIVE_KID not in KEYS:
        raise RuntimeError("ACTIVE_KID is not configured correctly or not present in KEYS.")
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    payload = {"sub": sub, "exp": expire}
    headers = {"kid": ACTIVE_KID}
    secret = KEYS[ACTIVE_KID]
    return jwt.encode(payload, secret, algorithm=ALGORITHM, headers=headers)

def decode_token(token: str) -> dict:
    try:
        hdr = jwt.get_unverified_header(token)
        kid = hdr.get("kid")
    except InvalidTokenError:
        kid = None

    if ENV in {"prod", "production", "staging", "stage"}:
        if not kid or kid not in KEYS:
            log.warning("Token rejected due to missing/unknown kid (env=%s, kid=%r)", ENV, kid)
            raise jwt.InvalidTokenError("Invalid token")
        return jwt.decode(
            token,
            KEYS[kid],
            algorithms=[ALGORITHM],
            options={"require": ["exp"]},
        )

    if kid and kid in KEYS:
        return jwt.decode(token, KEYS[kid], algorithms=[ALGORITHM], options={"require": ["exp"]})

    last_err = None
    for secret in KEYS.values():
        try:
            return jwt.decode(token, secret, algorithms=[ALGORITHM], options={"require": ["exp"]})
        except Exception as decode_err:
            last_err = decode_err
    raise last_err or jwt.InvalidTokenError("Invalid token")
