import pandas as pd
import numpy as np
import yfinance as yf
from datetime import datetime, timedelta
import os

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# ── Cached data store ─────────────────────────────────────────────
_cache = {
    'stock_data':    None,
    'last_updated':  None,
}

# ── Tickers ───────────────────────────────────────────────────────
TICKERS = {
    'PLNT':  'Planet Fitness (HVLP)',
    'XPOF':  'Xponential Fitness (Boutique)',
    'PTON':  'Peloton (Digital)',
    'S&P500': '^GSPC',
}

def fetch_stock_data(period='1y'):
    """Pull latest price data from yfinance."""
    symbols = ['PLNT', 'XPOF', 'PTON', '^GSPC']
    data = {}
    for sym in symbols:
        try:
            tk = yf.Ticker(sym)
            hist = tk.history(period=period)
            if not hist.empty:
                data[sym] = hist[['Close', 'Volume']].copy()
        except Exception as e:
            print(f"⚠️  Could not fetch {sym}: {e}")
    _cache['stock_data']   = data
    _cache['last_updated'] = datetime.now()
    return data

def get_stock_data():
    """Return cached data or fetch fresh if >1 hour old."""
    if _cache['stock_data'] is None or \
       (datetime.now() - _cache['last_updated']) > timedelta(hours=1):
        return fetch_stock_data()
    return _cache['stock_data']

def get_last_updated():
    if _cache['last_updated']:
        return _cache['last_updated'].strftime('%Y-%m-%d %H:%M:%S')
    return 'Not yet fetched'

# ── Static research data ──────────────────────────────────────────
def get_unit_economics():
    return {
        'HVLP':     {'CAC': 75,  'LTV': 705,  'LTV_CAC': 9.4, 'Gross_Margin': 39.4, 'Payback_Mos': 4},
        'Boutique': {'CAC': 320, 'LTV': 2340, 'LTV_CAC': 7.3, 'Gross_Margin': 35.0, 'Payback_Mos': 7},
        'Digital':  {'CAC': 95,  'LTV': 315,  'LTV_CAC': 3.3, 'Gross_Margin': 8.0,  'Payback_Mos': 18},
    }

def get_market_sizing():
    return {
        'HVLP':     {'TAM_B': 20.0, 'CAGR': 6.7,  'PE_Capital_B': 3.5, 'Members_M': 21.0},
        'Boutique': {'TAM_B': 5.4,  'CAGR': 12.8, 'PE_Capital_B': 1.5, 'Members_M': 6.2},
        'Digital':  {'TAM_B': 8.1,  'CAGR': 3.2,  'PE_Capital_B': 0.2, 'Members_M': 9.8},
    }

def get_scores():
    return {'HVLP': 8.5, 'Boutique': 7.1, 'Digital': 3.2}

def get_master_df():
    path = os.path.join(BASE_DIR, 'data', 'processed', 'master_df.csv')
    if os.path.exists(path):
        return pd.read_csv(path, index_col=0)
    return pd.DataFrame()

def get_trends():
    path = os.path.join(BASE_DIR, 'data', 'trends', 'google_trends.csv')
    if os.path.exists(path):
        df = pd.read_csv(path, index_col=0, parse_dates=True)
        return df
    return pd.DataFrame()