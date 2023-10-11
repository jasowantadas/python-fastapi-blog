from fastapi import FastAPI
from . import schemas, models

from .database import engine

app = FastAPI()


models.Base.metadata.create_all(engine)


@app.post('/blog')
def create(req: schemas.Blog):
    return {"title": req.title, "body": req.body}
