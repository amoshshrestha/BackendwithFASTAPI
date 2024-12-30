from typing import List
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from backend.app.core.hashing import Hash
from backend.app.models.user import User as models_User  # Import User model
from backend.app.schemas.user import ShowUser as Schemas_Show_User
from backend.app.schemas.user import UserBase as Schemas_User  # BaseUser schema that includes common fields

def create(request: Schemas_User, db: Session):
    
    hashed_password = Hash.bcrypt(request.password)

   
    new_user = models_User(
        name=request.name,
        email=request.email,
        password=hashed_password,
        role=request.role,  
        location=request.location  
    )

    try:
        # Add the new user to the session and commit to save in the database
        db.add(new_user)
        db.commit()
        db.refresh(new_user)  # Refresh the instance to get any updated fields

        # Return the created user as a response
        return new_user
    except Exception as e:
        db.rollback()  # Rollback if any exception occurs to avoid incomplete transactions
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error creating user: " + str(e)
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
