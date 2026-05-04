from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse
import os

app = FastAPI(title="Fitness PE Dashboard")

# ── Static & Templates ───────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app.mount(
    "/static",
    StaticFiles(directory=os.path.join(BASE_DIR, "static")),
    name="static",
)

templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

# ── Root route ───────────────────────────────────────────────────
@app.get("/")
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# ── Your existing API routes go below ───────────────────────────

from dashboard.data import (
    get_stock_data, get_unit_economics,
    get_market_sizing, get_scores,
    get_trends, get_last_updated, fetch_stock_data
)
from dashboard.charts import (
    stock_chart, scoring_chart,
    unit_economics_chart, market_bubble_chart,
    trends_chart
)
from dashboard.scheduler import start_scheduler

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

@asynccontextmanager
async def lifespan(app: FastAPI):
    fetch_stock_data()          # warm cache on startup
    scheduler = start_scheduler()
    yield
    scheduler.shutdown()

app = FastAPI(title="Fitness PE Dashboard", lifespan=lifespan)

app.mount("/static",
          StaticFiles(directory=os.path.join(BASE_DIR, "dashboard", "static")),
          name="static")

templates = Jinja2Templates(
    directory=os.path.join(BASE_DIR, "dashboard", "templates")
)

# ── Pages ─────────────────────────────────────────────────────────

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

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
    if df.empty:
        return JSONResponse({"chart": None, "error": "Trends data not available"})
    chart = trends_chart(df)
    return JSONResponse({"chart": chart})

@app.get("/api/refresh")
async def api_refresh():
    fetch_stock_data()
    return JSONResponse({"status": "refreshed", "last_updated": get_last_updated()})