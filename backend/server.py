from fastapi import FastAPI
import uvicorn

app = FastAPI()

@app.get('/')
def read_main():
    return {"msg": "Hello world!"}


@app.get('/main')
def read_main():
    return {"msg": "Hello Jason!"}


@app.get('/test')
def get_test_output(data):
    return {"msg": "yoyo!" + data}


if __name__ == "__main__":
    uvicorn.run(app)