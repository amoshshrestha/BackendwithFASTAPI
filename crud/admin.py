from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from backend.app.core.hashing import Hash
from backend.app.models.user import User as User
from backend.app.models.admin import Admin as models_User
from backend.app.schemas.admin import ShowAdmin as Schemas_Show_User
from backend.app.schemas.admin import AdminBase as Schemas_User
from backend.app.schemas.user import UserBase as S_User

# Admin-specific CRUD operations

def create_admin(request: Schemas_User, db: Session):
     
    

    hashed_password = Hash.bcrypt(request.password)
    new_admin = models_User(
        name=request.name,
        email=request.email,
        password=hashed_password,
        
    )

    try:
        db.add(new_admin)
        db.commit()
        db.refresh(new_admin)
        return new_admin
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error creating admin: " + str(e)
        )


def get_all_users(db: Session):
    # Admins can fetch all users
    return db.query(User).all()


def get_user_by_id(id: int, db: Session):
    # Admins can fetch user by id
    user = db.query(User).filter(User.id == id).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {id} not found"
        )
    return user


def update_user(id: int, request: S_User, db: Session):
    # Admin can update any user
    user = db.query(User).filter(User.id == id).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {id} not found"
        )

    user.name = request.name
    user.email = request.email
    user.role = request.role
    user.location = request.location
    user.password = Hash.bcrypt(request.password)  # Optionally hash the password again

    try:
        db.commit()
        db.refresh(user)
        return user
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error updating user: " + str(e)
        )


def delete_user(id: int, db: Session):
    # Admin can delete any user
    user = db.query(models_User).filter(models_User.id == id).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {id} not found"
        )

    try:
        db.delete(user)
        db.commit()
        return {"detail": "User deleted successfully"}
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error deleting user: " + str(e)
        )
