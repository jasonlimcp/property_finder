import io
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
import uvicorn
from src.utils import get_prop_list,get_planarea_list, get_filtered_table, get_stats, get_chart_pricediff, get_chart_anngrowth

app = FastAPI()

@app.get('/')
def read_main():
    return {}

@app.get('/propnames')
def send_prop_list():
    prop_list = get_prop_list()
    prop_list.insert(0,"All")
    return {"proplists":prop_list}

@app.get('/planningareas')
def send_planarea_list():
    planarea_list = get_planarea_list()
    return {"planlists":planarea_list}

@app.get('/stats')
def send_stats(propname,proptype,planarea,propsize_min,propsize_max,newsaleyear):
    df = get_filtered_table(propname,proptype,planarea,propsize_min,propsize_max,newsaleyear)
    dict_stats = get_stats(df)
    return {"stat_dict":dict_stats}

@app.get('/chartprice')
def send_chartprice(propname,proptype,planarea,propsize_min,propsize_max,newsaleyear):
    df = get_filtered_table(propname,proptype,planarea,propsize_min,propsize_max,newsaleyear)
    if len(df) != 0:
        chartprice = get_chart_pricediff(df)
        return StreamingResponse(io.BytesIO(chartprice.read()), media_type="image/png")
    else:
        return None

@app.get('/chartgrowth')
def send_chartgrowth(propname,proptype,planarea,propsize_min,propsize_max,newsaleyear):
    df = get_filtered_table(propname,proptype,planarea,propsize_min,propsize_max,newsaleyear)
    if len(df) != 0:
        chartgrowth = get_chart_anngrowth(df)
        return StreamingResponse(io.BytesIO(chartgrowth.read()), media_type="image/png")
    else:
        return None

if __name__ == "__main__":
    uvicorn.run(app)