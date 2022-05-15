from fastapi import FastAPI
import uvicorn
from src.utils import get_prop_list, get_sales_stats
from fastapi.responses import FileResponse

app = FastAPI()

@app.get('/')
def read_main():
    return {}

@app.get('/propnames')
def send_prop_list():
    prop_list = get_prop_list()
    prop_list.insert(0,"All") #Add 'All' option
    return {"lists":prop_list}

@app.get('/stats')
def send_stats_table(propname,postdist,propsize_min,propsize_max,newsaleyear):
    count = get_sales_stats(propname,postdist,propsize_min,propsize_max,newsaleyear)
    return {"stats":count}

@app.get('/img')
def send_img():
    pict = 'data/dsc.jpg'
    return FileResponse(pict)

if __name__ == "__main__":
    uvicorn.run(app)