from pydantic import BaseModel, EmailStr, ConfigDict  


class UserCreate(BaseModel):
    email: EmailStr  
    name: str        


class UserRegister(BaseModel):
    email: EmailStr
    name: str
    password: str   


class UserRead(BaseModel):
    id: int
    email: EmailStr
    name: str

    model_config = ConfigDict(from_attributes=True)
