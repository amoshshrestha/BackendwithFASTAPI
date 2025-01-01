# from typing import List
# from fastapi import HTTPException, status
# from geoalchemy2 import WKTElement
# from sqlalchemy.orm import Session
# from geoalchemy2.shape import from_shape
# from shapely.geometry import Point
# from geoalchemy2.shape import to_shape



from backend.app.core.hashing import Hash
# from backend.app.models.user import User as models_User  # Import User model
from backend.app.schemas.user import ShowUser as Schemas_Show_User
from backend.app.schemas.user import UserBase as Schemas_User  # BaseUser schema that includes common fields

# def serialize_location(location):
#     if location:
#         try:
#             point = to_shape(location)
#             return {"coordinates": [point.x, point.y]}
#         except Exception as e:
#             raise HTTPException(status_code=500, detail=f"Error serializing location: {e}")
#     return {"coordinates": []}
# def create(request: Schemas_User, db: Session):
    
    
#     hashed_password = Hash.bcrypt(request.password)
#     location = None
    
#     if request.location:
#         coordinates = request.location.coordinates
#         location = WKTElement(f"POINT({coordinates[0]} {coordinates[1]})", srid=4326)

#     new_user = models_User(
#         name=request.name,
#         email=request.email,
#         password=hashed_password,
#         role=request.role,  
#         location=location
#     )

#     try:
#         # Add the new user to the session and commit to save in the database
#         db.add(new_user)
#         db.commit()
#         db.refresh(new_user)  # Refresh the instance to get any updated fields
#         location_coordinates = serialize_location(new_user.location)
#         if new_user.location:
#             location_coordinates = db.scalar(new_user.location.ST_AsText())
#         # Return the created user as a response
#         return {
#                 "id": new_user.id,  # Ensure this is included
#                 "name": new_user.name,
#                 "email": new_user.email,
#                 "password": new_user.password,
#                 "role": new_user.role,
#                 "location": location_coordinates,
#             }
#     except Exception as e:
#         db.rollback()  # Rollback if any exception occurs to avoid incomplete transactions
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             detail="Error creating user: " + str(e)
#         )


# def read(id: int, db: Session):
#     user = db.query(models_User).filter(models_User.id == id).first()
#     if not user:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail=f"User with the id {id} is not available",
#         )
#     return user


# def read_all(db: Session) -> List[Schemas_Show_User]:
#     users = db.query(models_User).all()
#     if not users:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail=f"No users currently!!",
#         )
#     return users
from typing import List
from geoalchemy2 import WKTElement
from geoalchemy2.shape import to_shape
from shapely.geometry import Point
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from backend.app.models.user import User as models_User
from backend.app.schemas.user import UserBase, ShowUser

from geopy.geocoders import Nominatim
def geocode_address(address: str):
    try:
        geolocator = Nominatim(user_agent="myGeocoder")
        location = geolocator.geocode(address)
        if not location:
            raise HTTPException(status_code=400, detail="Address not found")
        return [location.longitude, location.latitude]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error during geocoding: {e}")
def serialize_location(location):
    if location:
        try:
            point = to_shape(location)
            return {"coordinates": [point.x, point.y]}
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error serializing location: {e}",
            )
    return None

def create(request: UserBase, db: Session) -> ShowUser:
    try:
        # Hash the password
        hashed_password = Hash.bcrypt(request.password)

        # Handle location if provided
        location = None
        # if request.location:
        #     coordinates = request.location.coordinates
        #     location = WKTElement(f"POINT({coordinates[0]} {coordinates[1]})", srid=4326)
        if request.location:
            if request.location.coordinates:
                coordinates = request.location.coordinates
            elif request.location.address:
                coordinates = geocode_address(request.location.address)
            else:
                coordinates = None

            if coordinates:
                location = WKTElement(f"POINT({coordinates[0]} {coordinates[1]})", srid=4326)

        # Create the user instance
        new_user = models_User(
            name=request.name,
            email=request.email,
            password=hashed_password,
            role=request.role,
            location=location,
        )

        db.add(new_user)
        db.commit()
        db.refresh(new_user)

    
        return ShowUser(
            id=new_user.id,
            name=new_user.name,
            email=new_user.email,
            role=new_user.role,
            location=serialize_location(new_user.location),
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error creating user: {e}",
        )
def read(id: int, db: Session):
    user = db.query(models_User).filter(models_User.id == id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with the id {id} is not available",
        )
    return user


def read_all(db: Session) -> List[Schemas_Show_User]:
    users = db.query(models_User).all()
    if not users:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No users currently!!",
        )
    return users
# def get_user_by_id(id: int, db: Session) -> ShowUser:
#     user = db.query(models_User).filter(models_User.id == id).first()
#     if not user:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail=f"User with ID {id} not found.",
#         )
#     return ShowUser(
#         id=user.id,
#         name=user.name,
#         email=user.email,
#         role=user.role,
#         location=serialize_location(user.location),
#     )

# def get_all_users(db: Session) -> List[ShowUser]:
#     users = db.query(models_User).all()
#     if not users:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail="No users found.",
#         )
#     return [
#         ShowUser(
#             id=user.id,
#             name=user.name,
#             email=user.email,
#             role=user.role,
#             location=serialize_location(user.location),
#         )
#         for user in users
#     ]
