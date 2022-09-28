from fastapi import FastAPI,HTTPException,Response,status,APIRouter,Depends
from sqlalchemy.orm import Session
from typing import List
import schema,models,utils
from database import get_db
from . import oauth2

router=APIRouter(
    prefix="/user",
    tags=["posts"]
)

'''
@router.get("/")
def gets(db: Session = Depends(get_db)):
    posts = db.query(models.User).all()
    print(posts)
    return {"data": posts}

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schema.userlogin)
def create_user(user: schema.userlogin, db: Session = Depends(get_db)):
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.post("/posting")
def posted(post: schema.user, db: Session = Depends(get_db)):
    print(post.dict())
    new_posts = models.User(**post.dict())
    db.add(new_posts)
    db.commit()
    db.refresh(new_posts)
    return {"data": new_posts}


'''

@router.post("/")
def create_user(data:schema.userlogin,db:Session=Depends(get_db)):
    new= models.User(**data.dict())
    db.add(new)
    db.commit()
    db.refresh(new)
    return new

@router.post("/post", status_code=status.HTTP_201_CREATED, response_model=schema.userlogin)
def create_user(user: schema.userlogin, db: Session = Depends(get_db)):
    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get("/")
def gets(db: Session = Depends(get_db)):
    posts = db.query(models.User).all()
    print(schema.user)
    return (posts)

@router.get("/{id}")
def getid(id: int, db: Session = Depends(get_db)):
    posts = db.query(models.Post).filter(models.Post.id == id).first()
    print(posts)
    return {"data": posts}


@router.put("/")
def update(post: schema.userlogin, db: Session = Depends(get_db),user_id:int=Depends(oauth2.get_current_user)):
    up = db.query(models.User).filter(models.User.id == user_id.id)
    up.update(post.dict(),synchronize_session=False)
    db.commit()
    return up.first()


@router.delete("/{id}")
def deleted(id: int, db: Session = Depends(get_db)):
    delete = db.query(models.User).filter(models.User.id == id)
    if delete.first == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"id with {id} doesnt exist")
    delete.delete(synchronize_session=False)
    db.commit()
    return {"data": delete}