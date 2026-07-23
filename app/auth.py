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
from . import schemas,database,models

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
router=APIRouter(
    prefix='/auth',
    tags=['auth']
)

bcrypt_context = CryptContext(schemes=['bcrypt_sha256', 'bcrypt'], deprecated='auto')
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/token')

def authenticate_users(username: str,password: str,db: Session ):
    user=db.query(models.Users).filter(models.Users.username==username).first()
    if not user:
        return False
    if not bcrypt_context.verify(password,user.password):
        return False
    return user
def access_token(username: str, id: int, expires_delta: timedelta):
    encode={"sub": username, "id":id}
    expires=datetime.utcnow()+expires_delta
    encode.update({"exp": expires})
    return jwt.encode(encode, SECRET_KEY,ALGORITHM)

def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload=jwt.decode(token, SECRET_KEY,algorithms=ALGORITHM)
        username: str=payload.get('sub')
        user_id: int =payload.get('id')
        if username is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, deatil="Could not validate user")
        return {'username': username, 'id':user_id}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate user")
        

    

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

@router.post("/token",)
def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session = Depends(database.get_db)):
    users=authenticate_users(form_data.username,form_data.password, db)
    if not users:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Could not find the user or invalid user")
    token=access_token(users.username,users.id, timedelta(minutes=20))
    return {"access_token": token, "token_type":'bearer'}


@router.get("/me", response_model=schemas.UserPost)
def get_login(current_user=Depends(get_current_user),db: Session = Depends(database.get_db)):
    users=db.query(models.Users).filter(models.Users.id==current_user["id"]).first()
    if not users:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Not authorized")
    return users
    




