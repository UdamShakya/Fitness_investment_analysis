"""
dashboard/data.py
Reads processed CSVs from data/processed/ and returns clean dicts
for each API endpoint.
"""
import os
import pandas as pd

BASE_DIR   = os.path.dirname(os.path.abspath(__file__))
PROCESSED  = os.path.join(BASE_DIR, "..", "data", "processed")

def _csv(name):
    return os.path.join(PROCESSED, name)


# ── 1. Stock performance ──────────────────────────────────────────
def get_stock_data():
    path = _csv("stock_performance.csv")
    if not os.path.exists(path):
        # Fallback hardcoded data so dashboard never crashes
        return {
            "dates":  ["2020-01","2021-01","2022-01","2023-01","2024-01","2024-12"],
            "series": [
                {"name": "PLNT",  "color": "#4f98a3", "values": [100,142,168,131,154,172]},
                {"name": "XPOF",  "color": "#e8af34", "values": [100,118,95, 88, 102,110]},
                {"name": "PTON",  "color": "#dd6974", "values": [100,380,210,42,  28,  22]},
                {"name": "S&P500","color": "#797876", "values": [100,118,108,113,143,158]},
            ]
        }
    df = pd.read_csv(path)
    dates = df["date"].tolist()
    series = []
    colors = {"PLNT":"#4f98a3","XPOF":"#e8af34","PTON":"#dd6974","SP500":"#797876"}
    for col in [c for c in df.columns if c != "date"]:
        series.append({
            "name":   col,
            "color":  colors.get(col, "#bab9b4"),
            "values": df[col].tolist()
        })
    return {"dates": dates, "series": series}


# ── 2. PE scoring matrix ──────────────────────────────────────────
def get_scores():
    path = _csv("scoring_matrix.csv")
    if not os.path.exists(path):
        return {
            "categories": ["HVLP", "Boutique", "Digital"],
            "criteria": [
                "Market Size","Growth Rate","Unit Economics",
                "Competitive Moat","PE Track Record","Scalability","Recession Resilience"
            ],
            "scores": {
                "HVLP":     [9, 8, 9, 8, 9, 9, 8],
                "Boutique": [7, 9, 7, 8, 7, 7, 6],
                "Digital":  [6, 4, 3, 4, 3, 7, 3],
            },
            "totals": {"HVLP": 8.5, "Boutique": 7.1, "Digital": 3.2}
        }
    df = pd.read_csv(path)
    return {
        "categories": df.columns[1:].tolist(),
        "criteria":   df["criteria"].tolist(),
        "scores": {
            col: df[col].tolist()
            for col in df.columns[1:]
        },
        "totals": {col: round(df[col].mean(), 1) for col in df.columns[1:]}
    }


# ── 3. Unit economics ─────────────────────────────────────────────
def get_unit_economics():
    path = _csv("unit_economics.csv")
    if not os.path.exists(path):
        return [
            {"category":"HVLP",    "cac":75,  "ltv":705, "ltv_cac":9.4,
             "gross_margin":39.4,  "payback_months":4},
            {"category":"Boutique","cac":120, "ltv":600, "ltv_cac":5.0,
             "gross_margin":32.0,  "payback_months":9},
            {"category":"Digital", "cac":95,  "ltv":312, "ltv_cac":3.3,
             "gross_margin":8.0,   "payback_months":18},
        ]
    df = pd.read_csv(path)
    return df.to_dict(orient="records")


# ── 4. Market sizing ──────────────────────────────────────────────
def get_market_sizing():
    path = _csv("market_sizing.csv")
    if not os.path.exists(path):
        return [
            {"category":"HVLP",    "tam_bn":20, "cagr":6.7,
             "pe_capital_bn":3.5,  "members_m":21},
            {"category":"Boutique","tam_bn":12, "cagr":12.8,
             "pe_capital_bn":2.1,  "members_m":9},
            {"category":"Digital", "tam_bn":8,  "cagr":3.2,
             "pe_capital_bn":0.8,  "members_m":7},
        ]
    df = pd.read_csv(path)
    return df.to_dict(orient="records")


# ── 5. Google Trends ──────────────────────────────────────────────
def get_trends():
    path = _csv("google_trends.csv")
    if not os.path.exists(path):
        months = [
            "2020-01","2020-04","2020-07","2020-10",
            "2021-01","2021-04","2021-07","2021-10",
            "2022-01","2022-04","2022-07","2022-10",
            "2023-01","2023-04","2023-07","2023-10",
            "2024-01","2024-04","2024-07","2024-10",
        ]
        return {
            "dates": months,
            "series": [
                {"name":"planet fitness", "color":"#4f98a3",
                 "values":[62,58,55,60,65,68,70,66,72,74,75,71,73,76,78,74,77,79,80,76]},
                {"name":"boutique fitness","color":"#e8af34",
                 "values":[40,12,22,30,35,42,48,44,50,55,58,53,56,60,62,57,59,63,65,61]},
                {"name":"peloton",         "color":"#dd6974",
                 "values":[30,35,80,75,100,90,70,60,45,35,30,28,25,22,20,18,17,16,15,14]},
            ]
        }
    df = pd.read_csv(path)
    dates = df["date"].tolist() if "date" in df.columns else df.iloc[:,0].tolist()
    colors = {"planet fitness":"#4f98a3","boutique fitness":"#e8af34","peloton":"#dd6974"}
    series = []
    for col in [c for c in df.columns if c != "date"]:
        series.append({
            "name":   col,
            "color":  colors.get(col.lower(), "#bab9b4"),
            "values": df[col].tolist()
        })
    return {"dates": dates, "series": series}
