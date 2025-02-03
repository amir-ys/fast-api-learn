
from fastapi import FastAPI

app = FastAPI()

@app.get('/{id}')
def hello(id : int):
    return {
       "message" : f"id:{id}"
    }