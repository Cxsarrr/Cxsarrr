"""
scripts/bento.py
Diseño "bento grid" con fondos tipo aurora para el perfil de @Cxsarrr.
"""

from datetime import date, timedelta
from xml.sax.saxutils import escape

from update_stats import DIAS, MESES, fmt

BASE = "#070B14"
TILE = "#0C1322"
TILE2 = "#101A2E"
LINE = "#1C2A44"
TEXT = "#F3F7FD"
MUTED = "#8593AB"
BLUE = "#4A90E2"
SKY = "#38BDF8"
VIOLET = "#7C83FD"
ICE = "#ABCDEF"
LEVELS = ["#121C2E", "#1E3A66", "#2F5FA0", "#4A90E2", "#9CCBFF"]
SANS = "-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif"
MONO = "ui-monospace,SFMono-Regular,Menlo,Consolas,monospace"


def head(W, H, css=""):
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
<style>
  text{{font-family:{SANS}}} .m{{font-family:{MONO}}}
  .in{{animation:in .8s cubic-bezier(.2,.8,.2,1) backwards}}
  @keyframes in{{from{{opacity:0;transform:translateY(14px)}}}}
  .pulse{{animation:pulse 2.2s ease-in-out infinite}}
  @keyframes pulse{{0%,100%{{opacity:.45}}50%{{opacity:1}}}}
  .drift{{animation:drift 14s ease-in-out infinite alternate}}
  .drift2{{animation:drift 18s ease-in-out infinite alternate-reverse}}
  @keyframes drift{{from{{transform:translate(-40px,-20px)}}to{{transform:translate(40px,30px)}}}}
  {css}
</style>
<defs>
  <radialGradient id="aB"><stop offset="0" stop-color="{BLUE}" stop-opacity=".55"/><stop offset="1" stop-color="{BLUE}" stop-opacity="0"/></radialGradient>
  <radialGradient id="aS"><stop offset="0" stop-color="{SKY}" stop-opacity=".40"/><stop offset="1" stop-color="{SKY}" stop-opacity="0"/></radialGradient>
  <radialGradient id="aV"><stop offset="0" stop-color="{VIOLET}" stop-opacity=".45"/><stop offset="1" stop-color="{VIOLET}" stop-opacity="0"/></radialGradient>
  <linearGradient id="gName" x1="0" x2="1"><stop offset="0" stop-color="{TEXT}"/><stop offset=".55" stop-color="{ICE}"/><stop offset="1" stop-color="{SKY}"/></linearGradient>
  <linearGradient id="gEdge" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#2A3E62"/><stop offset=".5" stop-color="{LINE}"/><stop offset="1" stop-color="#243656"/></linearGradient>
  <linearGradient id="gBtn" x1="0" x2="1"><stop offset="0" stop-color="{BLUE}"/><stop offset="1" stop-color="{SKY}"/></linearGradient>
  <linearGradient id="gRing" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{SKY}"/><stop offset="1" stop-color="{VIOLET}"/></linearGradient>
</defs>"""


def tile(x, y, w, h, delay=0.0, fill=TILE, aurora=None, cid=None):
    """Mosaico con borde degradado. aurora = lista de (gradiente, cx, cy, r)."""
    cid = cid or f"t{x}_{y}"
    blobs = ""
    if aurora:
        blobs = f'<g clip-path="url(#{cid})">' + "".join(
            f'<circle class="{"drift" if i % 2 == 0 else "drift2"}" cx="{x+cx}" cy="{y+cy}" r="{r}" fill="url(#{g})"/>'
            for i, (g, cx, cy, r) in enumerate(aurora)) + "</g>"
    return (f'<clipPath id="{cid}"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="28"/></clipPath>'
            f'<g class="in" style="animation-delay:{delay:.2f}s">'
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="28" fill="{fill}"/>{blobs}'
            f'<rect x="{x+.75}" y="{y+.75}" width="{w-1.5}" height="{h-1.5}" rx="27.5" fill="none" stroke="url(#gEdge)" stroke-width="1.5"/>')


def label(x, y, txt, color=MUTED):
    return f'<text class="m" x="{x}" y="{y}" font-size="15" letter-spacing="3" fill="{color}">{escape(txt)}</text>'


# ------------------------------------------------------------------ HERO
STACK_A = ["Django", "Next.js", "React", "TypeScript", "Python", "Tailwind CSS", "Vite", "Framer Motion"]
STACK_B = ["PostgreSQL", "Prisma", "MySQL", "Django REST", "Git", "Linux", "Postman", "Serverless"]


def marquee(items, x, y, clip, speed, reverse=False, hi=None):
    pills, cx = [], 0
    for it in items:
        w = len(it) * 12.2 + 44
        color = ICE if it in (hi or []) else TEXT
        pills.append(f'<g transform="translate({cx:.0f} 0)"><rect width="{w:.0f}" height="48" rx="24" fill="{TILE2}" stroke="{LINE}"/>'
                     f'<circle cx="22" cy="24" r="4" fill="{BLUE if it in (hi or []) else "#3A4F72"}"/>'
                     f'<text x="36" y="31" font-size="19" font-weight="600" fill="{color}">{it}</text></g>')
        cx += w + 14
    row = "".join(pills)
    k = f"mq{x}_{y}"
    frm, to = (f"-{cx:.0f}px", "0px") if reverse else ("0px", f"-{cx:.0f}px")
    css = f"@keyframes {k}{{from{{transform:translateX({frm})}}to{{transform:translateX({to})}}}} .{k}{{animation:{k} {speed}s linear infinite}}"
    return (f'<g clip-path="url(#{clip})"><g transform="translate({x} {y})"><g class="{k}">{row}'
            f'<g transform="translate({cx:.0f} 0)">{row}</g></g></g></g>'), css


def build_hero(s):
    W, H = 1600, 780
    css = []
    hi = ["Django", "Next.js", "React", "TypeScript", "PostgreSQL", "Prisma"]
    m1, c1 = marquee(STACK_A, 664, 640, "tF", 38, hi=hi)
    m2, c2 = marquee(STACK_B, 664, 700, "tF", 44, reverse=True, hi=hi)
    css += [c1, c2, ".ring{animation:ring 1.6s cubic-bezier(.2,.8,.2,1) .6s backwards} @keyframes ring{from{stroke-dashoffset:302}}",
            ".blink{animation:pulse 1s steps(2) infinite}"]
    # globo de puntos para ubicación
    dots = []
    for i in range(-5, 6):
        for j in range(-5, 6):
            if i * i + j * j <= 26:
                hl = (i, j) in ((1, 1), (0, 1), (1, 2))
                cls = ' class="pulse"' if hl else ""
                col = SKY if hl else "#2A3B5A"
                dots.append(f'<circle cx="{1140 + i*14}" cy="{404 + j*14}" r="{4 if hl else 2.6}" fill="{col}"{cls}/>')
    circ = 2 * 3.14159 * 48
    frac = min(s["cur"] / max(s["best"], 1), 1) if s["cur"] else 0.04
    return head(W, H, " ".join(css)) + f"""
<rect width="{W}" height="{H}" rx="34" fill="{BASE}"/>

{tile(24, 24, 960, 476, 0.0, aurora=[("aB", 760, 80, 380), ("aV", 900, 420, 300), ("aS", 120, 520, 260)], cid="tA")}
  {label(72, 98, "HOLA, SOY")}
  <text x="68" y="214" font-size="118" font-weight="800" letter-spacing="-4" fill="url(#gName)">Cesar</text>
  <text x="68" y="330" font-size="118" font-weight="800" letter-spacing="-4" fill="url(#gName)">Bolivar<tspan fill="{SKY}" class="blink">.</tspan></text>
  <text x="72" y="392" font-size="27" fill="{MUTED}">Desarrollador <tspan fill="{TEXT}" font-weight="700">Full Stack</tspan> — de la interfaz a la base de datos.</text>
  <rect x="72" y="424" width="276" height="48" rx="24" fill="url(#gBtn)"/>
  <text x="210" y="455" font-size="18" font-weight="700" fill="{BASE}" text-anchor="middle">Visita mi portafolio ↗</text>
</g>

{tile(1004, 24, 572, 220, 0.15, aurora=[("aS", 520, 40, 220)], cid="tB")}
  {label(1044, 76, "ESTADO")}
  <circle cx="1056" cy="134" r="18" fill="#22C55E" opacity=".18" class="pulse"/>
  <circle cx="1056" cy="134" r="8" fill="#4ADE80"/>
  <text x="1086" y="144" font-size="32" font-weight="800" fill="{TEXT}">Abierto a oportunidades</text>
  <text x="1044" y="200" font-size="20" fill="{MUTED}">Freelance · tiempo completo · proyectos</text>
</g>

{tile(1004, 264, 276, 236, 0.3, cid="tC")}
  {label(1044, 316, "UBICACIÓN")}
  {''.join(dots)}
  <text x="1044" y="472" font-size="22" font-weight="700" fill="{TEXT}">Barranquilla</text>
  <text x="1200" y="472" font-size="18" fill="{MUTED}">CO</text>
</g>

{tile(1300, 264, 276, 236, 0.45, aurora=[("aV", 240, 220, 200)], cid="tD")}
  {label(1340, 316, "RACHA ACTUAL")}
  <circle cx="1438" cy="398" r="48" fill="none" stroke="{LEVELS[0]}" stroke-width="10"/>
  <circle class="ring" cx="1438" cy="398" r="48" fill="none" stroke="url(#gRing)" stroke-width="10" stroke-linecap="round"
    stroke-dasharray="{circ:.0f}" stroke-dashoffset="{circ*(1-frac):.0f}" transform="rotate(-90 1438 398)"/>
  <text x="1438" y="412" font-size="38" font-weight="800" fill="{TEXT}" text-anchor="middle">{s['cur']}</text>
  <text x="1438" y="476" font-size="17" fill="{MUTED}" text-anchor="middle">{'día seguido' if s['cur'] == 1 else 'días seguidos'}</text>
</g>

{tile(24, 520, 620, 236, 0.6, aurora=[("aB", 80, 240, 240)], cid="tE")}
  {label(64, 572, "MI FORMA DE TRABAJAR")}
  <text x="64" y="624" font-size="19" fill="{MUTED}"><tspan class="m" fill="{SKY}" font-weight="700">01</tspan>  Interfaces <tspan fill="{TEXT}" font-weight="700">claras</tspan> y accesibles</text>
  <text x="64" y="666" font-size="19" fill="{MUTED}"><tspan class="m" fill="{SKY}" font-weight="700">02</tspan>  APIs <tspan fill="{TEXT}" font-weight="700">sólidas</tspan> y bien pensadas</text>
  <text x="64" y="708" font-size="19" fill="{MUTED}"><tspan class="m" fill="{SKY}" font-weight="700">03</tspan>  Datos <tspan fill="{TEXT}" font-weight="700">bien modelados</tspan></text>
  <g transform="translate(462 556)">
    <line x1="66" y1="22" x2="66" y2="160" stroke="{LINE}" stroke-width="2" stroke-dasharray="4 6"/>
    <circle cx="66" cy="22" r="5" fill="{SKY}"><animateMotion dur="2.4s" repeatCount="indefinite" path="M0 0 V138"/></circle>
    <circle cx="66" cy="160" r="4" fill="{ICE}"><animateMotion dur="2.4s" begin="1.2s" repeatCount="indefinite" path="M0 0 V-138"/></circle>
    <rect x="0" y="0" width="132" height="44" rx="14" fill="{TILE2}" stroke="{SKY}" stroke-opacity=".7"/>
    <text x="66" y="29" font-size="16" font-weight="700" fill="{TEXT}" text-anchor="middle">Interfaz</text>
    <rect x="0" y="68" width="132" height="44" rx="14" fill="{TILE2}" stroke="{BLUE}" stroke-opacity=".7"/>
    <text x="66" y="97" font-size="16" font-weight="700" fill="{TEXT}" text-anchor="middle">API</text>
    <rect x="0" y="136" width="132" height="44" rx="14" fill="{TILE2}" stroke="{VIOLET}" stroke-opacity=".7"/>
    <text x="66" y="165" font-size="16" font-weight="700" fill="{TEXT}" text-anchor="middle">Base de datos</text>
  </g>
</g>

{tile(664, 520, 912, 236, 0.75, cid="tF")}
  {label(704, 572, "STACK")}
  <text x="1536" y="572" font-size="15" fill="{MUTED}" text-anchor="end" class="m">{s['total']} contribuciones este año</text>
  {m1}
  {m2}
</g>
</svg>
"""


# ------------------------------------------------------------------ PROYECTOS
def project(title, emoji, url, desc, tags, mock, cid, aur, dx=20):
    W, H = 780, 500
    pills, x = [], 40
    for t in tags:
        w = len(t) * 10.5 + 30
        if x + w > W - 40:
            break
        pills.append(f'<rect x="{x}" y="440" width="{w:.0f}" height="34" rx="17" fill="{TILE2}" stroke="{LINE}"/>'
                     f'<text x="{x + w/2:.0f}" y="462" font-size="15" font-weight="600" fill="{ICE}" text-anchor="middle">{t}</text>')
        x += w + 10
    return head(W, H, ".float{animation:float 6s ease-in-out infinite} @keyframes float{0%,100%{transform:translateY(0)}50%{transform:translateY(-7px)}}") + f"""
<rect width="{W}" height="{H}" rx="30" fill="{BASE}"/>
{tile(0, 0, W, H, 0, aurora=aur, cid=cid)}
<g class="float" transform="translate(-20 -50)">
  <rect x="60" y="80" width="{W-80}" height="250" rx="18" fill="#080E1A" stroke="{LINE}" stroke-width="1.5"/>
  <rect x="61" y="81" width="{W-82}" height="34" rx="17" fill="{TILE2}"/>
  <circle cx="86" cy="98" r="6" fill="#3A4F72"/><circle cx="106" cy="98" r="6" fill="#3A4F72"/><circle cx="126" cy="98" r="6" fill="{SKY}"/>
  <rect x="152" y="87" width="{W-252}" height="22" rx="11" fill="#080E1A"/>
  <text class="m" x="170" y="103" font-size="13" fill="{MUTED}">{url}</text>
  <g transform="translate({dx} 78)">{mock}</g>
</g>
<text x="40" y="348" font-size="34" font-weight="800" fill="{TEXT}">{emoji} {title}</text>
<text x="{W-40}" y="346" font-size="17" font-weight="700" fill="{SKY}" text-anchor="end">Visitar ↗</text>
<text x="40" y="386" font-size="19" fill="{MUTED}">{desc[0]}</text>
<text x="40" y="414" font-size="19" fill="{MUTED}">{desc[1]}</text>
{''.join(pills)}
</g>
</svg>
"""


def build_projects():
    import cards
    nb = cards.netbio_mock().replace('fill="url(#gRing)"', f'fill="{SKY}"')
    pf = cards.portfolio_mock().replace('fill="url(#gRing)"', f'fill="{SKY}"')
    return {
        "bento-netbio.svg": project("NetBio", "🔗", "netbio.site",
                                    ["Todos tus enlaces en un lugar: tarjetas vCard,", "códigos QR y captura de clientes."],
                                    ["Next.js 16", "TypeScript", "Prisma", "Postgres", "Tailwind 4"],
                                    f'<g transform="translate(-10 -38) scale(.96)">{nb}</g>', "pA",
                                    [("aB", 700, 40, 320), ("aS", 60, 480, 240)], dx=60),
        "bento-portfolio.svg": project("Portafolio Web", "💼", "cesarbolivar.site",
                                       ["Mi perfil profesional, interactivo y bilingüe,", "con animaciones fluidas."],
                                       ["React 19", "Vite", "TypeScript", "Tailwind 4", "Framer Motion"],
                                       f'<g transform="translate(-10 -38) scale(.96)">{pf}</g>', "pB",
                                       [("aV", 700, 40, 320), ("aB", 60, 480, 240)]),
    }


# ------------------------------------------------------------------ ACTIVIDAD
def build_activity(s):
    W, H = 1600, 760
    days = s["days"]
    first = date.fromisoformat(days[0]["date"])
    start = first - timedelta(days=(first.weekday() + 1) % 7)
    x0, y0, step, cell = 96, 150, 27, 21
    cells, months, last_m, ncols = [], [], None, 0
    for d in days:
        dt = date.fromisoformat(d["date"])
        col, row = (dt - start).days // 7, (dt.weekday() + 1) % 7
        ncols = max(ncols, col + 1)
        x, y = x0 + col * step, y0 + row * step
        if row == 0 and dt.day <= 7 and dt.month != last_m:
            months.append((MESES[dt.month - 1].capitalize(), x))
            last_m = dt.month
        lv = d["level"]
        extra = f' class="pulse" style="animation-delay:{(col % 9) * .3:.1f}s"' if lv >= 3 else ""
        cells.append(f'<rect x="{x}" y="{y}" width="{cell}" height="{cell}" rx="5" fill="{LEVELS[lv]}"{extra}/>')
    gw = ncols * step
    # barras por día de la semana (lun..dom)
    mx = max(s["by_wd"]) or 1
    bars = []
    for i, v in enumerate(s["by_wd"]):
        h = 150 * v / mx
        bx = 1080 + i * 64
        top = i == s["by_wd"].index(mx)
        bars.append(f'<rect x="{bx}" y="{698 - 150}" width="40" height="150" rx="10" fill="{LEVELS[0]}"/>'
                    f'<rect class="grow" x="{bx}" y="{698 - h:.0f}" width="40" height="{max(h, 6):.0f}" rx="10" fill="{"url(#gBtn)" if top else LEVELS[2]}" style="animation-delay:{.5 + i*.08:.2f}s"/>'
                    f'<text x="{bx + 20}" y="728" font-size="15" fill="{TEXT if top else MUTED}" text-anchor="middle">{DIAS[i][:2]}</text>')
    top_day = DIAS[s["by_wd"].index(mx)]
    top_day = top_day if top_day.endswith("s") else top_day + "s"
    css = ".grow{animation:grow 1s cubic-bezier(.2,.8,.2,1) backwards;transform-box:fill-box;transform-origin:bottom} @keyframes grow{from{transform:scaleY(0)}}"
    scan = (f'<g clip-path="url(#hm)"><rect x="{x0-120}" y="{y0-6}" width="120" height="{7*step+6}" fill="url(#scan)">'
            f'<animate attributeName="x" values="{x0-120};{x0+gw}" dur="7s" repeatCount="indefinite"/></rect></g>')
    return head(W, H, css) + f"""
<defs><linearGradient id="scan" x1="0" x2="1"><stop offset="0" stop-color="{SKY}" stop-opacity="0"/><stop offset=".5" stop-color="{SKY}" stop-opacity=".16"/><stop offset="1" stop-color="{SKY}" stop-opacity="0"/></linearGradient>
<clipPath id="hm"><rect x="{x0}" y="{y0-6}" width="{gw}" height="{7*step+6}"/></clipPath></defs>
<rect width="{W}" height="{H}" rx="34" fill="{BASE}"/>

{tile(24, 24, 1552, 380, 0, aurora=[("aB", 1300, 0, 360), ("aV", 200, 420, 300)], cid="hA")}
  {label(64, 86, "ACTIVIDAD · ÚLTIMO AÑO")}
  <g transform="translate(1290 66)">
    <text x="0" y="14" font-size="15" fill="{MUTED}" text-anchor="end">Menos</text>
    {''.join(f'<rect x="{12 + i*24}" y="0" width="18" height="18" rx="5" fill="{c}"/>' for i, c in enumerate(LEVELS))}
    <text x="138" y="14" font-size="15" fill="{MUTED}">Más</text>
  </g>
  {''.join(f'<text x="{x}" y="{y0 - 18}" font-size="15" fill="{MUTED}">{m}</text>' for m, x in months)}
  <text x="56" y="{y0 + step + 16}" font-size="14" fill="{MUTED}">Lun</text>
  <text x="56" y="{y0 + 3*step + 16}" font-size="14" fill="{MUTED}">Mié</text>
  <text x="56" y="{y0 + 5*step + 16}" font-size="14" fill="{MUTED}">Vie</text>
  {''.join(cells)}
  {scan}
</g>

{tile(24, 424, 330, 312, .15, aurora=[("aS", 300, 0, 260)], cid="hB")}
  {label(64, 480, "CONTRIBUCIONES")}
  <text x="60" y="600" font-size="104" font-weight="800" letter-spacing="-3" fill="url(#gName)">{s['total']}</text>
  <text x="64" y="660" font-size="18" fill="{MUTED}">desde el {fmt(s['first'])} {s['first'].year}</text>
  <text x="64" y="700" font-size="18" fill="{MUTED}"><tspan fill="{TEXT}" font-weight="700">{s['active']}</tspan> días activos</text>
</g>

{tile(374, 424, 330, 312, .3, cid="hC")}
  {label(414, 480, "RACHA MÁS LARGA")}
  <text x="410" y="600" font-size="104" font-weight="800" letter-spacing="-3" fill="{TEXT}">{s['best']}<tspan font-size="32" font-weight="600" fill="{MUTED}" dx="10">días</tspan></text>
  <text x="414" y="660" font-size="18" fill="{SKY}" font-weight="600">{escape(s['best_r'])}</text>
  <text x="414" y="700" font-size="18" fill="{MUTED}">Racha actual: <tspan fill="{TEXT}" font-weight="700">{s['cur']}</tspan></text>
</g>

{tile(724, 424, 852, 312, .45, aurora=[("aV", 820, 300, 280)], cid="hD")}
  {label(764, 480, "¿CUÁNDO PROGRAMO MÁS?")}
  <text x="764" y="560" font-size="44" font-weight="800" fill="{TEXT}">{top_day}</text>
  <text x="764" y="600" font-size="19" fill="{MUTED}">es mi día más productivo:</text>
  <text x="764" y="628" font-size="19" fill="{MUTED}"><tspan fill="{TEXT}" font-weight="700">{round(mx * 100 / (sum(s['by_wd']) or 1))}%</tspan> de mis contribuciones.</text>
  {''.join(bars)}
</g>
</svg>
"""


# ------------------------------------------------------------------ CIERRE
def build_cta():
    W, H = 1600, 300
    return head(W, H) + f"""
<rect width="{W}" height="{H}" rx="34" fill="{BASE}"/>
{tile(24, 24, 1552, 252, 0, aurora=[("aB", 300, 260, 420), ("aV", 1250, 0, 420), ("aS", 780, 300, 300)], cid="cA")}
  {label(72, 92, "¿TIENES UNA IDEA?")}
  <text x="68" y="172" font-size="64" font-weight="800" letter-spacing="-2" fill="url(#gName)">Construyamos algo juntos.</text>
  <text x="72" y="222" font-size="22" fill="{MUTED}">Escríbeme y conversemos sobre tu proyecto.</text>
  <rect x="1236" y="118" width="292" height="68" rx="34" fill="url(#gBtn)"/>
  <text x="1382" y="161" font-size="23" font-weight="800" fill="{BASE}" text-anchor="middle">Hablemos →</text>
</g>
</svg>
"""


def build_all(s):
    out = {"bento-hero.svg": build_hero(s), "bento-activity.svg": build_activity(s), "bento-cta.svg": build_cta()}
    out.update(build_projects())
    return out
