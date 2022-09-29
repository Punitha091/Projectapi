from multiprocessing import synchronize
from pydantic import BaseModel
from database import engine, get_db
from sqlalchemy.orm import Session
from fastapi import FastAPI, Depends
import models
import schema
from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
import psycopg2
from psycopg2.extras import RealDictCursor
import utils
from router import auth,posts,user , vote



# models.Base.metadata.create_all(bind=engine)


app = FastAPI()

app.include_router(posts.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)


# try:
#     Conn = psycopg2.connect(host='localhost', database='apilearn',
#                             user='Punitha', password='2412', cursor_factory=RealDictCursor)
#     cursor = Conn.cursor()
#     print("Database connection was successful")
# except Exception as error:
#     print("Connecting to database failed")



@app.get('/')
def start():
    return {'msg':'Success'}
'''

class Post(BaseModel):
    title: str
    content: str
    published: bool


def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p


my_posts = [{"title": "post1", "content": "content1", "id": 1}, {"title": "post2",
                                                                 "content": "content2", "id": 2}, {"title": "post3", "content": "content3", "id": 3}]


def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return i


@app.get("/sqlalchemy")
def test_posts(db: Session = Depends(get_db)):
    posts = db.query(models.post).all()
    return {"data": posts}


@app.get("/posts")
def get_posts():
    cursor.execute("""SELECT * FROM learnapi""")
    posts = cursor.fetchall()
    print(posts)
    return {"data": posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    cursor.execute("""INSERT into learnapi(title,content,published) Values (%s,%s,%s) RETURNING * """,
                   (post.title, post.content, post.published))
    new_post = cursor.fetchone()
    Conn.commit()
    return {"data": new_post}


@app.get("/posts/{id}")
def get_posts(id: str):
    cursor.execute("""SELECT * FROM learnapi WHERE id=%s""", str(id))
    post = cursor.fetchone()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} not found")
    return {"data": post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_posts(id: int):
    cursor.execute(
        """ DELETE from learnapi WHERE id=%s RETURNING * """, (str(id)))
    deleted_posts = cursor.fetchone()
    Conn.commit()
    if deleted_posts == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"id{id} doesnt exist")
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    cursor.execute(""" UPDATE learnapi SET title=%s,content=%s,published=%s WHERE id=%s RETURNING *""",
                   (post.title, post.content, post.published, str(id)))
    updated_post = cursor.fetchone()
    Conn.commit()
    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"id with {id} doesn't exist")
    return {"data": updated_post}


@app.get("/")
async def root():
    return {"message": "Hello puvi"}


@app.get("/posts")
def get_posts():
    return {"data": "WElcome"}


@app.post("/createposts")
def create_posts(payload: dict = Body(...)):
    print(payload)
    return {"data": "Welcome post"}


@app.post("/createpost")
def create_posts(payload: dict = Body(...)):
    print(payload)
    return {"data": f"title{payload['title']} content:{payload['content']}"}


@app.post("/createpos")
def create_posts(new: dict = Body(...)):
    print(new)
    return {"data": "new"}


@app.post("/createbody")
def create_posts(payload: dict = Body(...)):
    print(payload)
    return {"data": f"title{payload['title']}content:{payload['content']}"}


@app.post("/createbod")
def create_posts(new_posts: Post):
    print(new_posts)
    return {"data": "new post"}


@app.post("/createbo")
def create_posts(new_posts: Post):
    print(new_posts)
    print(new_posts.dict())
    return {"data": "new post"}


@app.get("/posted")
def get_posts():
    return {"data": my_posts}

# to create ranndom number


@app.post("/poste")
def create_posts(post: Post):
    post_dict = post.dict()
    post_dict['id'] = randrange(0, 100000)
    my_posts.append(post_dict)
    return {"data": post_dict}


@app.get("/posted/{id}")
def get_post(id):
    print(id)
    return {"post_details": f"here is post{id}"}


@app.get("/post/{id}")
def get_posts(id: int):
    post = find_post(id)
    return {"post_details": post}


@app.get("/posts/latest")
def get_latest():
    post = my_posts[len(my_posts)-1]
    return {"detail": post}


@app.get("/post/{id}")
def get_post(id: int, response: Response):
    post = find_post(id)
    if not post:
        response.status_code = status.HTTP_404_NOT_FOUND
    return {"message": f"post with id: {id} was not found"}


@app.get("/posts/{id}")
def get_post(id: int):
    post = find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f" post with id : {id} was not foound")
    return {"post_detail": post}


@app.get("/posts/{id}", status_code=status.HTTP_201_CREATED)
def get_post(id: int):
    post = find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f" post with id : {id} was not foound")
    return {"post_detail": post}


@app.delete("/posts/{id}")
def delete_post(id: int):
    index = find_index_post(id)
    my_posts.pop(index)
    return {"message": " post deleted"}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    index = find_index_post(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not found")
    my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
def update_post(post: Post):
    print(post)
    return {"message": "updated"}


@app.put("/post/{id}")
def update_post(id: int, post: Post):
    index = find_index_post(id)

    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id : {id} doesn't exist")
    post_dict = post.dict()
    post_dict['id'] = id
    my_posts[index] = post_dict
    return {"data": post_dict}


@app.get("/sqlalchemy")
def test_posts(db: Session = Depends(get_db)):
    return {"status": "success"}


'''


@app.post("/posting", status_code=status.HTTP_201_CREATED, response_model=schema.users)
def createposts(data: schema.posts, db: Session = Depends(get_db)):
    new_posts = models.Post(**data.dict())
    db.add(new_posts)
    db.commit()
    db.refresh(new_posts)
    return {"data": new_posts}


@app.get("users/{id}", response_model=schema.users)
def get_user(id: int, db: Session = Depends(get_db)):
    # hashed_password = utils.hash(user.password)
    #    user.password = hashed_password
    user = db.query(models.Post).filter(models.Post.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"id with {id} doesnt exist")
    return user


@app.get("/getall")
def gets(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    print(posts)
    return {"data": posts}


@app.post("/getuser", status_code=status.HTTP_201_CREATED, response_model=schema.userlogin)
def create_user(user: schema.userlogin, db: Session = Depends(get_db)):
    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.post("/postinghere", status_code=status.HTTP_201_CREATED, response_model=schema.posts)
def create_user(user: schema.posts, db: Session = Depends(get_db)):
    new_user = models.Post(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
