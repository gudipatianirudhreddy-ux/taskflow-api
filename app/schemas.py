from pydantic import BaseModel
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
    

    
    
