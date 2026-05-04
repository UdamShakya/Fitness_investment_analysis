/* dashboard/static/app.js — v2
   Features: animated KPI counters, category filter pills, score drill-down,
   "why invest" verdict cards, chart export buttons
*/

// ── Design tokens (match style.css) ─────────────────────────────
const CAT_COLORS = { hvlp:'#4f98a3', boutique:'#e8af34', digital:'#dd6974' };

const PLOTLY_BASE = {
  paper_bgcolor:'#201f1d', plot_bgcolor:'#1c1b19',
  font:{ family:'Satoshi,-apple-system,sans-serif', color:'#cdccca', size:12 },
  margin:{ l:52, r:24, t:16, b:52 },
  legend:{ bgcolor:'rgba(0,0,0,0)', borderwidth:0, font:{ size:11 } },
  xaxis:{ gridcolor:'#262523', linecolor:'#262523', tickfont:{ color:'#797876',size:11 }, showgrid:false, zeroline:false },
  yaxis:{ gridcolor:'#262523', linecolor:'#262523', tickfont:{ color:'#797876',size:11 }, showgrid:true,  zeroline:false },
  hoverlabel:{ bgcolor:'#2d2c2a', bordercolor:'#393836', font:{ size:12, color:'#cdccca' } },
};

// Scoring criteria for drill-down (7 criteria, max 10 each)
const SCORE_CRITERIA = {
  hvlp:     { 'Revenue Growth':9, 'EBITDA Margin':8, 'LTV:CAC':10, 'Market Share':9, 'Brand Strength':8, 'PE Sentiment':9, 'Digital Integration':6 },
  boutique: { 'Revenue Growth':7, 'EBITDA Margin':9, 'LTV:CAC':7,  'Market Share':6, 'Brand Strength':9, 'PE Sentiment':7, 'Digital Integration':7 },
  digital:  { 'Revenue Growth':3, 'EBITDA Margin':2, 'LTV:CAC':3,  'Market Share':4, 'Brand Strength':5, 'PE Sentiment':2, 'Digital Integration':8 },
};

const cache = {};
let activeFilter = 'all';

// ── Lucide icons ─────────────────────────────────────────────────
lucide.createIcons();

// ── Timestamp ────────────────────────────────────────────────────
document.getElementById('last-updated-ts').textContent =
  new Date().toLocaleString('en-GB',{ day:'2-digit',month:'short',year:'numeric',hour:'2-digit',minute:'2-digit' });

// ── Tab switching ────────────────────────────────────────────────
document.querySelectorAll('.nav-item').forEach(btn => {
  btn.addEventListener('click', () => {
    const tab = btn.dataset.tab;
    activateTab(tab);
    loadTab(tab);
  });
});

function activateTab(tab) {
  document.querySelectorAll('.nav-item').forEach(b => b.classList.toggle('active', b.dataset.tab === tab));
  document.querySelectorAll('.tab-panel').forEach(p => p.classList.toggle('active', p.id === `tab-${tab}`));
  const titles = { overview:'Overview','unit-econ':'Unit Economics', market:'Market Sizing', trends:'Demand Trends' };
  document.querySelector('.topbar-title').textContent = titles[tab] || tab;
  // Animate KPIs on every tab switch
  animateKPIsInTab(tab);
}

// ── Refresh ──────────────────────────────────────────────────────
document.getElementById('btn-refresh').addEventListener('click', async () => {
  Object.keys(cache).forEach(k => delete cache[k]);
  const btn = document.getElementById('btn-refresh');
  btn.innerHTML = '<i data-lucide="loader"></i> Refreshing…';
  btn.disabled = true;
  lucide.createIcons();
  try { await fetch('/api/refresh'); } catch(e){}
  const active = document.querySelector('.nav-item.active')?.dataset.tab || 'overview';
  await loadTab(active, true);
  btn.innerHTML = '<i data-lucide="refresh-cw"></i> Refresh';
  btn.disabled = false;
  lucide.createIcons();
  document.getElementById('last-updated-ts').textContent =
    new Date().toLocaleString('en-GB',{ day:'2-digit',month:'short',year:'numeric',hour:'2-digit',minute:'2-digit' });
});

// ── Export buttons ───────────────────────────────────────────────
document.addEventListener('click', e => {
  const btn = e.target.closest('[data-export]');
  if (!btn) return;
  const id = btn.dataset.export;
  const el = document.getElementById(id);
  if (!el || !el._fullLayout) return;
  Plotly.downloadImage(el, { format:'png', filename: id, width:1200, height:500 });
});

// ── Category filter pills ────────────────────────────────────────
document.querySelectorAll('.pill').forEach(pill => {
  pill.addEventListener('click', () => {
    activeFilter = pill.dataset.filter;
    document.querySelectorAll('.pill').forEach(p => p.classList.toggle('active', p.dataset.filter === activeFilter));
    applyFilter(activeFilter);
  });
});

function applyFilter(filter) {
  // Highlight/dim KPI cards
  document.querySelectorAll('.kpi-card[data-category]').forEach(card => {
    const match = filter === 'all' || card.dataset.category === filter;
    card.style.opacity = match ? '1' : '0.35';
    card.style.transform = match ? 'translateY(0)' : 'translateY(2px)';
  });
  // Filter stock chart traces if loaded
  const stockEl = document.getElementById('chart-stocks');
  if (stockEl && stockEl.data) {
    const catMap = { hvlp:'PLNT', boutique:'XPOF', digital:'PTON' };
    const visible = stockEl.data.map(trace => {
      if (filter === 'all') return true;
      const name = (trace.name || '').toUpperCase();
      const target = (catMap[filter] || '').toUpperCase();
      return name.includes(target) || name.includes('S&P') || name.includes('SPY');
    }).map(v => v ? true : 'legendonly');
    Plotly.restyle(stockEl, { visible });
  }
}

// ── KPI counter animation ────────────────────────────────────────
function animateKPI(el) {
  const target = parseFloat(el.dataset.target || 0);
  const prefix = el.dataset.prefix || '';
  const suffix = el.dataset.suffix || '';
  const duration = 900;
  const start = performance.now();
  const decimals = target % 1 !== 0 ? 1 : 0;

  function tick(now) {
    const elapsed = now - start;
    const progress = Math.min(elapsed / duration, 1);
    const ease = 1 - Math.pow(1 - progress, 3); // ease-out cubic
    const current = (target * ease).toFixed(decimals);
    el.textContent = prefix + current + suffix;
    if (progress < 1) requestAnimationFrame(tick);
    else {
      el.textContent = prefix + target.toFixed(decimals) + suffix;
      el.classList.add('kpi-pop');
      setTimeout(() => el.classList.remove('kpi-pop'), 400);
    }
  }
  requestAnimationFrame(tick);
}

function animateKPIsInTab(tab) {
  const panel = document.getElementById(`tab-${tab}`);
  if (!panel) return;
  panel.querySelectorAll('.kpi-value[data-target]').forEach(el => animateKPI(el));
}

// ── Score drill-down ─────────────────────────────────────────────
function showDrilldown(category) {
  const criteria = SCORE_CRITERIA[category];
  if (!criteria) return;
  const color = CAT_COLORS[category] || '#4f98a3';
  const label = { hvlp:'HVLP', boutique:'Boutique Fitness', digital:'Digital / Connected' }[category];

  document.getElementById('drilldown-title').textContent = `${label} — Score Breakdown`;

  const rows = Object.entries(criteria).map(([name, score]) => `
    <div class="drilldown-row">
      <div class="drilldown-label">${name}</div>
      <div class="drilldown-bar-track">
        <div class="drilldown-bar-fill" style="width:0%;background:${color}" data-width="${score*10}%"></div>
      </div>
      <div class="drilldown-score">${score}/10</div>
    </div>`).join('');

  document.getElementById('drilldown-body').innerHTML = rows;
  document.getElementById('score-drilldown').classList.remove('hidden');
  document.getElementById('backdrop').classList.remove('hidden');

  // Animate bars
  requestAnimationFrame(() => {
    document.querySelectorAll('.drilldown-bar-fill').forEach(bar => {
      bar.style.width = bar.dataset.width;
    });
  });
}

document.getElementById('drilldown-close')?.addEventListener('click', closeDrilldown);
document.getElementById('backdrop')?.addEventListener('click', closeDrilldown);
function closeDrilldown() {
  document.getElementById('score-drilldown').classList.add('hidden');
  document.getElementById('backdrop').classList.add('hidden');
}

// Make scoring chart bars clickable for drill-down
function bindScoringClick() {
  const el = document.getElementById('chart-scoring');
  if (!el) return;
  el.on('plotly_click', data => {
    const pt = data.points[0];
    const label = (pt.label || pt.x || pt.y || '').toString().toLowerCase();
    if (label.includes('hvlp') || label.includes('planet') || label.includes('budget')) showDrilldown('hvlp');
    else if (label.includes('boutique')) showDrilldown('boutique');
    else if (label.includes('digital')) showDrilldown('digital');
  });
}

// ── Helpers ──────────────────────────────────────────────────────
function showError(elId, msg) {
  const el = document.getElementById(elId);
  if (el) el.innerHTML = `<div class="chart-error">Failed to load: ${msg}</div>`;
}

function plotChart(elId, figObj) {
  if (!figObj || !figObj.data) { showError(elId, 'empty response'); return; }
  Plotly.newPlot(elId, figObj.data, { ...PLOTLY_BASE, ...figObj.layout }, {
    responsive:true, displayModeBar:false,
  });
}

// ── Tab loader ───────────────────────────────────────────────────
async function loadTab(tab, force = false) {
  if (cache[tab] && !force) return;
  cache[tab] = true;
  if      (tab === 'overview')  await loadOverview();
  else if (tab === 'unit-econ') await loadUnitEcon();
  else if (tab === 'market')    await loadMarket();
  else if (tab === 'trends')    await loadTrends();
}

// ── Overview ─────────────────────────────────────────────────────
async function loadOverview() {
  try {
    const [sRes, scRes] = await Promise.all([
      fetch('/api/stocks').then(r=>r.json()),
      fetch('/api/scoring').then(r=>r.json()),
    ]);
    plotChart('chart-stocks',  sRes.chart);
    plotChart('chart-scoring', scRes.chart);
    bindScoringClick();
    applyFilter(activeFilter);
  } catch(e) {
    showError('chart-stocks',  e.message);
    showError('chart-scoring', e.message);
  }
}

// ── Unit Economics ───────────────────────────────────────────────
async function loadUnitEcon() {
  try {
    const res = await fetch('/api/unit-economics').then(r=>r.json());
    plotChart('chart-unit-econ', res.chart);
    const rows = res.data || [];
    const tbody = document.getElementById('ue-tbody');
    if (!rows.length) { tbody.innerHTML='<tr><td colspan="6" class="table-loading">No data</td></tr>'; return; }
    tbody.innerHTML = rows.map(r=>`
      <tr>
        <td>${r.category??'—'}</td>
        <td>$${(r.cac??0).toLocaleString()}</td>
        <td>$${(r.ltv??0).toLocaleString()}</td>
        <td>${(r.ltv_cac??0).toFixed(1)}x</td>
        <td>${(r.gross_margin??0).toFixed(1)}%</td>
        <td>${r.payback_months??'—'} months</td>
      </tr>`).join('');
  } catch(e) { showError('chart-unit-econ', e.message); }
}

// ── Market Sizing ────────────────────────────────────────────────
async function loadMarket() {
  try {
    const res = await fetch('/api/market-sizing').then(r=>r.json());
    plotChart('chart-bubble', res.chart);
    const rows = res.data || [];
    const tbody = document.getElementById('market-tbody');
    if (!rows.length) { tbody.innerHTML='<tr><td colspan="5" class="table-loading">No data</td></tr>'; return; }
    tbody.innerHTML = rows.map(r=>`
      <tr>
        <td>${r.category??'—'}</td>
        <td>$${(r.tam_bn??0).toLocaleString()}B</td>
        <td>${(r.cagr??0).toFixed(1)}%</td>
        <td>$${(r.pe_capital_bn??0).toLocaleString()}B</td>
        <td>${(r.members_m??0).toLocaleString()}M</td>
      </tr>`).join('');
  } catch(e) { showError('chart-bubble', e.message); }
}

// ── Demand Trends ────────────────────────────────────────────────
async function loadTrends() {
  try {
    const res = await fetch('/api/trends').then(r=>r.json());
    if (res.error) { showError('chart-trends', res.error); return; }
    plotChart('chart-trends', res.chart);
  } catch(e) { showError('chart-trends', e.message); }
}

// ── Init ─────────────────────────────────────────────────────────
activateTab('overview');
loadTab('overview');
