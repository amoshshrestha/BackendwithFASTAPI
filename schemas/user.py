# from typing import List
# from pydantic import BaseModel

# class LocationSchema(BaseModel):
#     coordinates: List[float]

# class UserBase(BaseModel):
#     name: str
#     email: str
#     password: str
#     location: LocationSchema | None
#     role: str  # Role attribute, "consumer" or "provider"

# class ConsumerUser(UserBase):
#     pass  # No extra fields, inherits from UserBase

# class ProviderUser(UserBase):
#     service_type: str  # Example extra field for providers, could be a list of services they provide



# class ShowUser(UserBase):
#     id: int

# class ShowConsumer(ShowUser):
#     pass
# class ShowProvider(ShowUser):
#     service_type: str



#     class Config:
#         orm_mode = True


# class UserProfile(BaseModel):
#     id: int
#     name: str = None
#     username: str = None

# class ProfileResponse(BaseModel):
#     email: str
#     role: str
#     profile: UserProfile

from typing import List, Optional
from pydantic import BaseModel, Field

# class LocationSchema(BaseModel):
#     coordinates: List[float] = Field(..., min_items=2, max_items=2, description="Latitude and Longitude as [x, y]")
class LocationSchema(BaseModel):
    coordinates: Optional[List[float]] = Field(
        None, min_items=2, max_items=2, description="Latitude and Longitude as [x, y]"
    )
    address: Optional[str] = Field(
        None, description="Physical address of the user"
    )
class UserBase(BaseModel):
    name: str
    email: str
    password: str
    location: Optional[LocationSchema] = None
    role: str  # "consumer" or "provider"

class ConsumerUser(UserBase):
    pass

class ProviderUser(UserBase):
    service_type: str  # Additional field for providers

class ShowUser(BaseModel):
    id: int
    name: str
    email: str
    role: str
    location: Optional[LocationSchema] = None

    class Config:
        orm_mode = True

class UserProfile(BaseModel):
    id: int
    name: str = None
    username: str = None

class ProfileResponse(BaseModel):
    email: str
    role: str
    profile: UserProfile