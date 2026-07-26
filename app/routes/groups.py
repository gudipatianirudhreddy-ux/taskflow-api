from fastapi import APIRouter, Depends, HTTPException,status
from .. import database,models,schemas
from sqlalchemy.orm import Session
from typing import List
from ..auth import get_current_user
import secrets
from datetime import timedelta, datetime,timezone
from app.services.email_service import send_group_invitation
from app.models import InvitationStatus

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
def send_invite(invite: schemas.GroupInvitationBase,group_id: int,db: Session = Depends(database.get_db),current_user= Depends(get_current_user)):
    ans=db.query(models.Groups).filter(models.Groups.id==group_id).first()
    if not ans:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Group dosen't exists")
    if ans.owners_id!=current_user["id"]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User not validate or nnot loggined")
    user=db.query(models.Users).filter(models.Users.email==invite.email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User does not exists")
    if user.id==current_user["id"]:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="You  cannot invite yourself")
    pending=db.query(models.GroupInvitation).filter( models.GroupInvitation.group_id==group_id, models.GroupInvitation.email==invite.email,models.GroupInvitation.status==InvitationStatus.pending
                                                    ).first()
    if pending:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Invitation already sent")
    modes=(db.query(models.Members).filter(models.Members.group_id==group_id,models.Members.user_id==user.id).first())
    if modes:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User already exists in the group")
    people=db.query(models.Members).filter(models.Members.group_id==group_id).count()
    if people>=3:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Only group of 3 people are only alowed")
    token=secrets.token_urlsafe(32)
    expires_at=datetime.now(timezone.utc) + timedelta(days=7)
    invite_obj=models.GroupInvitation(
         group_id=group_id,
         email=invite.email,
         invited_by=current_user["id"],
         token=token,
        expires_at=expires_at
    )
    db.add(invite_obj)
    db.commit()
    db.refresh(invite_obj)
    accept_url = f"http://localhost:8000/invitations/{invite_obj.token}/accept"
    try:
        inviter=db.query(models.Users).filter(models.Users.id==current_user["id"]).first()
        send_group_invitation(
            to_email=invite.email,
             inviter_email=inviter.email,
              group_name=ans.name,
              accept_url=accept_url
        )
    except Exception as e:
         db.delete(invite_obj)
         db.commit()
         raise  HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail=f"Failed to send invitation: {str(e)}")
     
         
        
    return invite_obj

    
    
    
    
                            
    
    
    
    
         
         
    
 
    
    
    
