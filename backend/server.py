from fastapi import FastAPI
import uvicorn
from src.utils import propnames

app = FastAPI()

@app.get('/')
def read_main():
    return {}

@app.get('/propnames')
def get_prop_list():
    prop_list = propnames()
    prop_list.insert(0,"All") #Add 'All' option
    return {"lister":prop_list}

if __name__ == "__main__":
    uvicorn.run(app)