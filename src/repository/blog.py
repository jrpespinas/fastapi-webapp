from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from .. import models, schemas

def get_all(db: Session):
    blogs = db.query(models.Blog).all()
    return blogs

def get_blog_by_id(id: int, db: Session):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()

    if not blog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Blog with the id {id} is not available!",
        )
    return blog

def update_blog_by_id(id: int, request, db: Session):
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

def delete_blog_by_id(id: int, db: Session):
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

def create_blog(request, db: Session):
    new_blog = models.Blog(title=request.title, body=request.body, user_id=1)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog