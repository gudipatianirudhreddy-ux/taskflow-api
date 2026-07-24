from datetime import timedelta, datetime
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException,Request
from pydantic import BaseModel
from sqlalchemy.orm import Session
from starlette import status
from .database import SessionLocal
from .models import Users
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt, JWTError
from . import schemas,database,models
from app.Oauth import oauth
import os
import asyncio
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
router=APIRouter(
    prefix='/auth',
    tags=['auth']
)

# oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/google')
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="/auth/google/login")


def access_token(username: str, id: int, expires_delta: timedelta):
    encode={"sub": username, "id":id}
    expires=datetime.utcnow()+expires_delta
    encode.update({"exp": expires})
    return jwt.encode(encode, SECRET_KEY,ALGORITHM)

def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload=jwt.decode(token, SECRET_KEY,algorithms=[ALGORITHM])
        username: str=payload.get('sub')
        user_id: int =payload.get('id')
        if username is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate user")
        return {'username': username, 'id':user_id}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate user")
        
 
@router.get("/google/login")
async def  google_login(request: Request):
    redirect_uri=request.url_for("google_callback")
    print("Redirect URI:", redirect_uri)
    return await oauth.google.authorize_redirect(
        request,
        redirect_uri
    )

@router.get("/google/callback")
async def google_callback(requests: Request,db: Session = Depends(database.get_db)):
    token=await oauth.google.authorize_access_token(requests)
    print(token)
    user_info = token["userinfo"]
    user=db.query(models.Users).filter(models.Users.google_id==user_info["sub"]).first()
    if not user:
        user=models.Users(
            google_id=user_info["sub"],
            username=user_info["name"],
            email=user_info["email"]
        )
        db.add(user)
        db.commit()
        db.refresh(user)
    acc_token=access_token(
        username=user.username,
        id=user.id,
        expires_delta=timedelta(minutes=30)
    )
    return {"access_token": acc_token, "token_type":"bearer"}
    
       
    
    
@router.get("/me", response_model=schemas.UserPost)
def get_login(current_user=Depends(get_current_user),db: Session = Depends(database.get_db)):
    users=db.query(models.Users).filter(models.Users.id==current_user["id"]).first()
    if not users:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Not authorized")
    return users
    




