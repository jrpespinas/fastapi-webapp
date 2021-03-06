from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel

app = FastAPI()


class Blog(BaseModel):
    title: str
    body: str
    published: Optional[bool]


@app.get("/blog")
def index(limit: int = 10, published: bool = True, sort: Optional[str] = None):
    if published:
        return {"data": f"{limit} published blogs from the database"}
    else:
        return {"data": f"{limit} blogs from the db"}


@app.get("/blog/unpublished")
def unpublished():
    return {"data": "all unpublished"}


@app.get("/blog/{id}")
def show(id: int):
    return {"data": id}


@app.get("/blog/{id}/comments")
def comments(id: int, limit=10):
    return {"data": {"1", "2"}}


@app.post("/blog")
def create_blog(request: Blog):
    return {"data": f"Blog created with the title as {request.title}"}
