from fastapi import APIRouter, Depends, HTTPException,status
from .. import database,models,schemas
from sqlalchemy.orm import Session
from typing import List
from ..auth import get_current_user

router=APIRouter(
    prefix='/groups',
    tags=['Groups']
)

@router.post('/',status_code=status.HTTP_201_CREATED,response_model=schemas.GroupPost)
def create_group(posts: schemas.Group,db: Session = Depends(database.get_db),current_user= Depends(get_current_user)):
    added=models.Groups(**posts.dict(), owners_id=current_user["id"])
    db.add(added)
    db.commit()
    db.refresh(added)
    return added

@router.get('/',status_code=status.HTTP_200_OK, response_model=List[schemas.GroupPost])
def get_groups(db: Session = Depends(database.get_db),current_user= Depends(get_current_user)):
    getting=db.query(models.Groups).filter(models.Groups.owners_id==current_user["id"]).all()
    if not getting:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not authorized or validated")
    
    return getting

@router.get("/{group_id}",status_code=status.HTTP_200_OK, response_model=schemas.GroupPost)
def getting_post(group_id: int, db: Session = Depends(database.get_db),current_user= Depends(get_current_user)):
    post=db.query(models.Groups).filter(models.Groups.id==group_id, models.Groups.owners_id==current_user["id"]).first()
    if not post:
         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not there or not authorized")
    return post

@router.patch("/{group_id}",status_code=status.HTTP_302_FOUND, response_model=schemas.GroupPost)
def updated_group(group_id: int,posts: schemas.UpdateGroup,db: Session = Depends(database.get_db),current_user= Depends(get_current_user)):
    up=db.query(models.Groups).filter(models.Groups.id==group_id, models.Groups.owners_id==current_user["id"])
    updates=posts.model_dump(exclude_unset=True)
    if not updates:
        raise HTTPException(
              status_code=status.HTTP_400_BAD_REQUEST,
            detail="No fields provided for update"
        )
    if not up.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found or group not found")
    up.update(updates, synchronize_session=False)
    db.commit()
    return up.first()

@router.delete("/{group_id}", status_code=status.HTTP_202_ACCEPTED,response_model=schemas.GroupPost)
def delete(group_id: int, db: Session = Depends(database.get_db),current_user= Depends(get_current_user)):
     deli=db.query(models.Groups).filter(models.Groups.id==group_id, models.Groups.owners_id==current_user["id"])
     if not deli:
          raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid id or id do not exist")
     db.delete(deli)
     db.commit()
     return {"Messsage":"Deleted the group Sucessfully"}

@router.post("/{group_id}/invite", status_code=status.HTTP_201_CREATED,response_model=schemas.GroupInvitationResponse)
def send_invite(group_id: int,db: Session = Depends(database.get_db),current_user= Depends(get_current_user)):
    ans=db.query(models.Groups).filter(models.Groups.id==group_id, models.Groups.owners_id==current_user["id"])
    if not ans:
        raise HTTPException(status=status.HTTP_401_UNAUTHORIZED, detail="Not validated user")
    
    
         
         
    
 
    
    
    
