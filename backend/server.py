from fastapi import FastAPI
import uvicorn
from src.utils import get_prop_list

app = FastAPI()

@app.get('/')
def read_main():
    return {}

@app.get('/propnames')
def send_prop_list():
    prop_list = get_prop_list()
    prop_list.insert(0,"All") #Add 'All' option
    return {"lists":prop_list}

if __name__ == "__main__":
    uvicorn.run(app)