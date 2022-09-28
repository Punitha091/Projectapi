from multiprocessing import synchronize
from fastapi import FastAPI,HTTPException,Response,status,APIRouter,Depends
from sqlalchemy.orm import Session
from typing import List, Optional
import schema,models,utils
from . import oauth2
from database import engine, get_db
from sqlalchemy import func

router=APIRouter(

    prefix="/post",
    tags=["posts"]
    
)
@router.post("/user",status_code=status.HTTP_201_CREATED)
def create_user(data:schema.posts,db:Session=Depends(get_db), current_user :int = Depends(oauth2.get_current_user)):
    print(current_user.id)
    print("works")
    new= models.Post(owner_id=current_user.id, **data.dict())
    db.add(new)
    db.commit()
    db.refresh(new)
    return new

@router.get("/",status_code=status.HTTP_201_CREATED)
def gets(db: Session = Depends(get_db), current_user:int = Depends(oauth2.get_current_user),limit:int=10, skip:int=0,search:Optional[str] =""):
    posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    
    result=db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote,models.Vote.post_id== models.Post.id,isouter=True).group_by(models.Post.id).all()
    return result

@router.get("/currentuser")
def currentuser(db: Session = Depends(get_db),user_id: int =Depends(oauth2.get_current_user)):
    posts = db.query(models.Post).filter(models.Post.id == user_id).first()
    print(posts)
    return (posts)

@router.put("/{id}")
def upd( id:int,post: schema.posts, db: Session = Depends(get_db), current_user :int = Depends(oauth2.get_current_user)):
    upds = db.query(models.Post).filter(models.Post.id == id)
    up=upds.first()
    if up.owner_id!= current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"not authorized to perform this action")
    
    upds.update(post.dict(),synchronize_session=False)
    db.commit()
    return upds.first()


@router.delete("/{id}")
def deleted (id: int, db: Session = Depends(get_db),current_user: int =Depends(oauth2.get_current_user)):
    delete = db.query(models.Post).filter(models.Post.id == id)
    dels= delete.first()
    if dels == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"id with {id} doesnt exist")
    if dels.owner_id!= current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"not authorized to perform this action")
    delete.delete(synchronize_session=False)
    db.commit()
    return {"data": delete}



@router.post("/posting")
def posted(post: schema.posts, db: Session = Depends(get_db)):
    print(post.dict())
    new_posts = models.Post(**post.dict())
    db.add(new_posts)
    db.commit()
    db.refresh(new_posts)
    return {"data": new_posts}

