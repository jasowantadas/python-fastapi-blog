from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# Models


class Blog(BaseModel):
    title: str
    body: str
    published: bool | None = None


# Static routes below

@app.post('/blog')
def create_blog(req: Blog):
    return req


@app.get('/blog')
def index(limit: int | None = None, published: bool | None = None):
    if published:
        return {'data': {'Number of blogs': limit, "published": published}}
    return {'data': {'Number of blogs': limit}}


@app.get('/blog/unpublished')
def unpublished():
    pass


# Dynamic routes below


@app.get('/blog/{id}')
def show(id: int):
    return {'data': id}
