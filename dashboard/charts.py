import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np

COLORS = {
    'HVLP':     '#4f98a3',
    'Boutique': '#f97316',
    'Digital':  '#a78bfa',
    'SP500':    '#64748b',
}

LAYOUT_BASE = dict(
    paper_bgcolor='#0f172a',
    plot_bgcolor='#0f172a',
    font=dict(color='#94a3b8', family='Inter, sans-serif'),
    margin=dict(l=50, r=30, t=50, b=50),
    legend=dict(bgcolor='#1e293b', bordercolor='#334155', borderwidth=1),
)

def stock_chart(stock_data: dict) -> str:
    fig = go.Figure()
    label_map = {'PLNT': 'HVLP', 'XPOF': 'Boutique', 'PTON': 'Digital', '^GSPC': 'S&P 500'}
    color_map  = {'PLNT': COLORS['HVLP'], 'XPOF': COLORS['Boutique'],
                  'PTON': COLORS['Digital'], '^GSPC': COLORS['SP500']}

    for sym, df in stock_data.items():
        if df is None or df.empty:
            continue
        norm = (df['Close'] / df['Close'].iloc[0]) * 100
        fig.add_trace(go.Scatter(
            x=df.index, y=norm,
            name=label_map.get(sym, sym),
            line=dict(color=color_map.get(sym, '#fff'), width=2),
            hovertemplate='%{y:.1f}<extra>%{fullData.name}</extra>'
        ))

    fig.update_layout(
        **LAYOUT_BASE,
        title=dict(text='Indexed Stock Performance (Base=100)', font=dict(color='white', size=14)),
        xaxis=dict(gridcolor='#1e293b', showgrid=True),
        yaxis=dict(gridcolor='#1e293b', showgrid=True, title='Index (Start=100)'),
        hovermode='x unified',
    )
    return fig.to_json()

def scoring_chart(scores: dict) -> str:
    cats  = list(scores.keys())
    vals  = list(scores.values())
    clrs  = [COLORS[c] for c in cats]

    fig = go.Figure(go.Bar(
        x=cats, y=vals,
        marker_color=clrs,
        text=[f'{v}/10' for v in vals],
        textposition='outside',
        textfont=dict(color='white', size=13),
    ))
    fig.update_layout(
        **LAYOUT_BASE,
        title=dict(text='PE Investment Score by Category', font=dict(color='white', size=14)),
        yaxis=dict(range=[0, 11], gridcolor='#1e293b', title='Score (out of 10)'),
        xaxis=dict(gridcolor='#1e293b'),
    )
    return fig.to_json()

def unit_economics_chart(ue: dict) -> str:
    fig = make_subplots(rows=1, cols=3,
                        subplot_titles=['LTV ($)', 'CAC ($)', 'LTV:CAC Ratio'])
    cats = list(ue.keys())
    clrs = [COLORS[c] for c in cats]

    for col_i, key in enumerate(['LTV', 'CAC', 'LTV_CAC'], start=1):
        vals = [ue[c][key] for c in cats]
        fig.add_trace(go.Bar(
            x=cats, y=vals,
            marker_color=clrs,
            text=[f'${v:,}' if key != 'LTV_CAC' else f'{v}x' for v in vals],
            textposition='outside',
            textfont=dict(color='white', size=11),
            showlegend=False,
        ), row=1, col=col_i)

    fig.update_layout(
        **LAYOUT_BASE,
        title=dict(text='Unit Economics Breakdown', font=dict(color='white', size=14)),
    )
    fig.update_yaxes(gridcolor='#1e293b')
    fig.update_xaxes(gridcolor='#1e293b')
    return fig.to_json()

def market_bubble_chart(ms: dict) -> str:
    cats  = list(ms.keys())
    x     = [ms[c]['TAM_B'] for c in cats]
    y     = [ms[c]['CAGR'] for c in cats]
    sizes = [ms[c]['PE_Capital_B'] * 60 for c in cats]
    clrs  = [COLORS[c] for c in cats]

    fig = go.Figure(go.Scatter(
        x=x, y=y,
        mode='markers+text',
        marker=dict(size=sizes, color=clrs, opacity=0.8,
                    line=dict(color='white', width=1.5)),
        text=cats,
        textposition='top center',
        textfont=dict(color='white', size=12),
        hovertemplate='<b>%{text}</b><br>TAM: $%{x}B<br>CAGR: %{y}%<extra></extra>'
    ))
    fig.update_layout(
        **LAYOUT_BASE,
        title=dict(text='TAM vs CAGR — Bubble = PE Capital Deployed', font=dict(color='white', size=14)),
        xaxis=dict(title='Total Addressable Market ($B)', gridcolor='#1e293b'),
        yaxis=dict(title='Market CAGR (%)', gridcolor='#1e293b'),
    )
    return fig.to_json()

def trends_chart(trends_df: pd.DataFrame) -> str:
    fig = go.Figure()
    col_colors = ['#4f98a3', '#f97316', '#a78bfa']
    for i, col in enumerate(trends_df.columns):
        fig.add_trace(go.Scatter(
            x=trends_df.index, y=trends_df[col],
            name=col,
            line=dict(color=col_colors[i % len(col_colors)], width=2),
            fill='tozeroy', fillcolor=col_colors[i % len(col_colors)].replace(')', ', 0.06)').replace('rgb', 'rgba'),
        ))
    fig.update_layout(
        **LAYOUT_BASE,
        title=dict(text='Google Search Demand — US Fitness (0–100)', font=dict(color='white', size=14)),
        xaxis=dict(gridcolor='#1e293b'),
        yaxis=dict(gridcolor='#1e293b', title='Search Interest'),
        hovermode='x unified',
    )
    return fig.to_json()