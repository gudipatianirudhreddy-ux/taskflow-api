from datetime import timedelta, datetime
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from starlette import status
from .database import SessionLocal
from .models import Users
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt, JWTError
from . import schemas,database

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
router=APIRouter(
    prefix='/auth',
    tags=['auth']
)

bcrypt_context = CryptContext(schemes=['bcrypt_sha256', 'bcrypt'], deprecated='auto')
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/token')

@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.UserPost)
def register(use:schemas.UserCreate, db: Session = Depends(database.get_db)):
    print(use.password)
    print(type(use.password))
    print(len(use.password))
    create=Users(
        username=use.username,
        password=bcrypt_context.hash(use.password),
        email=use.email,
    )
    db.add(create)
    db.commit()
    db.refresh(create)
    return create




