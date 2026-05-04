/* dashboard/static/app.js
   Fetches JSON from FastAPI /api/* routes and renders Plotly charts.
   chart field from API is already a plain object — never JSON.parse() it.
*/

const COLORS = {
  hvlp:     '#4f98a3',
  boutique: '#e8af34',
  digital:  '#dd6974',
  muted:    '#797876',
  text:     '#cdccca',
  bg:       '#201f1d',
  grid:     '#262523',
};

const PLOTLY_BASE = {
  paper_bgcolor: '#201f1d',
  plot_bgcolor:  '#1c1b19',
  font:          { family: 'Satoshi, -apple-system, sans-serif', color: '#cdccca', size: 12 },
  margin:        { l: 52, r: 24, t: 16, b: 52 },
  legend:        { bgcolor: 'rgba(0,0,0,0)', borderwidth: 0, font: { size: 11 } },
  xaxis:         { gridcolor: '#262523', linecolor: '#262523', tickfont: { color: '#797876', size: 11 }, showgrid: false, zeroline: false },
  yaxis:         { gridcolor: '#262523', linecolor: '#262523', tickfont: { color: '#797876', size: 11 }, showgrid: true,  zeroline: false },
  hoverlabel:    { bgcolor: '#2d2c2a', bordercolor: '#393836', font: { size: 12, color: '#cdccca' } },
};

const cache = {};

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
  const titles = { overview: 'Overview', 'unit-econ': 'Unit Economics', market: 'Market Sizing', trends: 'Demand Trends' };
  document.querySelector('.topbar-title').textContent = titles[tab] || tab;
}

// ── Initial load ─────────────────────────────────────────────────
activateTab('overview');
loadTab('overview');
document.getElementById('last-updated-ts').textContent = new Date().toLocaleDateString('en-GB', { day:'2-digit', month:'short', year:'numeric' });

// ── Refresh button ───────────────────────────────────────────────
document.getElementById('btn-refresh').addEventListener('click', async () => {
  Object.keys(cache).forEach(k => delete cache[k]);
  const btn = document.getElementById('btn-refresh');
  btn.textContent = 'Refreshing…';
  btn.disabled = true;
  await fetch('/api/refresh');
  const active = document.querySelector('.nav-item.active')?.dataset.tab || 'overview';
  await loadTab(active, true);
  btn.innerHTML = `<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="23 4 23 10 17 10"/><path d="M20.49 15a9 9 0 1 1-2.12-9.36L23 10"/></svg> Refresh`;
  btn.disabled = false;
  document.getElementById('last-updated-ts').textContent = new Date().toLocaleString('en-GB', { day:'2-digit', month:'short', year:'numeric', hour:'2-digit', minute:'2-digit' });
});

// ── Tab loader ───────────────────────────────────────────────────
async function loadTab(tab, force = false) {
  if (cache[tab] && !force) return;
  cache[tab] = true;
  if      (tab === 'overview')  await loadOverview();
  else if (tab === 'unit-econ') await loadUnitEcon();
  else if (tab === 'market')    await loadMarket();
  else if (tab === 'trends')    await loadTrends();
}

// ── Helpers ──────────────────────────────────────────────────────
function showError(elId, msg) {
  const el = document.getElementById(elId);
  if (el) el.innerHTML = `<div class="chart-error">Failed to load: ${msg}</div>`;
}

function plotChart(elId, figObj) {
  /* figObj is the Python dict returned by charts.py, already deserialised by
     the browser's fetch().json() — just pass data + layout to Plotly directly */
  if (!figObj || !figObj.data) { showError(elId, 'empty response'); return; }
  Plotly.newPlot(elId, figObj.data, { ...PLOTLY_BASE, ...figObj.layout }, {
    responsive:     true,
    displayModeBar: false,
  });
}

// ── Overview ─────────────────────────────────────────────────────
async function loadOverview() {
  try {
    const [sRes, scRes] = await Promise.all([
      fetch('/api/stocks').then(r => r.json()),
      fetch('/api/scoring').then(r => r.json()),
    ]);
    plotChart('chart-stocks',  sRes.chart);
    plotChart('chart-scoring', scRes.chart);
  } catch (e) {
    showError('chart-stocks',  e.message);
    showError('chart-scoring', e.message);
  }
}

// ── Unit Economics ───────────────────────────────────────────────
async function loadUnitEcon() {
  try {
    const res = await fetch('/api/unit-economics').then(r => r.json());
    plotChart('chart-unit-econ', res.chart);

    const rows = res.data || [];
    const tbody = document.getElementById('ue-tbody');
    if (!rows.length) { tbody.innerHTML = '<tr><td colspan="6" style="text-align:center;padding:2rem;color:var(--color-text-muted)">No data</td></tr>'; return; }
    tbody.innerHTML = rows.map(r => `
      <tr>
        <td>${r.category ?? '—'}</td>
        <td>$${(r.cac ?? 0).toLocaleString()}</td>
        <td>$${(r.ltv ?? 0).toLocaleString()}</td>
        <td>${(r.ltv_cac ?? 0).toFixed(1)}x</td>
        <td>${(r.gross_margin ?? 0).toFixed(1)}%</td>
        <td>${r.payback_months ?? '—'} months</td>
      </tr>`).join('');
  } catch (e) {
    showError('chart-unit-econ', e.message);
  }
}

// ── Market Sizing ────────────────────────────────────────────────
async function loadMarket() {
  try {
    const res = await fetch('/api/market-sizing').then(r => r.json());
    plotChart('chart-bubble', res.chart);

    const rows = res.data || [];
    const tbody = document.getElementById('market-tbody');
    if (!rows.length) { tbody.innerHTML = '<tr><td colspan="5" style="text-align:center;padding:2rem;color:var(--color-text-muted)">No data</td></tr>'; return; }
    tbody.innerHTML = rows.map(r => `
      <tr>
        <td>${r.category ?? '—'}</td>
        <td>$${(r.tam_bn ?? 0).toLocaleString()}B</td>
        <td>${(r.cagr ?? 0).toFixed(1)}%</td>
        <td>$${(r.pe_capital_bn ?? 0).toLocaleString()}B</td>
        <td>${(r.members_m ?? 0).toLocaleString()}M</td>
      </tr>`).join('');
  } catch (e) {
    showError('chart-bubble', e.message);
  }
}

// ── Demand Trends ────────────────────────────────────────────────
async function loadTrends() {
  try {
    const res = await fetch('/api/trends').then(r => r.json());
    if (res.error) { showError('chart-trends', res.error); return; }
    plotChart('chart-trends', res.chart);
  } catch (e) {
    showError('chart-trends', e.message);
  }
}
