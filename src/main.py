from typing import List
from . import schemas, models
from .security import Hashing
from .database import engine, get_db
from .routers import blog
from sqlalchemy.orm import Session
from fastapi import FastAPI, Depends, status, Response, HTTPException

app = FastAPI()

models.Base.metadata.create_all(engine)

app.include_router(blog.router)
# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()


@app.post("/blog", tags=["blogs"], status_code=status.HTTP_201_CREATED)
def create(request: schemas.Blog, db: Session = Depends(get_db)):
    new_blog = models.Blog(title=request.title, body=request.body, user_id=1)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


@app.put("/blog/{id}", tags=["blogs"], status_code=status.HTTP_202_ACCEPTED)
def update(id: int, request: schemas.Blog, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)

    if not blog.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Blog with the id {id} is not available!",
        )
    else:
        blog.update({"title": request.title, "body": request.body})

    db.commit()
    return {"message": "Updated"}


@app.delete("/blog/{id}", tags=["blogs"])
def destroy(id: int, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)

    if not blog.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Blog with the id {id} is not available!",
        )
    else:
        blog.delete(synchronize_session=False)

    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# @app.get("/blog", tags=["blogs"], response_model=List[schemas.ShowBlog])
# def get_blogs(db: Session = Depends(get_db)):
#     blogs = db.query(models.Blog).all()
#     return blogs


@app.get(
    "/blog/{id}",
    tags=["blogs"],
    status_code=status.HTTP_200_OK,
    response_model=schemas.ShowBlog,
)
def get_blog_by_id(id: int, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()

    if not blog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Blog with the id {id} is not available!",
        )
    return blog


@app.post("/user", tags=["users"], response_model=schemas.ShowUser)
def create_user(request: schemas.User, db: Session = Depends(get_db)):
    new_user = models.User(
        name=request.name,
        email=request.email,
        password=Hashing.get_hash_password(request.password),
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@app.get("/user/{id}", tags=["users"], response_model=schemas.ShowUser)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with the id {id} is not available!",
        )

    return user
