from fastapi import FastAPI, Depends, status, HTTPException
from typing import List
from . import schemas, models, token
from sqlalchemy.orm import Session
from .database import engine, SessionLocal
from passlib.context import CryptContext

app = FastAPI()


models.Base.metadata.create_all(engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post('/blog', status_code=status.HTTP_201_CREATED, tags=['Blogs'])
def create_Blog(req: schemas.Blog, db: Session = Depends(get_db),):
    new_blog = models.Blog(**req.dict(), user_id=1)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


@app.get('/blog', response_model=List[schemas.ShowBlog], tags=['Blogs'])
async def show_all_Blogs(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    print(blogs)
    return blogs


# later will try to include indexing here


@app.get('/blog/{id}', response_model=schemas.ShowBlog, tags=['Blogs'])
def find_Blog(id: int, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if blog:
        return blog
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Blog with id:{id} not found")
    # response.status_code = status.HTTP_404_NOT_FOUND
    # return {"details": f"Blog with id:{id} not found"}


@app.delete('/blog/{id}', tags=['Blogs'])
def Delete_Blog(id, db: Session = Depends(get_db)):
    db.query(models.Blog).filter(models.Blog.id ==
                                 id).delete(synchronize_session=False)
    db.commit()
    return "Done"


@app.put('/blog/{id}', tags=['Blogs'])
def Update_Blog(id: int, req: schemas.Blog, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Blog with id:{id} not found")
    blog.update(req.dict())
    db.commit()
    return "Updated Sucessfully"


# password encription
pwd_cxt = CryptContext(schemes=['bcrypt'], deprecated='auto')


def verify(plainPassword, hashedPassword):
    return pwd_cxt.verify(plainPassword, hashedPassword)


@app.post('/user', response_model=schemas.ShowUser, tags=['Users'])
def create_user(req: schemas.User, db: Session = Depends(get_db)):
    hashedPassword = pwd_cxt.hash(req.password)
    new_user = models.User(name=req.name, email=req.email,
                           password=hashedPassword)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@app.get('/user/{id}', response_model=schemas.ShowUser, tags=['Users'])
def get_user(id, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id:{id} not found")
    return user


@app.post('/login', tags=["Auth"])
def Login(req: schemas.Login, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(
        models.User.email == req.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Invalid creadentials")
    if not verify(req.password, user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Invalid Password")
    # jwt access token
    access_token = token.create_access_token(data={"sub": user.email})
    return {"access_toke": access_token, "token_type": "bearer"}
