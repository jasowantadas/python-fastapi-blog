from fastapi import FastAPI
from . import schemas

app = FastAPI()


@app.post('/blog')
def create(req: schemas.Blog):
    return {"title": req.title, "body": req.body}
