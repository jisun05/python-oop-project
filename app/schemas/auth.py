from pydantic import BaseModel


class Token(BaseModel):
    access_token: str 
    token_type: str = "bearer" 

class Login(BaseModel):
    email: str     
    password: str
