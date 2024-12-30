from typing import List

from fastapi import APIRouter, Depends,HTTPException
from sqlalchemy.orm import Session

from backend.app.crud.user import create, read, read_all
from backend.app.database.database import get_db
from backend.app.schemas.user import ShowUser, UserBase

router = APIRouter(prefix="/user", tags=["Users"])


@router.post("/create", response_model=ShowUser)
def create_user(request: UserBase, db: Session = Depends(get_db)):
    try:
        return create(request, db)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/get/{id}", response_model=ShowUser)
def get_user(id: int, db: Session = Depends(get_db)):
    return read(id, db)


@router.get("/get", response_model=List[ShowUser])
def get_user(db: Session = Depends(get_db)):
    return read_all(db)
