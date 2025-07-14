from typing import Literal
from pydantic import BaseModel

class User(BaseModel):
    id: int
    email: str
    role: Literal["admin", "user"]
