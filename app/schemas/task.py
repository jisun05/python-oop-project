from typing import Optional  
from pydantic import BaseModel, ConfigDict 


class TaskCreate(BaseModel):
    title: str


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    done: Optional[bool] = None


class TaskRead(BaseModel):
    id: int
    title: str
    done: bool
    owner_id: int

    model_config = ConfigDict(from_attributes=True)
