from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.app.crud.admin import create_admin, get_all_users, get_user_by_id, update_user, delete_user
from backend.app.database.database import get_db
from backend.app.schemas.admin import AdminBase, ShowAdmin
from backend.app.schemas.user import ShowUser, UserBase

router = APIRouter(prefix="/admin", tags=["Admin"])

# Admin route to create an admin user
@router.post("/create", response_model=ShowAdmin)
def create_new_admin(request: AdminBase, db: Session = Depends(get_db)):
    return create_admin(request, db)

# Admin route to get all users
@router.get("/users", response_model=List[ShowUser])
def get_all_users_route(db: Session = Depends(get_db)):
    return get_all_users(db)

# Admin route to get a user by id
@router.get("/user/{id}", response_model=ShowUser)
def get_user(id: int, db: Session = Depends(get_db)):
    return get_user_by_id(id, db)

# Admin route to update a user by id
@router.put("/user/{id}", response_model=ShowUser)
def update_user_route(id: int, request: UserBase, db: Session = Depends(get_db)):
    return update_user(id, request, db)

# Admin route to delete a user by id
@router.delete("/user/{id}")
def delete_user_route(id: int, db: Session = Depends(get_db)):
    return delete_user(id, db)
