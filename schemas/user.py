from pydantic import BaseModel



class UserBase(BaseModel):
    name: str
    email: str
    password: str
    location: str
    role: str  # Role attribute, "consumer" or "provider"

class ConsumerUser(UserBase):
    pass  # No extra fields, inherits from UserBase

class ProviderUser(UserBase):
    service_type: str  # Example extra field for providers, could be a list of services they provide



class ShowUser(UserBase):
    id: int

class ShowConsumer(ShowUser):
    pass
class ShowProvider(ShowUser):
    service_type: str



    class Config:
        orm_mode = True


