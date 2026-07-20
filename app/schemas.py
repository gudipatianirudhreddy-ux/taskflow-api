from pydantic import BaseModel,EmailStr,constr
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
    

    
    
