// ── State ────────────────────────────────────────────────────────
const state = { activeTab: 'overview', refreshing: false };

// ── Tab navigation ───────────────────────────────────────────────
function switchTab(tabId) {
  document.querySelectorAll('.nav-item').forEach(el => {
    el.classList.toggle('active', el.dataset.tab === tabId);
  });
  document.querySelectorAll('.tab-panel').forEach(el => {
    el.classList.toggle('active', el.id === `tab-${tabId}`);
  });
  document.querySelector('.topbar-title').textContent =
    document.querySelector(`[data-tab="${tabId}"]`)?.textContent.trim() || 'Dashboard';
  state.activeTab = tabId;
  loadTab(tabId);
}

// ── Plotly chart renderer ────────────────────────────────────────
function renderChart(containerId, chartJson) {
  if (!chartJson) return;
  const container = document.getElementById(containerId);
  if (!container) return;
  try {
    const spec = JSON.parse(chartJson);
    Plotly.newPlot(container, spec.data, spec.layout, {
      responsive: true,
      displayModeBar: false,
    });
  } catch (e) {
    container.innerHTML = `<div style="color:#f85149;padding:1rem;font-size:0.8rem;">Chart error: ${e.message}</div>`;
  }
}

function showSkeleton(containerId) {
  const el = document.getElementById(containerId);
  if (el) el.innerHTML = '<div class="chart-skeleton"></div>';
}

function showError(containerId, msg) {
  const el = document.getElementById(containerId);
  if (el) el.innerHTML = `<div style="display:flex;align-items:center;justify-content:center;height:200px;color:var(--color-text-muted);font-size:var(--text-sm);">${msg}</div>`;
}

// ── API fetchers ─────────────────────────────────────────────────
async function fetchJSON(url) {
  const res = await fetch(url);
  if (!res.ok) throw new Error(`HTTP ${res.status}`);
  return res.json();
}

async function loadOverview() {
  showSkeleton('chart-stocks');
  showSkeleton('chart-scoring');
  try {
    const [stocksData, scoringData] = await Promise.all([
      fetchJSON('/api/stocks'),
      fetchJSON('/api/scoring'),
    ]);
    renderChart('chart-stocks',  stocksData.chart);
    renderChart('chart-scoring', scoringData.chart);
    updateLastUpdated(stocksData.last_updated);

    // Update KPI score badges
    const scores = scoringData.scores;
    ['HVLP', 'Boutique', 'Digital'].forEach(cat => {
      const el = document.getElementById(`score-${cat.toLowerCase()}`);
      if (el && scores[cat]) el.textContent = `${scores[cat]}/10`;
    });
  } catch (e) {
    showError('chart-stocks',  `Failed to load stock data: ${e.message}`);
    showError('chart-scoring', `Failed to load scoring data: ${e.message}`);
  }
}

async function loadUnitEcon() {
  showSkeleton('chart-unit-econ');
  try {
    const data = await fetchJSON('/api/unit-economics');
    renderChart('chart-unit-econ', data.chart);

    // Populate table
    const tbody = document.getElementById('ue-tbody');
    if (tbody && data.data) {
      tbody.innerHTML = Object.entries(data.data).map(([cat, d]) => `
        <tr>
          <td><div class="cell-cat">
            <span class="cat-dot" style="background:var(--color-${cat.toLowerCase()})"></span>
            ${cat}
          </div></td>
          <td>$${d.CAC}</td>
          <td>$${d.LTV.toLocaleString()}</td>
          <td>${d.LTV_CAC}x</td>
          <td>${d.Gross_Margin}%</td>
          <td>${d.Payback_Mos} months</td>
        </tr>`).join('');
    }
  } catch (e) {
    showError('chart-unit-econ', `Failed to load unit economics: ${e.message}`);
  }
}

async function loadMarket() {
  showSkeleton('chart-bubble');
  try {
    const data = await fetchJSON('/api/market-sizing');
    renderChart('chart-bubble', data.chart);

    const tbody = document.getElementById('market-tbody');
    if (tbody && data.data) {
      tbody.innerHTML = Object.entries(data.data).map(([cat, d]) => `
        <tr>
          <td><div class="cell-cat">
            <span class="cat-dot" style="background:var(--color-${cat.toLowerCase()})"></span>
            ${cat}
          </div></td>
          <td>$${d.TAM_B}B</td>
          <td>${d.CAGR}%</td>
          <td>$${d.PE_Capital_B}B</td>
          <td>${d.Members_M}M</td>
        </tr>`).join('');
    }
  } catch (e) {
    showError('chart-bubble', `Failed to load market data: ${e.message}`);
  }
}

async function loadTrends() {
  showSkeleton('chart-trends');
  try {
    const data = await fetchJSON('/api/trends');
    if (data.error) {
      showError('chart-trends', `Trends data unavailable — run notebook 07 first to generate google_trends.csv`);
    } else {
      renderChart('chart-trends', data.chart);
    }
  } catch (e) {
    showError('chart-trends', `Failed to load trends: ${e.message}`);
  }
}

// ── Tab loader dispatcher ─────────────────────────────────────────
const tabLoaders = {
  overview:      loadOverview,
  'unit-econ':   loadUnitEcon,
  market:        loadMarket,
  trends:        loadTrends,
};

const loaded = new Set();
function loadTab(tabId) {
  if (loaded.has(tabId)) return;
  loaded.add(tabId);
  tabLoaders[tabId]?.();
}

// ── Refresh button ────────────────────────────────────────────────
async function handleRefresh() {
  if (state.refreshing) return;
  state.refreshing = true;
  const btn = document.getElementById('btn-refresh');
  btn.classList.add('spinning');
  btn.disabled = true;
  loaded.clear();
  try {
    await fetchJSON('/api/refresh');
    loadTab(state.activeTab);
  } catch (e) {
    console.error('Refresh failed:', e);
  } finally {
    state.refreshing = false;
    btn.classList.remove('spinning');
    btn.disabled = false;
  }
}

// ── Last updated ─────────────────────────────────────────────────
function updateLastUpdated(ts) {
  const el = document.getElementById('last-updated-ts');
  if (el && ts) el.textContent = ts;
}

// ── Init ─────────────────────────────────────────────────────────
document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('.nav-item[data-tab]').forEach(el => {
    el.addEventListener('click', () => switchTab(el.dataset.tab));
  });
  document.getElementById('btn-refresh')?.addEventListener('click', handleRefresh);
  switchTab('overview');
});
