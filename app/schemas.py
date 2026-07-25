from pydantic import BaseModel,EmailStr,constr
from typing import Optional
from datetime import datetime
from app.models import InvitationStatus
class Tasks(BaseModel):
    title: str
    content: str
    completed: bool=False

class TasksCreate(Tasks):
    pass
class TasksPost(Tasks):
    id: int
    class Config:
        from_attributes=True

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: constr(min_length=8, max_length=72)

class UserPost(BaseModel):
     id: int
     email: EmailStr
     class Config:
         from_attributes=True
class Token(BaseModel):
    access_token: str
    token_type: str
    
class Group(BaseModel):
    name: str
    description: str

class GroupPost(Group):
    id:int 
    class Config:
             from_attributes=True
             
class UpdateGroup(BaseModel):
    name: Optional[str]=None
    description: Optional[str]=None
    
class GroupInvitationBase(BaseModel):
    email: EmailStr

class GroupInvitationCreate(GroupInvitationBase):
    
    expires_at: datetime

class GroupInvitationResponse(GroupInvitationBase):
    id: int
    invited_by: int
    token: str
    status: InvitationStatus
    expires_at: datetime
    created_at: datetime

    class Config:
        from_attributes = True
