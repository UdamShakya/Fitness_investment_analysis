# 🏋️ US Fitness Industry — PE Investment Analysis

A full-stack quantitative research project analyzing Private Equity investment opportunities across three US fitness categories: **High-Volume Low-Price (HVLP)**, **Boutique**, and **Digital**. Built across 7 Jupyter notebooks, producing 12+ charts and a FastAPI dashboard.

***

## 📁 Repository Structure

```
fitness-investment-analysis/
│
├── 📁 data/
│   ├── raw/                          # Hardcoded research constants
│   ├── processed/
│   │   └── master_df.csv             # Merged dataframe — source of truth
│   └── trends/
│       └── google_trends.csv         # pytrends output (or manual export)
│
├── 📁 analysis/
│   ├── 01_data_collection.ipynb      ✅ yfinance + pytrends + hardcoded data
│   ├── 02_scoring_matrix.ipynb       ✅ Weighted scoring + sensitivity analysis
│   ├── 03_unit_economics.ipynb       ✅ CAC, LTV, margins, payback period
│   ├── 04_revenue_forecast.ipynb     ✅ CAGR-based forecast + regression
│   ├── 05_correlation_heatmap.ipynb  ✅ Macro vs fitness revenue correlations
│   ├── 06_market_sizing.ipynb        ✅ TAM/SAM/SOM + bubble chart
│   └── 07_google_trends.ipynb        ✅ Demand signal analysis
│
├── 📁 output/                        # All generated PNGs
│
├── 📁 dashboard/                     # FastAPI live dashboard (coming)
│   ├── main.py
│   ├── data.py
│   ├── charts.py
│   ├── scheduler.py
│   ├── templates/index.html
│   └── static/
│
├── 📁 presentation/                  # Slides + video script (coming)
│
├── .env
├── .gitignore
├── requirements.txt
└── README.md
```

***

## ✅ Progress — Analysis Notebooks

| Notebook | Module | Status | Outputs |
|---|---|---|---|
| `01_data_collection.ipynb` | Data Layer | ✅ Done | `master_df.csv`, `google_trends.csv` |
| `02_scoring_matrix.ipynb` | Weighted Scoring | ✅ Done | `scoring_heatmap.png`, `radar_chart.png`, `sensitivity_tornado.png` |
| `03_unit_economics.ipynb` | Unit Economics | ✅ Done | `unit_economics_bars.png`, `payback_margins.png` |
| `04_revenue_forecast.ipynb` | Revenue Forecast | ✅ Done | `revenue_forecast.png`, `forecast_table.png` |
| `05_correlation_heatmap.ipynb` | Macro Correlation | ✅ Done | `correlation_heatmap.png` |
| `06_market_sizing.ipynb` | Market Sizing | ✅ Done | `tam_sam_som.png`, `bubble_chart.png`, `members_vs_revenue.png` |
| `07_google_trends.ipynb` | Demand Signals | ✅ Done | `google_trends.png`, `trends_yoy.png`, `trends_momentum.png` |

***

## 📊 Output Charts

### Module 1 — Weighted Scoring Matrix (`02_scoring_matrix.ipynb`)

**`scoring_heatmap.png`**
PE investment scoring heatmap across 7 weighted criteria. HVLP scores highest at ~8.5/10, driven by EBITDA margin quality, LTV:CAC ratio, and macro resilience.

**`radar_chart.png`**
Spider/radar chart comparing all three categories across all 7 investment criteria simultaneously. Visualises HVLP's consistent dominance and Digital's weakness in margin-related axes.

**`sensitivity_tornado.png`**
Tornado chart showing how much HVLP's weighted score changes when each criterion weight is varied ±30%. Confirms score stability — HVLP wins regardless of which criteria is prioritised.

***

### Module 2 — Unit Economics (`03_unit_economics.ipynb`)

**`unit_economics_bars.png`**
Side-by-side bar charts for LTV ($), CAC ($), and LTV:CAC ratio across all three categories.

| Category | CAC | LTV | LTV:CAC | Gross Margin |
|---|---|---|---|---|
| HVLP | $75 | ~$705 | 9.4x | 39.4% |
| Boutique | $320 | ~$2,340 | 7.3x | 35.0% |
| Digital | $95 | ~$315 | 3.3x | 8.0% |

**`payback_margins.png`**
Horizontal bar chart for CAC payback period + gross margin comparison. HVLP recovers CAC in 4 months vs Digital's 18 months.

***

### Module 3 — Revenue Forecast (`04_revenue_forecast.ipynb`)

**`revenue_forecast.png`**
Line chart with historical index (2019–2024) and CAGR-based forecast (2025–2030) per category. Includes COVID shading for 2020 and a forecast boundary marker at 2024.5.

**`forecast_table.png`**
Summary table of 2024 index, 2030 forecast, annual CAGR, and 6-year cumulative change per category.

| Category | 2024 Index | 2030 Forecast | CAGR |
|---|---|---|---|
| HVLP | 118 | ~165 | +6.7% |
| Boutique | 99 | ~102 | +0.5% |
| Digital | 140 | ~114 | -3.0% |

> **Note on R²:** Polynomial regression R² values appear low due to only 6 annual data points and COVID as a structural outlier in 2020. Forward projections are CAGR-driven, not regression-driven, and are analytically sound.

***

### Module 4 — Correlation Heatmap (`05_correlation_heatmap.ipynb`)

**`correlation_heatmap.png`**
Lower-triangle correlation matrix of macro indicators (S&P 500, unemployment, consumer sentiment, CPI, PE deal index) vs fitness revenue indices. Key findings:

- HVLP revenue shows strong **positive correlation** with consumer sentiment and S&P 500 returns
- HVLP shows strong **negative correlation** with unemployment — confirming its macro resilience thesis
- Digital revenue is **negatively correlated** with all macro recovery signals (post-COVID demand reversal)

***

### Module 5 — Market Sizing (`06_market_sizing.ipynb`)

**`tam_sam_som.png`**
Funnel chart showing TAM → SAM → SOM for each category.

| Category | TAM | SAM | SOM | CAGR |
|---|---|---|---|---|
| HVLP | $20.0B | $7.0B | $0.84B | 6.7% |
| Boutique | $5.4B | $1.89B | $0.23B | 12.8% |
| Digital | $8.1B | $2.84B | $0.34B | 3.2% |

**`bubble_chart.png`**
TAM vs CAGR scatter chart where bubble size represents PE capital deployed. HVLP occupies the largest bubble in the large-market quadrant. Boutique sits in the high-growth/small-market quadrant with strong upside.

**`members_vs_revenue.png`**
Dual-axis bar chart comparing total membership scale (millions) vs average revenue per site ($M). HVLP leads on both absolute members (21M) and site-level revenue efficiency ($1.8M/site).

***

### Module 6 — Google Trends (`07_google_trends.ipynb`)

**`google_trends.png`**
5-year monthly smoothed search interest for `planet fitness`, `boutique fitness`, and `peloton` in the US. Annotated with COVID lockdown period.

**`trends_yoy.png`**
Year-over-year change in search interest per category — grouped bar chart showing demand acceleration/deceleration by year.

**`trends_momentum.png`**
90-day rolling average of weekly search interest — smooths noise and highlights sustained momentum vs spikes.

> **Note on data source:** pytrends pulls live data from Google Trends. If a 429 rate-limit error occurs, either wait 1–4 hours and retry, or manually export from [trends.google.com](https://trends.google.com) and load the CSV directly.

***

## 🔑 Key Findings (Summary)

| Metric | HVLP | Boutique | Digital |
|---|---|---|---|
| Investment Score | **8.5/10** | 7.1/10 | 3.2/10 |
| LTV:CAC Ratio | **9.4x** | 7.3x | 3.3x |
| CAC Payback | **4 months** | 7 months | 18 months |
| Gross Margin | **39.4%** | 35.0% | 8.0% |
| PE Capital Deployed | **$3.5B** | $1.5B | $0.2B |
| TAM | **$20B** | $5.4B | $8.1B |
| 2030 Revenue CAGR | **+6.7%** | +0.5% | -3.0% |

**HVLP is the dominant PE investment target** across every financial metric. Boutique is a credible secondary play given its 12.8% CAGR and strong LTV:CAC. Digital has structurally deteriorated post-COVID and carries the weakest unit economics of the three.

***

## ⚙️ Setup

### Prerequisites

```bash
python -m venv venv
source venv/bin/activate        # Mac/Linux
venv\Scripts\activate           # Windows
pip install -r requirements.txt
```

### Run Notebooks

```bash
jupyter notebook
```

Open notebooks in order from `analysis/01_data_collection.ipynb`. Each notebook auto-creates required folders and loads `master_df.csv` from `data/processed/`.

### Requirements

```
pandas
numpy
scikit-learn
yfinance
pytrends
matplotlib
seaborn
plotly
kaleido
fastapi
uvicorn
jinja2
python-dotenv
apscheduler
requests
jupyter
```

***# 🏋️ US Fitness Industry — PE Investment Analysis

A full-stack quantitative research project analyzing Private Equity investment opportunities across three US fitness categories: **High-Volume Low-Price (HVLP)**, **Boutique**, and **Digital**. Built across 7 Jupyter notebooks, producing 12+ charts and a FastAPI dashboard.

***

## 📁 Repository Structure

```
fitness-investment-analysis/
│
├── 📁 data/
│   ├── raw/                          # Hardcoded research constants
│   ├── processed/
│   │   └── master_df.csv             # Merged dataframe — source of truth
│   └── trends/
│       └── google_trends.csv         # pytrends output (or manual export)
│
├── 📁 analysis/
│   ├── 01_data_collection.ipynb      ✅ yfinance + pytrends + hardcoded data
│   ├── 02_scoring_matrix.ipynb       ✅ Weighted scoring + sensitivity analysis
│   ├── 03_unit_economics.ipynb       ✅ CAC, LTV, margins, payback period
│   ├── 04_revenue_forecast.ipynb     ✅ CAGR-based forecast + regression
│   ├── 05_correlation_heatmap.ipynb  ✅ Macro vs fitness revenue correlations
│   ├── 06_market_sizing.ipynb        ✅ TAM/SAM/SOM + bubble chart
│   └── 07_google_trends.ipynb        ✅ Demand signal analysis
│
├── 📁 output/                        # All generated PNGs
│
├── 📁 dashboard/                     # FastAPI live dashboard (coming)
│   ├── main.py
│   ├── data.py
│   ├── charts.py
│   ├── scheduler.py
│   ├── templates/index.html
│   └── static/
│
├── 📁 presentation/                  # Slides + video script (coming)
│
├── .env
├── .gitignore
├── requirements.txt
└── README.md
```

***

## ✅ Progress — Analysis Notebooks

| Notebook | Module | Status | Outputs |
|---|---|---|---|
| `01_data_collection.ipynb` | Data Layer | ✅ Done | `master_df.csv`, `google_trends.csv` |
| `02_scoring_matrix.ipynb` | Weighted Scoring | ✅ Done | `scoring_heatmap.png`, `radar_chart.png`, `sensitivity_tornado.png` |
| `03_unit_economics.ipynb` | Unit Economics | ✅ Done | `unit_economics_bars.png`, `payback_margins.png` |
| `04_revenue_forecast.ipynb` | Revenue Forecast | ✅ Done | `revenue_forecast.png`, `forecast_table.png` |
| `05_correlation_heatmap.ipynb` | Macro Correlation | ✅ Done | `correlation_heatmap.png` |
| `06_market_sizing.ipynb` | Market Sizing | ✅ Done | `tam_sam_som.png`, `bubble_chart.png`, `members_vs_revenue.png` |
| `07_google_trends.ipynb` | Demand Signals | ✅ Done | `google_trends.png`, `trends_yoy.png`, `trends_momentum.png` |

***

## 📊 Output Charts

### Module 1 — Weighted Scoring Matrix (`02_scoring_matrix.ipynb`)

**`scoring_heatmap.png`**
PE investment scoring heatmap across 7 weighted criteria. HVLP scores highest at ~8.5/10, driven by EBITDA margin quality, LTV:CAC ratio, and macro resilience.

**`radar_chart.png`**
Spider/radar chart comparing all three categories across all 7 investment criteria simultaneously. Visualises HVLP's consistent dominance and Digital's weakness in margin-related axes.

**`sensitivity_tornado.png`**
Tornado chart showing how much HVLP's weighted score changes when each criterion weight is varied ±30%. Confirms score stability — HVLP wins regardless of which criteria is prioritised.

***

### Module 2 — Unit Economics (`03_unit_economics.ipynb`)

**`unit_economics_bars.png`**
Side-by-side bar charts for LTV ($), CAC ($), and LTV:CAC ratio across all three categories.

| Category | CAC | LTV | LTV:CAC | Gross Margin |
|---|---|---|---|---|
| HVLP | $75 | ~$705 | 9.4x | 39.4% |
| Boutique | $320 | ~$2,340 | 7.3x | 35.0% |
| Digital | $95 | ~$315 | 3.3x | 8.0% |

**`payback_margins.png`**
Horizontal bar chart for CAC payback period + gross margin comparison. HVLP recovers CAC in 4 months vs Digital's 18 months.

***

### Module 3 — Revenue Forecast (`04_revenue_forecast.ipynb`)

**`revenue_forecast.png`**
Line chart with historical index (2019–2024) and CAGR-based forecast (2025–2030) per category. Includes COVID shading for 2020 and a forecast boundary marker at 2024.5.

**`forecast_table.png`**
Summary table of 2024 index, 2030 forecast, annual CAGR, and 6-year cumulative change per category.

| Category | 2024 Index | 2030 Forecast | CAGR |
|---|---|---|---|
| HVLP | 118 | ~165 | +6.7% |
| Boutique | 99 | ~102 | +0.5% |
| Digital | 140 | ~114 | -3.0% |

> **Note on R²:** Polynomial regression R² values appear low due to only 6 annual data points and COVID as a structural outlier in 2020. Forward projections are CAGR-driven, not regression-driven, and are analytically sound.

***

### Module 4 — Correlation Heatmap (`05_correlation_heatmap.ipynb`)

**`correlation_heatmap.png`**
Lower-triangle correlation matrix of macro indicators (S&P 500, unemployment, consumer sentiment, CPI, PE deal index) vs fitness revenue indices. Key findings:

- HVLP revenue shows strong **positive correlation** with consumer sentiment and S&P 500 returns
- HVLP shows strong **negative correlation** with unemployment — confirming its macro resilience thesis
- Digital revenue is **negatively correlated** with all macro recovery signals (post-COVID demand reversal)

***

### Module 5 — Market Sizing (`06_market_sizing.ipynb`)

**`tam_sam_som.png`**
Funnel chart showing TAM → SAM → SOM for each category.

| Category | TAM | SAM | SOM | CAGR |
|---|---|---|---|---|
| HVLP | $20.0B | $7.0B | $0.84B | 6.7% |
| Boutique | $5.4B | $1.89B | $0.23B | 12.8% |
| Digital | $8.1B | $2.84B | $0.34B | 3.2% |

**`bubble_chart.png`**
TAM vs CAGR scatter chart where bubble size represents PE capital deployed. HVLP occupies the largest bubble in the large-market quadrant. Boutique sits in the high-growth/small-market quadrant with strong upside.

**`members_vs_revenue.png`**
Dual-axis bar chart comparing total membership scale (millions) vs average revenue per site ($M). HVLP leads on both absolute members (21M) and site-level revenue efficiency ($1.8M/site).

***

### Module 6 — Google Trends (`07_google_trends.ipynb`)

**`google_trends.png`**
5-year monthly smoothed search interest for `planet fitness`, `boutique fitness`, and `peloton` in the US. Annotated with COVID lockdown period.

**`trends_yoy.png`**
Year-over-year change in search interest per category — grouped bar chart showing demand acceleration/deceleration by year.

**`trends_momentum.png`**
90-day rolling average of weekly search interest — smooths noise and highlights sustained momentum vs spikes.

> **Note on data source:** pytrends pulls live data from Google Trends. If a 429 rate-limit error occurs, either wait 1–4 hours and retry, or manually export from [trends.google.com](https://trends.google.com) and load the CSV directly.

***

## 🔑 Key Findings (Summary)

| Metric | HVLP | Boutique | Digital |
|---|---|---|---|
| Investment Score | **8.5/10** | 7.1/10 | 3.2/10 |
| LTV:CAC Ratio | **9.4x** | 7.3x | 3.3x |
| CAC Payback | **4 months** | 7 months | 18 months |
| Gross Margin | **39.4%** | 35.0% | 8.0% |
| PE Capital Deployed | **$3.5B** | $1.5B | $0.2B |
| TAM | **$20B** | $5.4B | $8.1B |
| 2030 Revenue CAGR | **+6.7%** | +0.5% | -3.0% |

**HVLP is the dominant PE investment target** across every financial metric. Boutique is a credible secondary play given its 12.8% CAGR and strong LTV:CAC. Digital has structurally deteriorated post-COVID and carries the weakest unit economics of the three.

***

## ⚙️ Setup

### Prerequisites

```bash
python -m venv venv
source venv/bin/activate        # Mac/Linux
venv\Scripts\activate           # Windows
pip install -r requirements.txt
```

### Run Notebooks

```bash
jupyter notebook
```

Open notebooks in order from `analysis/01_data_collection.ipynb`. Each notebook auto-creates required folders and loads `master_df.csv` from `data/processed/`.

### Requirements

```
pandas
numpy
scikit-learn
yfinance
pytrends
matplotlib
seaborn
plotly
kaleido
fastapi
uvicorn
jinja2
python-dotenv
apscheduler
requests
jupyter
```

***k