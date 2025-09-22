from uuid import uuid4
import os, time, logging
from contextlib import asynccontextmanager, suppress
from fastapi import FastAPI, Request, Response
from starlette.middleware.base import RequestResponseEndpoint
from starlette.responses import RedirectResponse
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
from starlette.middleware.trustedhost import TrustedHostMiddleware
from sqlalchemy.exc import SQLAlchemyError
from uvicorn.middleware.proxy_headers import ProxyHeadersMiddleware
from app.core.log_config import setup_logging, request_id_context
from app.db import Base, engine
from app.routers import users, tasks, auth


@asynccontextmanager
async def lifespan(_app: FastAPI):
    setup_logging()
    Base.metadata.create_all(bind=engine)
    try:
        yield
    finally:
        with suppress(SQLAlchemyError):
            engine.dispose()


app = FastAPI(title="Task Manager API", version="0.2.0", lifespan=lifespan)

req_logger = logging.getLogger("app.request")

ENV = os.getenv("APP_ENV", "dev").lower()
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "*")
FORWARDED_ALLOW_IPS = os.getenv("FORWARDED_ALLOW_IPS", "*") 

if ENV in {"prod", "production", "staging", "stage"}:
    app.add_middleware(ProxyHeadersMiddleware, trusted_hosts=FORWARDED_ALLOW_IPS)

if ENV in {"prod", "production", "staging", "stage"}:
    app.add_middleware(HTTPSRedirectMiddleware)

if ALLOWED_HOSTS != "*":
    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=[h.strip() for h in ALLOWED_HOSTS.split(",") if h.strip()],
    )

@app.middleware("http")
async def add_request_id_and_log(
    request: Request,
    call_next: RequestResponseEndpoint,
) -> Response:
    rid = request.headers.get("X-Request-ID") or str(uuid4())
    token = request_id_context.set(rid)
    start = time.perf_counter()
    try:
        response = await call_next(request)
        duration_ms = (time.perf_counter() - start) * 1000
        req_logger.info(
            "HTTP %s %s -> %s in %.2fms",
            request.method, request.url.path, response.status_code, duration_ms,
        )
        response.headers["X-Request-ID"] = rid
        return response
    finally:
        request_id_context.reset(token)

@app.get("/", include_in_schema=False)
def root():
    return RedirectResponse(url="/docs")

@app.get("/health")
def health():
    return {"status": "ok"}

app.include_router(users.router)
app.include_router(tasks.router)
app.include_router(auth.router)
