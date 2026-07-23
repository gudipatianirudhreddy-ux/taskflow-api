from fastapi import FastAPI,HTTPException,status,Depends
from .import schemas
from . import database,models
from sqlalchemy.orm import Session
from typing import List
from . import auth
from .routes import posts
app=FastAPI()
app.include_router(auth.router)
app.include_router(posts.router)
@app.get("/")
def root():
    return {"message":"Welcome to taskapi"}
