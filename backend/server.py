from fastapi import FastAPI
import uvicorn
from src.utils import propnames

app = FastAPI()

@app.get('/')
def read_main():
    return {"msg": "Hello world!"}


@app.get('/main')
def read_main():
    return {"msg": "Hello Jason!"}

@app.get('/propnames')
def get_prop_list():
    prop_list = propnames()
    return prop_list

@app.get('/test')
def get_test_output(data):
    return {"msg": "yoyo!" + data}


if __name__ == "__main__":
    uvicorn.run(app)