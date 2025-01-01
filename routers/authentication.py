from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from backend.app.core.hashing import Hash
from backend.app.core.oauth2 import get_current_user
from backend.app.core.token import (
    create_access_token,
    create_refresh_token,
    verify_refresh_token,
)
from backend.app.database.database import get_db
from backend.app.models.user import User as models_user
from backend.app.models.admin import Admin as models_admin
from backend.app.schemas.token import Token, TokenData

router = APIRouter(tags=["authentication"])


# @router.post("/login")
# def login(
#     request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
# ):
#     user = db.query(models_user).filter(request.username == models_user.email).first()
#     if not user:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail=f"User not available",
#         )
#     if not Hash.verify(user.password, request.password):
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail=f"Incorrect Password",
#         )
#     access_token = create_access_token(data={"sub": user.email})
#     refresh_token = create_refresh_token(data={"sub": user.email})
#     return {
#         "access_token": access_token,
#         "token_type": "bearer",
#         "refresh_token": refresh_token,
#     }

@router.post("/login")
def login(
    request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    # Check if the email exists in the Admins table
    admin = db.query(models_admin).filter(models_admin.email == request.username).first()

    if admin:
        # Verify admin's password
        if not Hash.verify(admin.password, request.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect password for admin",
            )
        # Generate tokens for admin
        access_token = create_access_token(data={"sub": admin.email, "role": "admin"})
        refresh_token = create_refresh_token(data={"sub": admin.email, "role": "admin"})
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "refresh_token": refresh_token,
        }

    # Check if the email exists in the Users table
    user = db.query(models_user).filter(models_user.email == request.username).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    # Verify user's password
    if not Hash.verify(user.password, request.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect password",
        )

    # Generate tokens for user
    access_token = create_access_token(data={"sub": user.email, "role": "user"})
    refresh_token = create_refresh_token(data={"sub": user.email, "role": "user"})
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "refresh_token": refresh_token,
    }


@router.post("/refresh-token", response_model=Token)
def refresh_access_token(refresh_token: str):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    token_data = verify_refresh_token(refresh_token, credentials_exception)

    if token_data is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired refresh token",
        )

    new_access_token = create_access_token(data={"sub": token_data.email})
    new_refresh_token = create_refresh_token(data={"sub": token_data.email})

    return Token(
        access_token=new_access_token,
        token_type="bearer",
        refresh_token=new_refresh_token,
    )

@router.get("/profile")
def get_profile(current_user: TokenData = Depends(get_current_user)):
    profile = current_user.profile
    return {
        "email": current_user.email,  # Access the email attribute
        "profile": {
            "id": getattr(profile, "id", None),  # Safely access 'id' attribute
            "name": getattr(profile, "name", None),  # Safely access 'name' attribute
            "Location": getattr(profile, "location", None),  # Safely access 'username' attribute
        },
    }

