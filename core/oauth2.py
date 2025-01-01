from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from backend.app.database.database import get_db
from backend.app.models.user import User
from backend.app.models.admin import Admin
from sqlalchemy.orm import Session

from backend.app.core.token import verify_token
from backend.app.schemas.token import TokenData

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


# def get_current_user(token: str = Depends(oauth2_scheme)):
#     credentials_exception = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Could not validate credentials",
#         headers={"WWW-Authenticate": "Bearer"},
#     )
#     return verify_token(token, credentials_exception)

def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    token_data = verify_token(token, credentials_exception)

    # Query the user or admin from the database
    user = db.query(User).filter(User.email == token_data.email).first()
    if not user:
        admin = db.query(Admin).filter(Admin.email == token_data.email).first()
        if not admin:
            raise credentials_exception
        return TokenData(email=admin.email, profile=admin)  # Return TokenData object

    return TokenData(email=user.email, profile=user)  # Return TokenData object
