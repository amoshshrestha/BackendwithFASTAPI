from pydantic import BaseModel
class AdminBase(BaseModel):
    name: str
    email: str
    password: str
    role: str = "admin"  # Admin role is always "admin"

class ShowAdmin(AdminBase):
    id: int

    class Config:
        orm_mode = True
