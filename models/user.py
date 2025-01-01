from sqlalchemy import Column, Integer, String, Enum
from geoalchemy2 import Geography

from backend.app.database.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    role = Column(Enum("normal_user", "service_provider", name="user_roles"))
    location = Column(Geography(geometry_type='POINT', srid=4326), nullable=True)