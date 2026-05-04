"""
dashboard/charts.py
Builds Plotly chart JSON for each API endpoint.
All functions return a dict (Plotly figure as JSON-serialisable object).
"""
import json

# ── Shared theme ──────────────────────────────────────────────────
DARK_BG    = "#1c1b19"
PAPER_BG   = "#201f1d"
GRID_COLOR = "#262523"
FONT_COLOR = "#cdccca"
FONT_MUTED = "#797876"
FONT       = "Satoshi, -apple-system, sans-serif"

BASE_LAYOUT = dict(
    paper_bgcolor = PAPER_BG,
    plot_bgcolor  = DARK_BG,
    font          = dict(family=FONT, color=FONT_COLOR, size=12),
    margin        = dict(l=48, r=24, t=24, b=48),
    legend        = dict(
        bgcolor     = "rgba(0,0,0,0)",
        borderwidth = 0,
        font        = dict(size=11, color=FONT_COLOR),
    ),
    xaxis = dict(
        gridcolor    = GRID_COLOR,
        linecolor    = GRID_COLOR,
        tickfont     = dict(color=FONT_MUTED, size=11),
        showgrid     = False,
        zeroline     = False,
    ),
    yaxis = dict(
        gridcolor    = GRID_COLOR,
        linecolor    = GRID_COLOR,
        tickfont     = dict(color=FONT_MUTED, size=11),
        showgrid     = True,
        zeroline     = False,
    ),
    hoverlabel = dict(
        bgcolor   = "#2d2c2a",
        bordercolor = "#393836",
        font      = dict(family=FONT, size=12, color=FONT_COLOR),
    ),
)


def _fig(data, layout_overrides=None):
    layout = {**BASE_LAYOUT, **(layout_overrides or {})}
    return {"data": data, "layout": layout}


# ── 1. Stock performance line chart ──────────────────────────────
def stock_chart(d: dict) -> dict:
    traces = []
    for s in d["series"]:
        traces.append({
            "type":  "scatter",
            "mode":  "lines",
            "name":  s["name"],
            "x":     d["dates"],
            "y":     s["values"],
            "line":  {"color": s["color"], "width": 2},
            "hovertemplate": "<b>%{meta}</b>  %{x}<br>Index: %{y:.0f}<extra></extra>",
            "meta":  s["name"],
        })
    return _fig(traces, {
        "yaxis": {**BASE_LAYOUT["yaxis"], "title": {"text": "Indexed (100 = start)", "font": {"size": 11, "color": FONT_MUTED}}},
        "hovermode": "x unified",
    })


# ── 2. Scoring matrix radar / bar chart ──────────────────────────
def scoring_chart(d: dict) -> dict:
    colors = {"HVLP": "#4f98a3", "Boutique": "#e8af34", "Digital": "#dd6974"}
    traces = []
    for cat in d["categories"]:
        traces.append({
            "type":        "bar",
            "name":        cat,
            "x":           d["criteria"],
            "y":           d["scores"][cat],
            "marker":      {"color": colors.get(cat, "#bab9b4"), "opacity": 0.85},
            "hovertemplate": f"<b>{cat}</b><br>%{{x}}: %{{y}}/10<extra></extra>",
        })
    return _fig(traces, {
        "barmode": "group",
        "yaxis":   {**BASE_LAYOUT["yaxis"],
                    "range": [0, 10],
                    "title": {"text": "Score / 10", "font": {"size": 11, "color": FONT_MUTED}}},
        "xaxis":   {**BASE_LAYOUT["xaxis"], "tickangle": -20},
    })


# ── 3. Unit economics grouped bar ────────────────────────────────
def unit_economics_chart(rows: list) -> dict:
    cats   = [r["category"] for r in rows]
    colors = {"HVLP": "#4f98a3", "Boutique": "#e8af34", "Digital": "#dd6974"}

    traces = [
        {
            "type":            "bar",
            "name":            "LTV ($)",
            "x":               cats,
            "y":               [r["ltv"] for r in rows],
            "marker":          {"color": [colors.get(c, "#bab9b4") for c in cats], "opacity": 0.9},
            "hovertemplate":   "LTV: $%{y}<extra></extra>",
        },
        {
            "type":            "bar",
            "name":            "CAC ($)",
            "x":               cats,
            "y":               [r["cac"] for r in rows],
            "marker":          {"color": [colors.get(c, "#bab9b4") for c in cats], "opacity": 0.45},
            "hovertemplate":   "CAC: $%{y}<extra></extra>",
        },
        {
            "type":            "scatter",
            "mode":            "markers+text",
            "name":            "LTV:CAC",
            "x":               cats,
            "y":               [r["ltv_cac"] * 60 for r in rows],  # scaled for visibility
            "text":            [f'{r["ltv_cac"]}x' for r in rows],
            "textposition":    "top center",
            "marker":          {"size": 10, "color": "#ffffff", "opacity": 0.9},
            "yaxis":           "y2",
            "hovertemplate":   "LTV:CAC %{text}<extra></extra>",
        },
    ]
    return _fig(traces, {
        "barmode": "group",
        "yaxis":  {**BASE_LAYOUT["yaxis"],
                   "title": {"text": "$ Value", "font": {"size":11,"color":FONT_MUTED}}},
        "yaxis2": {"overlaying":"y","side":"right","showgrid":False,
                   "tickfont":{"color":FONT_MUTED,"size":11},
                   "title":{"text":"LTV:CAC ratio","font":{"size":11,"color":FONT_MUTED}}},
    })


# ── 4. Market sizing bubble chart ────────────────────────────────
def market_bubble_chart(rows: list) -> dict:
    colors = {"HVLP": "#4f98a3", "Boutique": "#e8af34", "Digital": "#dd6974"}
    traces = []
    for r in rows:
        cat = r["category"]
        traces.append({
            "type": "scatter",
            "mode": "markers+text",
            "name": cat,
            "x":    [r["cagr"]],
            "y":    [r["tam_bn"]],
            "text": [cat],
            "textposition": "top center",
            "marker": {
                "size":    [r["pe_capital_bn"] * 28],
                "color":   colors.get(cat, "#bab9b4"),
                "opacity": 0.8,
                "line":    {"width": 1.5, "color": "#393836"},
                "sizemode": "diameter",
            },
            "hovertemplate": (
                f"<b>{cat}</b><br>"
                "TAM: $%{y}B<br>"
                "CAGR: %{x}%<br>"
                f"PE Capital: ${r['pe_capital_bn']}B"
                "<extra></extra>"
            ),
        })
    return _fig(traces, {
        "xaxis": {**BASE_LAYOUT["xaxis"],
                  "title": {"text": "CAGR (%)", "font": {"size":11,"color":FONT_MUTED}}},
        "yaxis": {**BASE_LAYOUT["yaxis"],
                  "title": {"text": "TAM ($B)", "font": {"size":11,"color":FONT_MUTED}}},
        "showlegend": True,
    })


# ── 5. Google Trends line chart ───────────────────────────────────
def trends_chart(d: dict) -> dict:
    traces = []
    for s in d["series"]:
        traces.append({
            "type": "scatter",
            "mode": "lines",
            "name": s["name"].title(),
            "x":    d["dates"],
            "y":    s["values"],
            "line": {"color": s["color"], "width": 2, "shape": "spline", "smoothing": 0.8},
            "fill": "tozeroy",
            "fillcolor": s["color"].replace("#", "rgba(").rstrip(")") + ",0.06)" if s["color"].startswith("#") else s["color"],
            "hovertemplate": "<b>%{meta}</b>  %{x}<br>Interest: %{y}<extra></extra>",
            "meta": s["name"].title(),
        })
    return _fig(traces, {
        "yaxis": {**BASE_LAYOUT["yaxis"],
                  "range": [0, 105],
                  "title": {"text": "Search Interest (0–100)", "font": {"size":11,"color":FONT_MUTED}}},
        "hovermode": "x unified",
    })
