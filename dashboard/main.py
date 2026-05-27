from fastapi.responses import JSONResponse, HTMLResponse
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse
import os
from jinja2 import Environment, FileSystemLoader
from fastapi.responses import FileResponse
from dashboard.data import (
    get_stock_data, get_scores,
    get_unit_economics, get_market_sizing, get_trends
)
from dashboard.charts import (
    stock_chart, scoring_chart,
    unit_economics_chart, market_bubble_chart, trends_chart
)
from datetime import datetime

def get_last_updated():
    return datetime.now().strftime("%d %b %Y, %H:%M")
app = FastAPI(title="Fitness PE Dashboard")

import time
START_TIME = time.time()

@app.get("/health")
async def health_check():
    """Required by Docker HEALTHCHECK and Railway."""
    return {
        "status": "ok",
        "uptime_seconds": round(time.time() - START_TIME, 1),
        "service": "FitPE Analytics"
    }

# ── Static & Templates ───────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app.mount(
    "/static",
    StaticFiles(directory=os.path.join(BASE_DIR, "static")),
    name="static",
)



# ── Root route ───────────────────────────────────────────────────
@app.get("/")
async def index():
    from fastapi.responses import FileResponse
    import os
    return FileResponse(os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates", "index.html"))

# ── API routes — called by JS fetch() ────────────────────────────

@app.get("/api/stocks")
async def api_stocks():
    data  = get_stock_data()
    chart = stock_chart(data)
    return JSONResponse({"chart": chart, "last_updated": get_last_updated()})

@app.get("/api/scoring")
async def api_scoring():
    scores = get_scores()
    chart  = scoring_chart(scores)
    return JSONResponse({"chart": chart, "scores": scores})

@app.get("/api/unit-economics")
async def api_unit_economics():
    ue    = get_unit_economics()
    chart = unit_economics_chart(ue)
    return JSONResponse({"chart": chart, "data": ue})

@app.get("/api/market-sizing")
async def api_market_sizing():
    ms    = get_market_sizing()
    chart = market_bubble_chart(ms)
    return JSONResponse({"chart": chart, "data": ms})

@app.get("/api/trends")
async def api_trends():
    df = get_trends()
    if not df or not df.get("dates"):
        return JSONResponse({"chart": None, "error": "Trends data unavailable"})
    chart = trends_chart(df)
    return JSONResponse({"chart": chart})

@app.get("/api/refresh")
async def api_refresh():
    from datetime import datetime
    # Re-reads all data fresh from CSVs on next request (no caching)
    return JSONResponse({
        "status": "ok",
        "last_updated": datetime.now().strftime("%d %b %Y, %H:%M")
    })