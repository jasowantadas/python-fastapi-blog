from fastapi import FastAPI

app = FastAPI()


@app.get('/')
def index():
    return {'data': {'name': "Jasowanta Das"}}


@app.get('/about')
def about():
    return {'data': {'about': "About page"}}
