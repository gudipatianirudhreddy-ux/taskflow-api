from fastapi import APIRouter, Depends, HTTPException,status
from .. import database,models,schemas
from sqlalchemy.orm import Session
from typing import List
from ..auth import get_current_user
router=APIRouter(
    prefix="/tasks",
    tags=['Posts']
)

@router.get("/",status_code=status.HTTP_200_OK,response_model=List[schemas.TasksPost])
def get_tasks(current_user= Depends(get_current_user),db: Session = Depends(database.get_db)):
    tasks=db.query(models.tasks).filter(models.tasks.users_id==current_user["id"]).all()
    if tasks is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Tasks not there")
    return tasks

@router.post("/",status_code=status.HTTP_200_OK,response_model=schemas.TasksPost)
def post_tasks(posts: schemas.Tasks,db: Session = Depends(database.get_db),current_user= Depends(get_current_user)):
    added=models.tasks(**posts.dict(),
                       users_id=current_user["id"])
    db.add(added)
    db.commit()
    db.refresh(added)
    return added

@router.get("/{id}",status_code=status.HTTP_200_OK,response_model=schemas.TasksPost)
def getting_tasks(id: int, db: Session = Depends(database.get_db),current_user= Depends(get_current_user)):
    ans=db.query(models.tasks).filter(models.tasks.id==id, models.tasks.users_id==current_user["id"]).first()
    if not ans:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid id")
    return ans

@router.delete("/{id}", status_code=status.HTTP_201_CREATED)
def delete_tasks(id: int, db: Session = Depends(database.get_db),current_user= Depends(get_current_user) ):
    deli=db.query(models.tasks).filter(models.tasks.id==id,models.tasks.users_id==current_user["id"]).first()
    if not deli:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid id or id do not exist")
    db.delete(deli)
    db.commit()
    return {"Message":"Deleted successfully"}

@router.put("/{id}",status_code=status.HTTP_200_OK,response_model=schemas.TasksPost)
def update_tasks(id: int,posts: schemas.Tasks,db: Session = Depends(database.get_db),current_user= Depends(get_current_user) ):
    qur=db.query(models.tasks).filter(models.tasks.id==id,models.tasks.users_id==current_user["id"])
    if not qur.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="id do not exists or not found")
    qur.update(posts.dict(), synchronize_session=False)
    db.commit()
    return qur.first()
