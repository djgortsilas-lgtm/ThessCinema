import json
from datetime import datetime

with open('snapshot.json', 'r', encoding='utf-8') as f:
    movies = json.load(f)

snapshot_date = datetime.now().strftime('%d/%m/%Y %H:%M')
data_json = json.dumps(movies, ensure_ascii=False)

css = """*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
:root{--bg:#fef9f0;--surface:#ffffff;--surface2:#fdf3e7;--primary:#e85d5d;--accent:#f5a623;--text:#2d2d2d;--text2:#888;--border:#f0e6d8;--rating-bg:#f5a623;--rating-color:#fff;--radius:12px;--shadow:0 2px 12px rgba(0,0,0,0.06)}
body{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;background:var(--bg);color:var(--text);line-height:1.6;min-height:100vh}
a{color:#e85d5d;text-decoration:none}
a:hover{color:#d04444;text-decoration:underline}
header{background:var(--surface);border-bottom:1px solid var(--border);padding:12px 16px;position:sticky;top:0;z-index:100;box-shadow:var(--shadow)}
.header-inner{max-width:1400px;margin:0 auto;display:flex;align-items:center;gap:20px;flex-wrap:wrap}
header h1{font-size:22px;margin:0}
header h1 a{color:var(--primary);text-decoration:none}
nav{display:flex;gap:4px;flex:1;flex-wrap:wrap}
.tab{background:transparent;color:var(--text2);border:1px solid transparent;padding:8px 16px;border-radius:8px;cursor:pointer;font-size:14px;transition:all 0.2s}
.tab:hover{background:var(--surface2);color:var(--text)}
.tab.active{background:var(--accent);color:#fff;border-color:var(--accent)}
.header-actions{display:flex;align-items:center;gap:10px;margin-left:auto}
.last-update{font-size:12px;color:var(--text2)}
#refreshBtn{background:var(--surface2);border:1px solid var(--border);color:var(--text);padding:6px 14px;border-radius:8px;cursor:pointer;font-size:13px;transition:all 0.2s}
#refreshBtn:hover{background:var(--accent);color:#fff;border-color:var(--accent)}
#refreshBtn:disabled{opacity:.5;cursor:wait}
#refreshStatus{font-size:11px;color:#e85d5d;display:none}
.server-panel{background:var(--surface);border:2px dashed var(--accent);border-radius:var(--radius);padding:20px;margin-bottom:20px;text-align:center}
.server-panel h3{color:var(--accent);margin-bottom:8px}
.server-panel code{display:block;background:var(--surface2);padding:10px 14px;border-radius:6px;margin:10px 0;font-size:13px;color:var(--text)}
.server-panel .note{font-size:13px;color:var(--text2);margin-top:8px}
main{max-width:1400px;margin:0 auto;padding:20px 16px}
.movies-grid{display:flex;flex-direction:column;gap:12px}
.movie-card{background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);overflow:hidden;transition:all 0.2s;box-shadow:var(--shadow)}
.movie-card:hover{border-color:var(--accent);box-shadow:0 4px 20px rgba(245,166,35,0.15)}
.movie-card-inner{display:flex;gap:16px;padding:16px}
.movie-poster{flex-shrink:0;width:100px}
.movie-poster img{width:100px;height:auto;border-radius:6px;display:block}
.movie-info{flex:1;min-width:0}
.movie-info h2{font-size:18px;margin-bottom:4px}
.movie-info h2 a{color:var(--text)}
.movie-info h2 a:hover{color:var(--primary);text-decoration:none}
.movie-meta{font-size:13px;color:var(--text2);margin-bottom:6px}
.imdb-badge{display:inline-block;background:var(--rating-bg);color:var(--rating-color);padding:1px 8px;border-radius:4px;font-weight:700;font-size:12px;margin-right:6px}
.genre-tag{display:inline-block;background:#fdf3e7;color:#b87333;padding:1px 8px;border-radius:4px;font-size:12px;margin:1px 2px}
.movie-desc{font-size:14px;color:var(--text2);margin:6px 0;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden}
.movie-cinemas{display:flex;flex-wrap:wrap;gap:4px;margin-top:6px}
.cinema-chip{display:inline-block;background:#fff5e6;color:#b87333;border:1px solid #f0dcc0;padding:2px 10px;border-radius:12px;font-size:12px}
.showtimes-panel{border-top:1px solid var(--border);padding:12px 16px;background:var(--surface2);display:none}
.showtimes-panel.open{display:block}
.cinema-showtimes{margin-bottom:10px}
.cinema-showtimes h4{font-size:14px;margin-bottom:4px;color:#e85d5d}
.hall-table{width:100%;border-collapse:collapse;font-size:12px;margin-bottom:8px}
.hall-table th,.hall-table td{padding:4px 6px;border:1px solid var(--border);text-align:center;vertical-align:top}
.hall-table th{background:#fdf3e7;color:#666;font-weight:600}
.hall-table td .time-slot{display:inline-block;background:#f5a623;color:#fff;padding:2px 8px;border-radius:4px;margin:1px;font-size:11px}
.hall-table td.empty{color:#ccc}
.timeline-header{position:sticky;top:60px;z-index:50;background:var(--bg);padding:8px 0;display:flex;gap:8px;overflow-x:auto;margin-bottom:16px}
.day-pill{background:var(--surface);border:1px solid var(--border);padding:8px 16px;border-radius:20px;cursor:pointer;font-size:13px;white-space:nowrap;color:var(--text2);transition:all 0.2s;box-shadow:var(--shadow)}
.day-pill.active{background:var(--accent);color:#fff;border-color:var(--accent)}
.day-pill:hover{border-color:var(--accent)}
.timeline-day-content{padding:0 4px}
.timeline-cinema-section{background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);margin-bottom:12px;overflow:hidden}
.timeline-cinema-title{font-size:15px;padding:10px 14px;background:var(--surface2);border-bottom:1px solid var(--border);color:#e85d5d}
.timeline-movie-entry{display:flex;flex-wrap:wrap;gap:6px;align-items:baseline;padding:10px 14px;border-bottom:1px solid var(--border);cursor:pointer;transition:background 0.15s}
.timeline-movie-entry:last-child{border-bottom:none}
.timeline-movie-entry:hover{background:var(--surface2)}
.timeline-movie-title{font-weight:600;font-size:14px;color:var(--text)}
.timeline-movie-hall{font-size:12px;color:var(--text2)}
.timeline-movie-times{margin-left:auto;font-size:13px;color:#e85d5d;white-space:nowrap}
.cinemas-list{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:16px}
.cinema-card{background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);padding:16px}
.cinema-card h3{font-size:16px;margin-bottom:8px;color:#e85d5d}
.cinema-card .addr{font-size:12px;color:var(--text2);margin-bottom:8px}
.cinema-movie{font-size:13px;padding:8px 0;border-bottom:1px solid var(--border)}
.cinema-movie:last-child{border:none}
.cinema-movie-title{font-weight:600;color:var(--text);white-space:nowrap}
.cinema-movie-days{margin-top:2px;display:flex;flex-direction:column;gap:2px;width:100%}
.cinema-day-line{display:flex;flex-wrap:wrap;align-items:baseline;gap:4px}
.cinema-day{color:#b87333;font-weight:600;font-size:12px}
.cinema-day-times{font-size:12px;color:#e85d5d}
footer{text-align:center;padding:24px;color:var(--text2);font-size:13px;border-top:1px solid var(--border);margin-top:40px}
@media(max-width:768px){
  .header-inner{flex-direction:column;align-items:stretch}
  nav{justify-content:center}
  .movie-card-inner{flex-direction:column;align-items:center;text-align:center}
  .movie-poster{width:80px}
  .movie-poster img{width:80px}
  .movie-cinemas{justify-content:center}
  .timeline-grid{grid-template-columns:120px 1fr}
}
"""

HTML = """<!DOCTYPE html>
<html lang="el">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>ThessCinema</title>
<style>""" + css + """</style>
</head>
<body>
<header>
<div class="header-inner">
<h1><a href="#">ThessCinema</a></h1>
<nav>
<button class="tab active" data-view="column">\u039b\u03af\u03c3\u03c4\u03b1 \u03a4\u03b1\u03b9\u03bd\u03b9\u03ce\u03bd</button>
<button class="tab" data-view="timeline">\u03a7\u03c1\u03bf\u03bd\u03bf\u03bb\u03cc\u03b3\u03b9\u03bf</button>
<button class="tab" data-view="cinemas">\u0391\u03bd\u03ac \u0391\u03af\u03b8\u03bf\u03c5\u03c3\u03b1</button>
</nav>
<div class="header-actions">
<span class="last-update">""" + snapshot_date + """</span>
<button id="refreshBtn">\u0391\u03bd\u03b1\u03bd\u03ad\u03c9\u03c3\u03b7</button>
<span id="refreshStatus"></span>
</div>
</div>
</header>
<main><div id="content"></div></main>
<footer><p>&copy; 2026 ThessCinema</p></footer>
<script>
const MOVIES_DATA = """ + data_json + """;
const SNAPSHOT_DATE = \"""" + snapshot_date + """\";
const SHOWTIMES_CACHE = new Map();

const CORS_PROXIES = [
  'https://api.allorigins.win/raw?url=',
  'https://corsproxy.io/?url=',
];

// --- GitHub raw (for auto-refresh via GitHub Actions) ---
// Change these to match your repository:
const GITHUB_USER = 'YOUR_USERNAME';
const GITHUB_REPO = 'ThessCinema';
const GITHUB_DATA_URL = `https://raw.githubusercontent.com/${GITHUB_USER}/${GITHUB_REPO}/main/server/snapshot.json`;

function el(tag, attrs, ...children) {
  const e = document.createElement(tag);
  if (attrs) for (const [k, v] of Object.entries(attrs)) {
    if (k === 'className') e.className = v;
    else if (k === 'textContent') e.textContent = v;
    else if (k === 'innerHTML') e.innerHTML = v;
    else if (k.startsWith('on')) e.addEventListener(k.slice(2).toLowerCase(), v);
    else e.setAttribute(k, v);
  }
  for (const c of children) if (c != null) e.append(typeof c === 'string' ? document.createTextNode(c) : c);
  return e;
}

function esc(s) { const d = document.createElement('div'); d.textContent = s; return d.innerHTML; }
function summerIcon(name) { return name.includes('\u0398\u03b5\u03c1\u03b9\u03bd\u03cc\u03c2') ? '\u2600\uFE0F ' + name : name; }

function renderShowtimes(panel, cinemas) {
  if (!cinemas.length) { panel.append(el('p',{style:'color:var(--text2);font-size:13px'},'\u0394\u03b5\u03bd \u03c5\u03c0\u03ac\u03c1\u03c7\u03bf\u03c5\u03bd \u03c0\u03c1\u03bf\u03b2\u03bf\u03bb\u03ad\u03c2 \u03b3\u03b9\u03b1 \u03b1\u03c5\u03c4\u03ae \u03c4\u03b7\u03bd \u03b5\u03b2\u03b4\u03bf\u03bc\u03ac\u03b4\u03b1.')); return; }
  for (const c of cinemas) {
    const block = el('div',{className:'cinema-showtimes'},
      el('h4',{},summerIcon(c.name)),
      c.address ? el('div',{style:'font-size:11px;color:var(--text2);margin-bottom:4px'},c.address) : null
    );
    for (const hall of (c.halls||[])) {
      if (!hall.days || !hall.days.length) continue;
      const table = el('table',{className:'hall-table'});
      const thead = el('tr');
      for (const d of hall.days) thead.append(el('th',{},d));
      table.append(thead);
      for (const rowTimes of (hall.showtimes||[])) {
        const tr = el('tr');
        for (let i = 0; i < Math.max(hall.days.length, rowTimes.length); i++) {
          const times = rowTimes[i] || [];
          if (!times.length) { tr.append(el('td',{className:'empty'},'\u2014')); }
          else { const td = el('td',{}); for (const t of times) td.append(el('span',{className:'time-slot'},t)); tr.append(td); }
        }
        table.append(tr);
      }
      block.append(table);
    }
    panel.append(block);
  }
}

function renderColumnView(data) {
  data = data || MOVIES_DATA;
  const container = el('div',{className:'movies-grid'});
  for (const m of data) {
    const ps = m.poster && !m.poster.includes('data:image') ? m.poster : '';
    const gens = (m.genres||[]).slice(0,4).map(g => el('span',{className:'genre-tag'},g));
    const chips = (m.cinemas||[]).map(c => el('span',{className:'cinema-chip'},summerIcon(c.name)));
    const imdbH = m.imdb ? '<span class="imdb-badge">IMDb '+esc(m.imdb)+'</span>' : '';
    const panel = el('div',{className:'showtimes-panel'});
    const btn = el('button',{className:'showtimes-toggle',style:'background:none;border:none;color:#e85d5d;cursor:pointer;font-size:13px;margin-top:6px;padding:2px 0;font-weight:600'},'\u03ce\u03c1\u03b5\u03c2 \u03a0\u03c1\u03bf\u03b2\u03bf\u03bb\u03ce\u03bd \u25bc');
    let open = false;
    btn.onclick = async () => {
      open = !open;
      panel.classList.toggle('open', open);
      btn.textContent = open ? '\u03ce\u03c1\u03b5\u03c2 \u03a0\u03c1\u03bf\u03b2\u03bf\u03bb\u03ce\u03bd \u25b2' : '\u03ce\u03c1\u03b5\u03c2 \u03a0\u03c1\u03bf\u03b2\u03bf\u03bb\u03ce\u03bd \u25bc';
      if (open && !panel.hasChildNodes()) {
        let st = m.showtimes;
        if ((!st || !st.length) && m.detail_url) {
          if (SHOWTIMES_CACHE.has(m.detail_url)) {
            st = SHOWTIMES_CACHE.get(m.detail_url);
          } else {
            btn.textContent = '\u03a6\u03cc\u03c1\u03c4\u03c9\u03c3\u03b7...';
            st = await fetchShowtimesForMovie(m.detail_url);
            if (st) { SHOWTIMES_CACHE.set(m.detail_url, st); m.showtimes = st; }
          }
        }
        renderShowtimes(panel, st||[]);
      }
    };
    const card = el('div',{className:'movie-card'},
      el('div',{className:'movie-card-inner'},
        el('div',{className:'movie-poster'}, ps ? el('img',{src:ps,alt:m.title,loading:'lazy'}) : el('span',{className:'genre-tag'},'No Poster')),
        el('div',{className:'movie-info'},
          el('h2',{}, m.title),
          el('div',{className:'movie-meta',innerHTML:imdbH+(m.year?' <span>'+esc(m.year)+'</span>':'')}),
          el('div',{className:'movie-meta'},...gens),
          m.description ? el('div',{className:'movie-desc'},m.description) : null,
          el('div',{className:'movie-cinemas'},...chips),
          btn
        )
      ),
      panel
    );
    container.append(card);
  }
  return container;
}

function getTimesForMovieDay(movie, dayLabel) {
  const result = [];
  for (const c of (movie.showtimes||[])) {
    for (const hall of (c.halls||[])) {
      const dayIdx = (hall.days||[]).findIndex(d => d.includes(dayLabel));
      if (dayIdx < 0) continue;
      const times = new Set();
      for (const row of (hall.showtimes||[])) {
        if (row[dayIdx] && row[dayIdx].length) for (const t of row[dayIdx]) times.add(t);
      }
      if (times.size) result.push({cinema: c.name, hall: hall.name, times: [...times]});
    }
  }
  return result;
}

function renderTimelineView() {
  const container = el('div',{});
  const dayHeader = el('div',{className:'timeline-header'});
  const dAbbrs = ['\u0394\u03b5','\u03a4\u03c1','\u03a4\u03b5','\u03a0\u03b5','\u03a0\u03b1','\u03a3\u03b1','\u039a\u03c5'];
  const today = new Date();
  const weekDays = [];
  for (let i = 0; i < 7; i++) {
    const d = new Date(today); d.setDate(today.getDate() + i);
    const idx = d.getDay() === 0 ? 6 : d.getDay() - 1;
    weekDays.push({date:d, abbr:dAbbrs[idx], label:dAbbrs[idx]+' '+d.getDate()+'/'+(d.getMonth()+1)});
  }
  let activeDay = 0;
  function buildDayContent(dayIdx) {
    const dayLabel = weekDays[dayIdx].abbr;
    const wrapper = el('div',{className:'timeline-day-content'});
    const cinemaMap = {};
    for (const m of MOVIES_DATA) {
      const entries = getTimesForMovieDay(m, dayLabel);
      for (const e of entries) {
        if (!cinemaMap[e.cinema]) cinemaMap[e.cinema] = [];
        cinemaMap[e.cinema].push({title:m.title, hall:e.hall, times:e.times, movie:m});
      }
    }
    if (!Object.keys(cinemaMap).length) {
      wrapper.append(el('p',{style:'color:var(--text2);text-align:center;padding:24px'},'\u0394\u03b5\u03bd \u03c5\u03c0\u03ac\u03c1\u03c7\u03bf\u03c5\u03bd \u03c0\u03c1\u03bf\u03b2\u03bf\u03bb\u03ad\u03c2 \u03b3\u03b9\u03b1 \u03b1\u03c5\u03c4\u03ae \u03c4\u03b7\u03bd \u03b7\u03bc\u03ad\u03c1\u03b1.'));
      return wrapper;
    }
    for (const [cn, items] of Object.entries(cinemaMap).sort()) {
      const section = el('div',{className:'timeline-cinema-section'},
        el('h3',{className:'timeline-cinema-title'},summerIcon(cn))
      );
      for (const item of items) {
        const entry = el('div',{className:'timeline-movie-entry'});
        entry.append(el('span',{className:'timeline-movie-title'},item.title));
        if (item.hall !== '\u0391\u03af\u03b8\u03bf\u03c5\u03c3\u03b1') entry.append(el('span',{className:'timeline-movie-hall'},'('+item.hall+')'));
        entry.append(el('span',{className:'timeline-movie-times'},item.times.join(', ')));
        entry.onclick = () => { document.querySelectorAll('.tab')[0].click(); setTimeout(()=>{for(const card of document.querySelectorAll('.movie-card')){if(card.textContent.includes(item.title)){card.scrollIntoView({behavior:'smooth',block:'center'});const b=card.querySelector('.showtimes-toggle');if(b)b.click();break}}},100) };
        section.append(entry);
      }
      wrapper.append(section);
    }
    return wrapper;
  }
  for (let i = 0; i < weekDays.length; i++) {
    const pill = el('button',{className:'day-pill'+(i===activeDay?' active':''),textContent:weekDays[i].label});
    pill.onclick = () => { dayHeader.querySelectorAll('.day-pill').forEach(p=>p.classList.remove('active')); pill.classList.add('active'); activeDay = i; const old=container.querySelector('.timeline-day-content'); if(old) old.remove(); container.append(buildDayContent(activeDay)); };
    dayHeader.append(pill);
  }
  container.append(dayHeader);
  container.append(buildDayContent(0));
  return container;
}

function getShowtimesForCinema(movie, cinemaName) {
  const st = (movie.showtimes||[]).find(c => c.name === cinemaName);
  if (!st || !st.halls || !st.halls.length) return null;
  const dayMap = {};
  for (const hall of st.halls) {
    const days = hall.days || [];
    const rows = hall.showtimes || [];
    for (let di = 0; di < days.length; di++) {
      if (!dayMap[days[di]]) dayMap[days[di]] = new Set();
      for (const row of rows) {
        if (row[di] && row[di].length) for (const t of row[di]) dayMap[days[di]].add(t);
      }
    }
  }
  return dayMap;
}

function renderCinemasView() {
  const container = el('div',{className:'cinemas-list'});
  const cm = {};
  for (const m of MOVIES_DATA) {
    for (const c of (m.cinemas||[])) {
      if (!cm[c.name]) cm[c.name] = {name:c.name, entries:[]};
      cm[c.name].entries.push(m);
    }
  }
  for (const [name,data] of Object.entries(cm).sort()) {
    const card = el('div',{className:'cinema-card'},el('h3',{},summerIcon(name)));
    for (const m of data.entries) {
      const line = el('div',{className:'cinema-movie'});
      line.append(el('span',{className:'cinema-movie-title'},m.title));
      const dayMap = getShowtimesForCinema(m, name);
      const timesWrap = el('div',{className:'cinema-movie-days'});
      if (dayMap && Object.keys(dayMap).length) {
        for (const [dayLabel, times] of Object.entries(dayMap)) {
          const dayLine = el('div',{className:'cinema-day-line'});
          dayLine.append(el('span',{className:'cinema-day'},dayLabel + ': '));
          dayLine.append(el('span',{className:'cinema-day-times'},[...times].join(', ')));
          timesWrap.append(dayLine);
        }
      }
      line.append(timesWrap);
      card.append(line);
    }
    container.append(card);
  }
  return container;
}

// ---- Refresh logic ----

function setStatus(msg, isError) {
  const el = document.getElementById('refreshStatus');
  el.textContent = msg;
  el.style.display = 'inline';
  el.style.color = isError ? '#e94560' : '#4fc3f7';
  if (!isError) setTimeout(() => { el.style.display = 'none'; }, 4000);
}

async function tryFetch(url, timeoutMs) {
  const ctrl = new AbortController();
  const id = setTimeout(() => ctrl.abort(), timeoutMs);
  try {
    const r = await fetch(url, { signal: ctrl.signal });
    clearTimeout(id);
    if (!r.ok) throw new Error('HTTP '+r.status);
    return await r.text();
  } catch(e) {
    clearTimeout(id);
    throw e;
  }
}

async function fetchShowtimesForMovie(url) {
  const slug = url.split('/').filter(s=>s).pop();
  try {
    const txt = await tryFetch('http://localhost:8765/api/movies/'+slug, 5000);
    const data = JSON.parse(txt);
    if (data && data.cinemas && data.cinemas.length) return data.cinemas;
  } catch(e) { /* backend not available */ }
  // CORS proxy fallback (may not work with this site)
  let html = '';
  for (const proxy of CORS_PROXIES) {
    try { html = await tryFetch(proxy + encodeURIComponent(url), 15000); if (html.length > 2000) break; }
    catch(e) { continue; }
  }
  if (!html || html.length < 2000 || !html.includes('python-table')) return [];
  const doc = new DOMParser().parseFromString(html, 'text/html');
  const tables = doc.querySelectorAll('table.python-table.text-center');
  const cinemas = [];
  for (const table of tables) {
    const container = table.closest('.cine-table-sc') || table.parentElement;
    const prev = container?.previousElementSibling;
    const cinemaNameEl = prev?.querySelector('h4, h3, strong, .title') || prev;
    const cinemaName = cinemaNameEl ? cinemaNameEl.textContent.trim() : '\u0391\u03af\u03b8\u03bf\u03c5\u03c3\u03b1';
    const addrEl = prev?.querySelector('.address, .addr, [class*="address"], [class*="addr"], p');
    const address = addrEl ? addrEl.textContent.trim() : '';
    const cinema = { name: cinemaName, address, halls: [] };
    const tbody = table.querySelector('tbody');
    if (!tbody) continue;
    const rows = tbody.querySelectorAll('tr');
    if (rows.length < 2) continue;
    const dayCells = rows[1].querySelectorAll('th, td');
    let days = [...dayCells].map(c => c.textContent.trim()).filter(Boolean);
    if (!days.length) {
      for (let i = 0; i < (rows[0]?.querySelectorAll('th, td').length || 7); i++) days.push('\u0397\u03bc\u03ad\u03c1\u03b1 '+(i+1));
    }
    const hallGroups = [];
    let i = 0;
    while (i < rows.length) {
      const rowCells = rows[i].querySelectorAll('th, td');
      let hallName = '';
      let colspan = 0;
      for (const cell of rowCells) {
        const cs = parseInt(cell.getAttribute('colspan') || '1');
        colspan += cs;
        const txt = cell.textContent.trim();
        if (cs >= 4 && txt && !txt.match(/^\d{1,2}:\d{2}/)) hallName = txt;
      }
      if (colspan >= 4 && hallName) {
        const group = { name: hallName, rows: [] };
        i++;
        while (i < rows.length) {
          const nextCells = rows[i].querySelectorAll('td');
          if (nextCells.length < 4) break;
          const timeRow = [];
          for (const cell of nextCells) {
            const times = [...cell.querySelectorAll('span')].map(s => s.textContent.trim()).filter(t => t.match(/^\d{1,2}:\d{2}/));
            timeRow.push(times.length ? times : []);
          }
          group.rows.push(timeRow);
          i++;
        }
        hallGroups.push(group);
      } else {
        i++;
      }
    }
    if (!hallGroups.length && days.length) {
      const showtimes = [];
      for (let r = 2; r < rows.length; r++) {
        const timeRow = [];
        for (const cell of rows[r].querySelectorAll('td')) {
          const times = [...cell.querySelectorAll('span')].map(s => s.textContent.trim()).filter(t => t.match(/^\d{1,2}:\d{2}/));
          timeRow.push(times.length ? times : []);
        }
        if (timeRow.some(t => t.length)) showtimes.push(timeRow);
      }
      if (showtimes.length) cinema.halls.push({ name: '\u0391\u03af\u03b8\u03bf\u03c5\u03c3\u03b1', days, showtimes });
    } else {
      for (const g of hallGroups) cinema.halls.push({ name: g.name, days, showtimes: g.rows });
    }
    cinemas.push(cinema);
  }
  return cinemas;
}

function showServerHelp() {
  let panel = document.getElementById('serverHelp');
  if (panel) return;
  panel = el('div',{id:'serverHelp',className:'server-panel'},
    el('h3',{},'\u2600\uFE0F \u0391\u03bd\u03b1\u03bd\u03ad\u03c9\u03c3\u03b7 \u03b4\u03b5\u03b4\u03bf\u03bc\u03ad\u03bd\u03c9\u03bd'),
    el('p',{},'\u0397 \u03b6\u03c9\u03bd\u03c4\u03b1\u03bd\u03ae \u03b1\u03bd\u03b1\u03bd\u03ad\u03c9\u03c3\u03b7 \u03b1\u03c0\u03b1\u03b9\u03c4\u03b5\u03af \u03c4\u03bf Python backend \u03bd\u03b1 \u03c4\u03c1\u03ad\u03c7\u03b5\u03b9. \u039c\u03af\u03b1 \u03b1\u03c0\u03cc \u03c4\u03b9\u03c2 \u03b5\u03be\u03ae\u03c2 \u03b5\u03c0\u03b9\u03bb\u03bf\u03b3\u03ad\u03c2:'),
    el('div',{style:'display:flex;flex-wrap:wrap;gap:12px;justify-content:center;margin:12px 0'},
      el('code',{style:'flex:1;min-width:200px;font-size:13px'},'cd server && python -m uvicorn main:app --host 0.0.0.0 --port 8765'),
      el('span',{style:'font-size:13px;color:var(--text2);align-self:center'},'\u03ae'),
      el('code',{style:'font-size:13px'},'double-click start.bat')
    ),
    el('p',{className:'note'},'\u03a4\u03b1 \u03c0\u03c1\u03bf\u03b2\u03bf\u03bb\u03ad\u03c2 \u03b1\u03c0\u03cc \u03c4\u03bf \u03b5\u03bd\u03c3\u03c9\u03bc\u03b1\u03c4\u03c9\u03bc\u03ad\u03bd\u03bf \u03c3\u03c4\u03bf\u03b9\u03c7\u03b5\u03af\u03bf (\u03c3\u03ae\u03bc\u03b5\u03c1\u03b1) \u03b5\u03bc\u03c6\u03b1\u03bd\u03af\u03b6\u03bf\u03bd\u03c4\u03b1\u03b9 \u03ba\u03b1\u03bd\u03bf\u03bd\u03b9\u03ba\u03ac.')
  );
  document.getElementById('content').before(panel);
}

async function doRefresh() {
  const btn = document.getElementById('refreshBtn');
  const status = document.getElementById('refreshStatus');
  btn.disabled = true;
  status.textContent = '\u0391\u03bd\u03b1\u03bd\u03ad\u03c9\u03c3\u03b7...';
  status.style.display = 'inline';
  status.style.color = '#4fc3f7';
  try {
    let movies = null;
    // 1) Python backend
    try {
      const txt = await tryFetch('http://localhost:8765/api/rebuild', 120000);
      const data = JSON.parse(txt);
      if (data && data.movies && data.movies.length && data.movies[0].showtimes) { movies = data.movies; }
    } catch(e) {
      try {
        const txt = await tryFetch('http://localhost:8765/api/movies?refresh=1', 10000);
        const data = JSON.parse(txt);
        if (data && data.movies && data.movies.length && data.movies[0].showtimes) { movies = data.movies; }
      } catch(e2) { /* backend not available */ }
    }
    // 2) GitHub raw (works without server — data updated by GitHub Actions)
    if (!movies && GITHUB_USER !== 'YOUR_USERNAME') {
      try {
        const txt = await tryFetch(GITHUB_DATA_URL, 10000);
        const data = JSON.parse(txt);
        if (Array.isArray(data) && data.length && data[0].detail_url) { movies = data; }
      } catch(e) { /* github not available */ }
    }
    if (movies && movies.length > 0) {
      MOVIES_DATA.length = 0;
      SHOWTIMES_CACHE.clear();
      for (const m of movies) MOVIES_DATA.push(m);
      const now = new Date();
      const sd = now.getDate().toString().padStart(2,'0')+'/'+
                 ((now.getMonth()+1).toString().padStart(2,'0'))+'/'+
                 now.getFullYear()+' '+now.getHours().toString().padStart(2,'0')+':'+
                 now.getMinutes().toString().padStart(2,'0');
      document.querySelector('.last-update').textContent = sd;
      const activeTab = document.querySelector('.tab.active');
      if (activeTab) activeTab.click();
      setStatus('\u0391\u03bd\u03b1\u03bd\u03b5\u03ce\u03b8\u03b7\u03ba\u03b5! ('+movies.length+' \u03c4\u03b1\u03b9\u03bd\u03af\u03b5\u03c2)');
    } else {
      setStatus('\u0397 \u03b1\u03bd\u03b1\u03bd\u03ad\u03c9\u03c3\u03b7 \u03c7\u03c1\u03b5\u03b9\u03ac\u03b6\u03b5\u03c4\u03b1\u03b9 Python server \u2014 \u03ba\u03ac\u03bd\u03b5 double-click \u03c4\u03bf start.bat \u03ae \u03c4\u03c1\u03b5\u03be\u03b5: cd server && python -m uvicorn main:app --host 0.0.0.0 --port 8765', true);
      showServerHelp();
    }
  } catch(e) {
    setStatus('\u03a3\u03c6\u03ac\u03bb\u03bc\u03b1: '+e.message, true);
  } finally {
    btn.disabled = false;
  }
}

function init() {
  const content = document.getElementById('content');
  content.append(renderColumnView());
  document.querySelectorAll('.tab').forEach(tab => {
    tab.onclick = () => {
      document.querySelectorAll('.tab').forEach(t=>t.classList.remove('active'));
      tab.classList.add('active');
      content.innerHTML = '';
      const v = tab.dataset.view;
      if (v === 'column') content.append(renderColumnView());
      else if (v === 'timeline') content.append(renderTimelineView());
      else content.append(renderCinemasView());
    };
  });
  document.getElementById('refreshBtn').onclick = doRefresh;
}
init();
</script>
</body>
</html>"""

with open('ThessCinema.html', 'w', encoding='utf-8') as f:
    f.write(HTML)

# Also copy to static/ for the development server
import os
os.makedirs('static', exist_ok=True)
with open('static/index.html', 'w', encoding='utf-8') as f:
    f.write(HTML)

print(f'Created ThessCinema.html ({len(HTML)} bytes)')
