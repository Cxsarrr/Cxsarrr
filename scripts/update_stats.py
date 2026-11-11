#!/usr/bin/env python3
"""
scripts/update_stats.py
Genera los SVG del perfil de @Cxsarrr a partir de sus contribuciones reales:
  - assets/header.svg
  - assets/github-stats.svg
  - assets/spent-my-time.svg

Uso local con datos guardados:  python scripts/update_stats.py --data days.json
(days.json = lista de {"date": "YYYY-MM-DD", "count": n, "level": 0-4})
"""

import json
import os
import re
import sys
import urllib.request
from datetime import date, datetime, timedelta
from xml.sax.saxutils import escape

USERNAME = "Cxsarrr"
NAME = "Cesar Bolivar"
ROLE = "Desarrollador Full Stack"
TOKEN = os.environ.get("GH_PAT") or os.environ.get("GITHUB_TOKEN")

# Paleta azul (de oscuro a claro)
BG = "#0B121C"
PANEL = "#111B2A"
PANEL2 = "#15233A"
STROKE = "#22364F"
TEXT = "#F5F8FC"
MUTED = "#8C9BB0"
LEVELS = ["#152235", "#1F3A63", "#2F5A8A", "#4A90E2", "#ABCDEF"]
ACCENT = "#4A90E2"
LIGHT = "#ABCDEF"
MID = "#6FA8EA"

MESES = ["ene", "feb", "mar", "abr", "may", "jun", "jul", "ago", "sep", "oct", "nov", "dic"]
MESES_LARGO = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio",
               "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
DIAS = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
FONT = "-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif"
MONO = "ui-monospace,SFMono-Regular,Menlo,Consolas,monospace"

LEVEL_MAP = {"NONE": 0, "FIRST_QUARTILE": 1, "SECOND_QUARTILE": 2,
             "THIRD_QUARTILE": 3, "FOURTH_QUARTILE": 4}


# ----------------------------------------------------------------- datos
def fetch_graphql():
    if not TOKEN:
        return None
    query = """query($login:String!){user(login:$login){contributionsCollection{
      contributionCalendar{weeks{contributionDays{date contributionCount contributionLevel}}}}}}"""
    body = json.dumps({"query": query, "variables": {"login": USERNAME}}).encode()
    req = urllib.request.Request(
        "https://api.github.com/graphql", data=body,
        headers={"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json",
                 "User-Agent": "profile-stats"})
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            res = json.loads(r.read().decode())
        weeks = res["data"]["user"]["contributionsCollection"]["contributionCalendar"]["weeks"]
        return [{"date": d["date"], "count": d["contributionCount"],
                 "level": LEVEL_MAP.get(d["contributionLevel"], 0)}
                for w in weeks for d in w["contributionDays"]]
    except Exception as e:  # noqa: BLE001
        print(f"GraphQL falló: {e}")
        return None


def fetch_html():
    req = urllib.request.Request(f"https://github.com/users/{USERNAME}/contributions",
                                 headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=20) as r:
        html = r.read().decode()
    tips = dict(re.findall(r'<tool-tip[^>]*for="([^"]+)"[^>]*>\s*([^<]+?)\s*</tool-tip>', html))
    days = []
    for td in re.findall(r"<td\s+([^>]*data-date[^>]*)>", html):
        d = re.search(r'data-date="([\d-]+)"', td)
        lv = re.search(r'data-level="(\d)"', td)
        i = re.search(r'id="([^"]+)"', td)
        m = re.search(r"(\d+) contribution", tips.get(i.group(1) if i else "", ""))
        if d and lv:
            days.append({"date": d.group(1), "level": int(lv.group(1)),
                         "count": int(m.group(1)) if m else 0})
    return days


def load_days():
    if "--data" in sys.argv:
        with open(sys.argv[sys.argv.index("--data") + 1], encoding="utf-8") as f:
            return json.load(f)
    days = fetch_graphql()
    if not days:
        days = fetch_html()
    return days


# ----------------------------------------------------------------- cálculos
def fmt(d):
    return f"{d.day} {MESES[d.month - 1]}"


def streaks(days):
    ds = sorted(days, key=lambda x: x["date"])
    best = run = 0
    best_s = best_e = run_s = None
    for x in ds:
        if x["count"] > 0:
            run_s = run_s or x["date"]
            run += 1
            if run > best:
                best, best_s, best_e = run, run_s, x["date"]
        else:
            run, run_s = 0, None
    i = len(ds) - 1
    if i > 0 and ds[i]["count"] == 0:
        i -= 1
    cur, cur_s, cur_e = 0, None, ds[i]["date"] if ds else None
    while i >= 0 and ds[i]["count"] > 0:
        cur += 1
        cur_s = ds[i]["date"]
        i -= 1

    def rng(a, b):
        if not a:
            return "Sin racha activa"
        a, b = date.fromisoformat(a), date.fromisoformat(b)
        return fmt(a) if a == b else f"{fmt(a)} – {fmt(b)}"
    return cur, rng(cur_s, cur_e), best, rng(best_s, best_e)


def compute(days):
    days = sorted(days, key=lambda x: x["date"])
    total = sum(d["count"] for d in days)
    cur, cur_r, best, best_r = streaks(days)
    by_wd = [0] * 7
    by_month = {}
    for d in days:
        dt = date.fromisoformat(d["date"])
        by_wd[dt.weekday()] += d["count"]
        key = (dt.year, dt.month)
        by_month[key] = by_month.get(key, 0) + d["count"]
    active = sum(1 for d in days if d["count"] > 0)
    first = date.fromisoformat(days[0]["date"]) if days else date.today()
    return {"days": days, "total": total, "cur": cur, "cur_r": cur_r, "best": best,
            "best_r": best_r, "by_wd": by_wd, "by_month": by_month, "active": active,
            "first": first}


# ----------------------------------------------------------------- piezas SVG
def style(extra=""):
    return f"""<style>
  .s{{font-family:{FONT}}} .m{{font-family:{MONO}}}
  .fade{{animation:fade .9s ease backwards}}
  @keyframes fade{{from{{opacity:0;transform:translateY(8px)}}to{{opacity:1;transform:none}}}}
  @keyframes pulse{{0%,100%{{opacity:.55}}50%{{opacity:1}}}}
  @keyframes spin{{to{{transform:rotate(360deg)}}}}
  {extra}
</style>"""


def defs():
    return f"""<defs>
  <linearGradient id="gCard" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="#101A29"/><stop offset=".55" stop-color="{BG}"/><stop offset="1" stop-color="#0F1E33"/>
  </linearGradient>
  <radialGradient id="gGlow" cx=".85" cy=".1" r=".7">
    <stop offset="0" stop-color="{ACCENT}" stop-opacity=".22"/><stop offset="1" stop-color="{ACCENT}" stop-opacity="0"/>
  </radialGradient>
  <radialGradient id="gGlow2" cx=".1" cy="1" r=".6">
    <stop offset="0" stop-color="{LIGHT}" stop-opacity=".10"/><stop offset="1" stop-color="{LIGHT}" stop-opacity="0"/>
  </radialGradient>
  <linearGradient id="gRing" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="{LIGHT}"/><stop offset="1" stop-color="{ACCENT}"/>
  </linearGradient>
  <linearGradient id="gScan" x1="0" x2="1">
    <stop offset="0" stop-color="{LIGHT}" stop-opacity="0"/><stop offset=".5" stop-color="{LIGHT}" stop-opacity=".18"/><stop offset="1" stop-color="{LIGHT}" stop-opacity="0"/>
  </linearGradient>
</defs>"""


def card(w, h):
    return (f'<rect x="1" y="1" width="{w-2}" height="{h-2}" rx="28" fill="url(#gCard)" stroke="{STROKE}" stroke-width="2"/>'
            f'<rect x="1" y="1" width="{w-2}" height="{h-2}" rx="28" fill="url(#gGlow)"/>'
            f'<rect x="1" y="1" width="{w-2}" height="{h-2}" rx="28" fill="url(#gGlow2)"/>')


def donut(cx, cy, r, sw, parts, colors, center_big, center_small, delay=0.3):
    total = sum(parts) or 1
    circ = 2 * 3.14159265 * r
    out = [f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{LEVELS[0]}" stroke-width="{sw}"/>']
    off = 0.0
    for i, p in enumerate(parts):
        if p <= 0:
            continue
        seg = circ * p / total
        gap = 4 if seg > 8 else 0
        out.append(
            f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{colors[i % len(colors)]}" stroke-width="{sw}" '
            f'stroke-dasharray="{max(seg-gap,0.1):.2f} {circ:.2f}" stroke-dashoffset="{-off:.2f}" '
            f'transform="rotate(-90 {cx} {cy})" class="fade" style="animation-delay:{delay + i*0.12:.2f}s"/>')
        off += seg
    out.append(f'<text class="s" x="{cx}" y="{cy+8}" font-size="30" font-weight="700" fill="{TEXT}" text-anchor="middle">{center_big}</text>')
    out.append(f'<text class="s" x="{cx}" y="{cy+30}" font-size="13" fill="{MUTED}" text-anchor="middle">{escape(center_small)}</text>')
    return "\n".join(out)


def legend_rows(x, y, rows, colors, w):
    out = []
    for i, (label, pct) in enumerate(rows):
        yy = y + i * 34
        out.append(f'<circle cx="{x+6}" cy="{yy-5}" r="6" fill="{colors[i % len(colors)]}"/>')
        out.append(f'<text class="s" x="{x+22}" y="{yy}" font-size="15" fill="{TEXT}">{escape(label)}</text>')
        out.append(f'<text class="s" x="{x+w}" y="{yy}" font-size="15" fill="{MUTED}" text-anchor="end">{pct}%</text>')
    return "\n".join(out)


def pct_rows(pairs, n=5):
    tot = sum(v for _, v in pairs) or 1
    pairs = sorted(pairs, key=lambda x: -x[1])
    top = pairs[:n - 1] if len(pairs) > n else pairs
    rest = sum(v for _, v in pairs[n - 1:]) if len(pairs) > n else 0
    rows = [(k, v) for k, v in top]
    if rest:
        rows.append(("Otros", rest))
    pcts = [round(v * 100 / tot) for _, v in rows]
    return [(k, p) for (k, _), p in zip(rows, pcts)], [v for _, v in rows]


# ----------------------------------------------------------------- header.svg
def build_header():
    W, H = 1600, 380
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
{style(".blink{animation:pulse 1.6s infinite} .dot{animation:pulse 2.4s infinite}")}
{defs()}
{card(W, H)}
<g opacity=".18" stroke="{STROKE}">{''.join(f'<line x1="{x}" y1="70" x2="{x}" y2="{H-2}"/>' for x in range(80, W, 80))}</g>
<line x1="2" y1="70" x2="{W-2}" y2="70" stroke="{STROKE}" stroke-width="2"/>
<circle cx="48" cy="36" r="8" fill="#3A4D66"/><circle cx="76" cy="36" r="8" fill="#3A4D66"/><circle cx="104" cy="36" r="8" fill="{ACCENT}"/>
<text class="m" x="136" y="42" font-size="17" fill="{MUTED}">cesar@dev:~/workspace <tspan fill="{LIGHT}">[main]</tspan></text>
<rect x="{W-350}" y="16" width="310" height="40" rx="20" fill="{PANEL2}" stroke="{ACCENT}" stroke-opacity=".6" stroke-width="1.5"/>
<circle cx="{W-324}" cy="36" r="11" fill="{LIGHT}" opacity=".18" class="dot"/>
<circle cx="{W-324}" cy="36" r="5" fill="{LIGHT}"/>
<text class="s" x="{W-306}" y="42" font-size="16" font-weight="600" fill="{TEXT}">Abierto a oportunidades ✦</text>
<g class="fade" style="animation-delay:.1s">
  <rect x="72" y="140" width="28" height="3" fill="{ACCENT}"/>
  <text class="m" x="116" y="148" font-size="18" letter-spacing="4" fill="{LIGHT}">FULL STACK DEVELOPER</text>
</g>
<g class="fade" style="animation-delay:.3s">
  <text class="s" x="70" y="238" font-size="84" font-weight="800" fill="{TEXT}" letter-spacing="-1">{NAME}<tspan class="blink" fill="{ACCENT}">_</tspan></text>
</g>
<g class="fade" style="animation-delay:.5s">
  <text class="s" x="72" y="296" font-size="26" font-weight="500" fill="{MUTED}">Django · Next.js · React · TypeScript · PostgreSQL</text>
</g>
<g transform="translate(1196 104)" class="fade" style="animation-delay:.7s">
  <rect width="340" height="236" rx="18" fill="{PANEL}" stroke="{STROKE}" stroke-width="1.5"/>
  <rect width="340" height="40" rx="18" fill="{PANEL2}"/><rect y="22" width="340" height="18" fill="{PANEL2}"/>
  <line x1="0" y1="40" x2="340" y2="40" stroke="{STROKE}"/>
  <circle cx="22" cy="20" r="5" fill="#3A4D66"/><circle cx="40" cy="20" r="5" fill="#3A4D66"/><circle cx="58" cy="20" r="5" fill="{ACCENT}"/>
  <text class="m" x="80" y="25" font-size="14" fill="{MUTED}">cesar.ts</text>
  <text class="m" x="22" y="74" font-size="16" fill="{LIGHT}">const <tspan fill="{TEXT}">cesar</tspan> <tspan fill="{MUTED}">=</tspan> {{</text>
  <text class="m" x="44" y="102" font-size="16" fill="{MUTED}">role: <tspan fill="{ACCENT}">"Full Stack"</tspan>,</text>
  <text class="m" x="44" y="130" font-size="16" fill="{MUTED}">front: [<tspan fill="{ACCENT}">"Next.js"</tspan>, <tspan fill="{ACCENT}">"React"</tspan>],</text>
  <text class="m" x="44" y="158" font-size="16" fill="{MUTED}">back: [<tspan fill="{ACCENT}">"Django"</tspan>, <tspan fill="{ACCENT}">"Prisma"</tspan>],</text>
  <text class="m" x="44" y="186" font-size="16" fill="{MUTED}">openToWork: <tspan fill="{LIGHT}">true</tspan>,</text>
  <text class="m" x="22" y="214" font-size="16" fill="{LIGHT}">}}<tspan class="blink" fill="{ACCENT}">▍</tspan></text>
</g>
</svg>
"""


# ----------------------------------------------------------------- github-stats.svg
def build_stats(s):
    W, H = 1200, 640
    circ = 2 * 3.14159265 * 62
    ring = min(s["cur"] / max(s["best"], 1), 1.0) if s["cur"] else 0
    wd_rows, wd_vals = pct_rows(list(zip(DIAS, s["by_wd"])))
    mo_pairs = [(f"{MESES_LARGO[m-1]} {y}", v) for (y, m), v in s["by_month"].items() if v]
    mo_rows, mo_vals = pct_rows(mo_pairs)
    colors = [LIGHT, ACCENT, MID, "#2F5A8A", "#3A4D66"]
    top_wd = wd_rows[0][0] if wd_rows else "—"
    top_mo = mo_rows[0][0].split(" ")[0] if mo_rows else "—"
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
{style(f"@keyframes ring{{from{{stroke-dashoffset:{circ:.1f}}}}} .ring{{animation:ring 1.6s cubic-bezier(.2,.8,.2,1) .4s backwards}} .glow{{animation:pulse 3s infinite}}")}
{defs()}
{card(W, H)}
<text class="s" x="40" y="64" font-size="30" font-weight="700" fill="{TEXT}">GitHub stats</text>
<text class="s" x="40" y="92" font-size="15" fill="{MUTED}">{NAME} • {ROLE}</text>

<g class="fade" style="animation-delay:.1s">
  <rect x="40" y="120" width="330" height="200" rx="20" fill="{PANEL}" stroke="{STROKE}" stroke-width="1.5"/>
  <text class="s" x="66" y="162" font-size="15" fill="{MUTED}">Contribuciones totales</text>
  <text class="s" x="64" y="254" font-size="76" font-weight="800" fill="{TEXT}">{s['total']}</text>
  <text class="s" x="66" y="294" font-size="14" font-weight="600" fill="{LIGHT}">{fmt(s['first'])} {s['first'].year} – hoy</text>
</g>

<g class="fade" style="animation-delay:.25s">
  <rect x="390" y="120" width="420" height="200" rx="20" fill="{PANEL2}" stroke="{ACCENT}" stroke-opacity=".55" stroke-width="1.5"/>
  <circle class="glow" cx="492" cy="220" r="78" fill="{ACCENT}" opacity=".08"/>
  <circle cx="492" cy="220" r="62" fill="none" stroke="{LEVELS[0]}" stroke-width="10"/>
  <circle class="ring" cx="492" cy="220" r="62" fill="none" stroke="url(#gRing)" stroke-width="10" stroke-linecap="round"
    stroke-dasharray="{circ:.1f}" stroke-dashoffset="{circ*(1-max(ring,0.04)):.1f}" transform="rotate(-90 492 220)"/>
  <text class="s" x="492" y="232" font-size="40" font-weight="800" fill="{TEXT}" text-anchor="middle">{s['cur']:02d}</text>
  <text class="s" x="492" y="254" font-size="12" fill="{MUTED}" text-anchor="middle">días</text>
  <text class="s" x="584" y="196" font-size="20" font-weight="700" fill="{TEXT}">Racha actual</text>
  <text class="s" x="584" y="224" font-size="14" font-weight="600" fill="{LIGHT}">{escape(s['cur_r'])}</text>
  <text class="s" x="584" y="252" font-size="13" fill="{MUTED}">Construyendo cada día</text>
</g>

<g class="fade" style="animation-delay:.4s">
  <rect x="830" y="120" width="330" height="200" rx="20" fill="{PANEL}" stroke="{STROKE}" stroke-width="1.5"/>
  <text class="s" x="856" y="162" font-size="15" fill="{MUTED}">Racha más larga</text>
  <text class="s" x="854" y="254" font-size="76" font-weight="800" fill="{TEXT}">{s['best']:02d}<tspan dx="10" font-size="22" font-weight="500" fill="{MUTED}">días</tspan></text>
  <text class="s" x="856" y="294" font-size="14" font-weight="600" fill="{LIGHT}">{escape(s['best_r'])}</text>
</g>

<g class="fade" style="animation-delay:.55s">
  <rect x="40" y="342" width="550" height="258" rx="20" fill="{PANEL}" stroke="{STROKE}" stroke-width="1.5"/>
  <text class="s" x="66" y="384" font-size="17" font-weight="700" fill="{TEXT}">Actividad por día de la semana</text>
  {legend_rows(66, 426, wd_rows, colors, 270)}
  {donut(468, 480, 64, 22, wd_vals, colors, f"{wd_rows[0][1] if wd_rows else 0}%", top_wd)}
</g>

<g class="fade" style="animation-delay:.7s">
  <rect x="610" y="342" width="550" height="258" rx="20" fill="{PANEL}" stroke="{STROKE}" stroke-width="1.5"/>
  <text class="s" x="636" y="384" font-size="17" font-weight="700" fill="{TEXT}">Meses más activos</text>
  {legend_rows(636, 426, mo_rows, colors, 270)}
  {donut(1038, 480, 64, 22, mo_vals, colors, f"{mo_rows[0][1] if mo_rows else 0}%", top_mo, 0.8)}
</g>
</svg>
"""


# ----------------------------------------------------------------- spent-my-time.svg
CODE_LINES = [
    ('<tspan fill="#ABCDEF">export default</tspan> <tspan fill="#4A90E2">async function</tspan> Page() {', 0),
    ('<tspan fill="#ABCDEF">const</tspan> links = <tspan fill="#ABCDEF">await</tspan> prisma.link', 1),
    ('.findMany({ where: { userId } })', 2),
    ('<tspan fill="#ABCDEF">return</tspan> &lt;<tspan fill="#4A90E2">LinkGrid</tspan> items={links} /&gt;', 1),
    ('}', 0),
]


def build_spent(s):
    W, H = 1600, 640
    days = s["days"]
    first = date.fromisoformat(days[0]["date"])
    start = first - timedelta(days=(first.weekday() + 1) % 7)  # domingo
    x0, y0, dx, cell = 690, 282, 16, 12
    cells, months, last_m = [], [], None
    ncols = 0
    for d in days:
        dt = date.fromisoformat(d["date"])
        col = (dt - start).days // 7
        row = (dt.weekday() + 1) % 7
        ncols = max(ncols, col + 1)
        x, y = x0 + col * dx, y0 + row * dx
        if row == 0 or dt == first:
            if dt.month != last_m and (dt.day <= 7 or dt == first):
                months.append((MESES[dt.month - 1].capitalize(), x))
                last_m = dt.month
        if d["level"]:
            cells.append(f'<rect class="cell" x="{x}" y="{y}" width="{cell}" height="{cell}" rx="3" fill="{LEVELS[d["level"]]}" style="animation-delay:{(col*0.06):.2f}s"/>')
        else:
            cells.append(f'<rect x="{x}" y="{y}" width="{cell}" height="{cell}" rx="3" fill="{LEVELS[0]}"/>')
    grid_w = ncols * dx
    # Distribución por trimestre del último año
    q = [0, 0, 0, 0]
    span = max((date.fromisoformat(days[-1]["date"]) - first).days + 1, 1)
    for d in days:
        idx = min(((date.fromisoformat(d["date"]) - first).days * 4) // span, 3)
        q[idx] += d["count"]
    qt = sum(q) or 1
    qlabels = []
    for i in range(4):
        a = first + timedelta(days=span * i // 4)
        b = first + timedelta(days=span * (i + 1) // 4 - 1)
        qlabels.append(f"{fmt(a)} – {fmt(b)}")
    qcolors = ["#2F5A8A", MID, ACCENT, LIGHT]
    bar_x, bar_w, bar_y = 620, 924, 548
    segs, labels, bx = [], [], bar_x
    for i, v in enumerate(q):
        w = bar_w * v / qt
        if w <= 0:
            continue
        segs.append(f'<rect x="{bx:.1f}" y="{bar_y}" width="{max(w-4,2):.1f}" height="22" rx="11" fill="{qcolors[i]}" class="fade" style="animation-delay:{0.6+i*0.15:.2f}s"/>')
        bx += w
    for i, v in enumerate(q):
        lx = bar_x + i * (bar_w / 4)
        labels.append(f'<circle cx="{lx+6:.1f}" cy="{bar_y+45}" r="6" fill="{qcolors[i]}"/>'
                      f'<text class="s" x="{lx+20:.1f}" y="{bar_y+51}" font-size="16" fill="{MUTED}">{qlabels[i]} '
                      f'<tspan font-weight="700" fill="{TEXT}">{round(v*100/qt)}%</tspan></text>')
    code = []
    for i, (line, ind) in enumerate(CODE_LINES):
        y = 272 + i * 34
        code.append(f'<text class="m fade" style="animation-delay:{0.3+i*0.35:.2f}s" x="{150 + ind*22}" y="{y}" font-size="16" fill="{TEXT}">{line}</text>')
    code.append(f'<rect class="blink" x="{150}" y="{272 + len(CODE_LINES)*34 - 16}" width="10" height="20" fill="{ACCENT}"/>')
    clips = ''
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
{style(".cell{animation:pulse 4s ease-in-out infinite} .blink{animation:pulse 1.2s steps(2) infinite} .float{animation:float 5s ease-in-out infinite} @keyframes float{0%,100%{transform:translateY(0)}50%{transform:translateY(-8px)}}")}
{defs().replace('</defs>', clips + f'<clipPath id="heat"><rect x="{x0}" y="270" width="{grid_w}" height="124"/></clipPath></defs>')}
{card(W, H)}
<text class="s" x="56" y="96" font-size="52" font-weight="800" fill="{TEXT}">Spent My Time</text>
<text class="s" x="58" y="134" font-size="21" fill="{MUTED}">Interfaces limpias, APIs sólidas y bases de datos bien diseñadas.</text>
<circle cx="1110" cy="78" r="7" fill="{LIGHT}"/><text class="s" x="1124" y="84" font-size="18" fill="{TEXT}">Frontend</text>
<circle cx="1240" cy="78" r="7" fill="{ACCENT}"/><text class="s" x="1254" y="84" font-size="18" fill="{TEXT}">Backend</text>
<circle cx="1364" cy="78" r="7" fill="#2F5A8A"/><text class="s" x="1378" y="84" font-size="18" fill="{TEXT}">Bases de datos</text>

<!-- LAPTOP -->
<g class="float">
  <ellipse cx="320" cy="500" rx="250" ry="22" fill="{ACCENT}" opacity=".10"/>
  <rect x="110" y="190" width="420" height="270" rx="18" fill="#0E1726" stroke="{STROKE}" stroke-width="3"/>
  <rect x="124" y="204" width="392" height="242" rx="10" fill="#0A111C"/>
  <circle cx="146" cy="226" r="5" fill="#3A4D66"/><circle cx="164" cy="226" r="5" fill="#3A4D66"/><circle cx="182" cy="226" r="5" fill="{ACCENT}"/>
  <text class="m" x="204" y="231" font-size="15" fill="{TEXT}">netbio/page.tsx</text>
  <rect x="202" y="238" width="128" height="2" fill="{ACCENT}"/>
  {''.join(code)}
  <path d="M80 462 H560 L536 486 H104 Z" fill="#16243A" stroke="{STROKE}" stroke-width="2"/>
  <rect x="270" y="464" width="100" height="6" rx="3" fill="#22364F"/>
</g>
<circle cx="86" cy="230" r="4" fill="{LIGHT}" opacity=".6"/><circle cx="570" cy="300" r="3" fill="{ACCENT}"/><circle cx="560" cy="180" r="5" fill="{ACCENT}" opacity=".5"/>

<!-- HEATMAP -->
<text class="s" x="620" y="224" font-size="28" font-weight="700" fill="{TEXT}">Contribuciones diarias</text>
<text class="s" x="1352" y="222" font-size="18" fill="{MUTED}" text-anchor="end">Menos</text>
{''.join(f'<rect x="{1362+i*24}" y="207" width="18" height="18" rx="4" fill="{c}"/>' for i, c in enumerate(LEVELS))}
<text class="s" x="1488" y="222" font-size="18" fill="{MUTED}">Más</text>
{''.join(f'<text class="s" x="{x}" y="266" font-size="17" fill="{MUTED}">{m}</text>' for m, x in months)}
<text class="s" x="630" y="308" font-size="16" fill="{MUTED}">Lun</text>
<text class="s" x="630" y="340" font-size="16" fill="{MUTED}">Mié</text>
<text class="s" x="630" y="372" font-size="16" fill="{MUTED}">Vie</text>
<g>{''.join(cells)}</g>
<g clip-path="url(#heat)"><rect x="{x0}" y="270" width="90" height="124" fill="url(#gScan)"><animate attributeName="x" values="{x0-90};{x0+grid_w}" dur="9s" repeatCount="indefinite"/></rect></g>

<rect x="620" y="420" width="268" height="42" rx="12" fill="{PANEL2}" stroke="{STROKE}" stroke-width="1.2"/>
<text class="s" x="640" y="447" font-size="16" fill="{TEXT}"><tspan font-weight="700" fill="{LIGHT}">{s['total']}</tspan> contribuciones</text>
<rect x="902" y="420" width="300" height="42" rx="12" fill="{PANEL2}" stroke="{STROKE}" stroke-width="1.2"/>
<text class="s" x="922" y="447" font-size="16" fill="{TEXT}"><tspan font-weight="700" fill="{ACCENT}">{s['best']}d</tspan> racha más larga</text>
<rect x="1216" y="420" width="328" height="42" rx="12" fill="{PANEL2}" stroke="{STROKE}" stroke-width="1.2"/>
<text class="s" x="1236" y="447" font-size="16" fill="{TEXT}"><tspan font-weight="700" fill="{MID}">{s['active']}</tspan> días activos este año</text>

<!-- POR TRIMESTRE -->
<text class="s" x="620" y="526" font-size="24" font-weight="700" fill="{TEXT}">Actividad por trimestre</text>
<rect x="{bar_x}" y="{bar_y}" width="{bar_w}" height="22" rx="11" fill="{LEVELS[0]}"/>
{''.join(segs)}
{''.join(labels)}
</svg>
"""


def main():
    days = load_days()
    if not days:
        print("No se pudieron obtener contribuciones.")
        sys.exit(1)
    s = compute(days)
    print(f"Total {s['total']} · racha actual {s['cur']} ({s['cur_r']}) · más larga {s['best']} ({s['best_r']})")
    os.makedirs("assets", exist_ok=True)
    import xml.etree.ElementTree as ET
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import bento
    files = bento.build_all(s)
    for name, svg in files.items():
        ET.fromstring(svg)  # valida XML
        with open(os.path.join("assets", name), "w", encoding="utf-8") as f:
            f.write(svg)
        print(f"assets/{name} actualizado")


if __name__ == "__main__":
    main()
