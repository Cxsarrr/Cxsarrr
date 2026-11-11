"""
scripts/cards.py
SVG estáticos del perfil: portada (hero), tarjetas de proyectos y pie.
"""

from update_stats import (ACCENT, BG, FONT, LIGHT, MID, MONO, MUTED, PANEL, PANEL2,
                          STROKE, TEXT, defs, style)

DEEP = "#1F3A63"


_RV = []


def reveal(x, y, w, h, delay, dur=0.9, chars=28, fill="#0A111C"):
    """Rectángulo que tapa el texto y se desliza para simular que se escribe.
    Sin animación queda desplazado (atributo transform) y el texto se ve completo."""
    k = f"rv{len(_RV)}"
    _RV.append(f"@keyframes {k}{{from{{transform:translateX(0)}}to{{transform:translateX({w:.0f}px)}}}}"
               f".{k}{{animation:{k} {dur:.2f}s steps({chars}) {delay:.2f}s backwards}}")
    return (f'<rect class="{k}" x="{x}" y="{y}" width="{w:.0f}" height="{h}" fill="{fill}" '
            f'transform="translate({w:.0f} 0)"/>')


# --------------------------------------------------------------------- HERO
def build_hero():
    W, H = 1600, 560
    lines = [
        ("$", "whoami", None),
        ("→", "Cesar Bolivar", "Desarrollador Full Stack"),
        ("$", "cat stack.txt", None),
        ("→", "Django · Next.js · React · TypeScript", None),
        ("$", "status --now", None),
        ("●", "Abierto a oportunidades", None),
    ]
    tx, ty, lh = 96, 196, 46
    rows, t = [], 0.4
    for i, (p, txt, extra) in enumerate(lines):
        y = ty + i * lh
        cmd = p == "$"
        pc = ACCENT if cmd else (LIGHT if p == "●" else MUTED)
        body = (f'<tspan fill="{TEXT if cmd else LIGHT}" font-weight="{600 if not cmd else 400}">{txt}</tspan>'
                + (f'<tspan dx="14" fill="{MUTED}">·</tspan><tspan dx="14" fill="{MUTED}">{extra}</tspan>' if extra else ""))
        dot = ' class="pulse"' if p == "●" else ""
        rows.append(f'<text class="m" x="{tx}" y="{y}" font-size="24"><tspan fill="{pc}"{dot}>{p}</tspan>&#160;{body}</text>')
        n = len(txt) + (len(extra) + 5 if extra else 0) + 3
        w = n * 14.5 + 20
        rows.append(reveal(tx - 4, y - 28, w, 40, t, dur=n * 0.035 if cmd else 0.25, chars=n if cmd else 1))
        t += n * 0.035 + 0.35 if cmd else 0.45
    cursor_y = ty + len(lines) * lh
    rows.append(f'<text class="m" x="{tx}" y="{cursor_y}" font-size="24" fill="{ACCENT}">$ <tspan class="caret">▍</tspan></text>')

    # Monograma con órbitas
    cx, cy = 1236, 300
    orbit = f"""
<g transform="translate({cx} {cy})">
  <circle r="190" fill="none" stroke="{STROKE}" stroke-dasharray="2 10"/>
  <circle r="140" fill="none" stroke="{STROKE}"/>
  <g class="spin" style="animation-duration:22s"><circle cx="190" cy="0" r="7" fill="{LIGHT}"/><circle cx="-190" cy="0" r="4" fill="{ACCENT}"/></g>
  <g class="spin rev" style="animation-duration:14s"><circle cx="0" cy="-140" r="6" fill="{ACCENT}"/><circle cx="99" cy="99" r="3.5" fill="{LIGHT}"/></g>
  <circle r="98" fill="url(#gMono)" opacity=".18" class="pulse"/>
  <polygon points="0,-92 80,-46 80,46 0,92 -80,46 -80,-46" fill="{PANEL2}" stroke="url(#gRing)" stroke-width="3"/>
  <text class="s" x="0" y="22" font-size="64" font-weight="800" fill="{TEXT}" text-anchor="middle" letter-spacing="-2">CB</text>
  <g font-family="{MONO}" font-size="15" fill="{MUTED}">
    <text x="150" y="-150">&lt;/&gt;</text><text x="-210" y="150">{{ }}</text><text x="160" y="170">SQL</text><text x="-200" y="-120">API</text>
  </g>
</g>"""
    stars = "".join(
        f'<circle cx="{(i*397)%W}" cy="{(i*211)%H}" r="{1 + (i%3)*0.6}" fill="{LIGHT}" class="tw" style="animation-delay:{(i%7)*0.6:.1f}s"/>'
        for i in range(1, 46))
    css = "\n".join(_RV) + """
  .caret{animation:pulse 1s steps(2) infinite}
  .pulse{animation:pulse 2.4s ease-in-out infinite}
  .spin{animation:spin linear infinite;transform-box:view-box;transform-origin:0 0}
  .rev{animation-direction:reverse}
  .tw{animation:pulse 3.5s ease-in-out infinite;opacity:.5}
"""
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
{style(css)}
{defs().replace('</defs>', f'<radialGradient id="gMono"><stop offset="0" stop-color="{ACCENT}"/><stop offset="1" stop-color="{ACCENT}" stop-opacity="0"/></radialGradient><clipPath id="tc"><rect x="58" y="118" width="896" height="384"/></clipPath><clipPath id="hc"><rect x="1" y="1" width="{W-2}" height="{H-2}" rx="28"/></clipPath></defs>')}
<g clip-path="url(#hc)">
  <rect width="{W}" height="{H}" fill="{BG}"/>
  <rect width="{W}" height="{H}" fill="url(#gGlow)"/>
  <rect width="{W}" height="{H}" fill="url(#gGlow2)"/>
  <g opacity=".5">{stars}</g>
</g>
<rect x="1" y="1" width="{W-2}" height="{H-2}" rx="28" fill="none" stroke="{STROKE}" stroke-width="2"/>

<!-- terminal -->
<rect x="56" y="64" width="900" height="440" rx="20" fill="#0A111C" stroke="{STROKE}" stroke-width="2"/>
<path d="M76 64 h860 a20 20 0 0 1 20 20 v32 h-900 v-32 a20 20 0 0 1 20 -20z" fill="{PANEL2}"/>
<line x1="56" y1="116" x2="956" y2="116" stroke="{STROKE}" stroke-width="2"/>
<circle cx="88" cy="90" r="8" fill="#3A4D66"/><circle cx="114" cy="90" r="8" fill="#3A4D66"/><circle cx="140" cy="90" r="8" fill="{ACCENT}"/>
<text class="m" x="506" y="96" font-size="17" fill="{MUTED}" text-anchor="middle">cesar@bolivar: ~/portafolio — zsh</text>
<g clip-path="url(#tc)">{''.join(rows)}</g>

{orbit}
<text class="m" x="1236" y="536" font-size="16" fill="{MUTED}" text-anchor="middle" letter-spacing="3">BARRANQUILLA · CO</text>
</svg>
"""


# --------------------------------------------------------------------- PROYECTOS
def pill(x, y, label, fill=PANEL2, color=LIGHT):
    w = len(label) * 9.2 + 26
    return (f'<rect x="{x}" y="{y}" width="{w:.0f}" height="30" rx="15" fill="{fill}" stroke="{STROKE}"/>'
            f'<text class="m" x="{x + w/2:.0f}" y="{y+20}" font-size="14" fill="{color}" text-anchor="middle">{label}</text>'), w


def project_card(title, url, desc, tags, mock, emoji):
    W, H = 800, 520
    pills, x = [], 40
    for t in tags:
        p, w = pill(x, 468, t)
        if x + w > W - 40:
            break
        pills.append(p)
        x += w + 10
    desc_lines = "".join(
        f'<text class="s" x="40" y="{396 + i*28}" font-size="19" fill="{MUTED}">{ln}</text>'
        for i, ln in enumerate(desc))
    css = ".hov{animation:float 6s ease-in-out infinite} @keyframes float{0%,100%{transform:translateY(0)}50%{transform:translateY(-6px)}} .pulse{animation:pulse 2.4s infinite}"
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
{style(css)}
{defs()}
<rect x="1" y="1" width="{W-2}" height="{H-2}" rx="26" fill="url(#gCard)" stroke="{STROKE}" stroke-width="2"/>
<rect x="1" y="1" width="{W-2}" height="{H-2}" rx="26" fill="url(#gGlow)"/>
<!-- navegador -->
<g class="hov">
  <rect x="40" y="36" width="{W-80}" height="270" rx="16" fill="#0A111C" stroke="{STROKE}" stroke-width="2"/>
  <path d="M56 36 h{W-112} a16 16 0 0 1 16 16 v22 h-{W-80} v-22 a16 16 0 0 1 16 -16z" fill="{PANEL2}"/>
  <circle cx="66" cy="56" r="6" fill="#3A4D66"/><circle cx="86" cy="56" r="6" fill="#3A4D66"/><circle cx="106" cy="56" r="6" fill="{ACCENT}"/>
  <rect x="136" y="44" width="{W-216}" height="24" rx="12" fill="#0A111C"/>
  <text class="m" x="156" y="61" font-size="14" fill="{MUTED}">🔒 {url}</text>
  {mock}
</g>
<text class="s" x="40" y="352" font-size="30" font-weight="800" fill="{TEXT}">{emoji} {title}</text>
<g transform="translate({W-148} 326)"><rect width="108" height="34" rx="17" fill="{ACCENT}"/>
  <circle cx="22" cy="17" r="5" fill="{TEXT}" class="pulse"/>
  <text class="s" x="62" y="23" font-size="15" font-weight="700" fill="{TEXT}" text-anchor="middle">En vivo</text></g>
{desc_lines}
{''.join(pills)}
</svg>
"""


def netbio_mock():
    # teléfono con link-in-bio + QR + tarjeta vCard
    btns = "".join(
        f'<rect x="300" y="{150 + i*30}" width="200" height="22" rx="11" fill="{c}"/>'
        f'<text class="s" x="400" y="{165 + i*30}" font-size="11" font-weight="600" fill="{tc}" text-anchor="middle">{t}</text>'
        for i, (t, c, tc) in enumerate([("Instagram", ACCENT, TEXT), ("LinkedIn", DEEP, TEXT),
                                         ("Portafolio", DEEP, TEXT), ("Descargar vCard", LIGHT, BG)]))
    qr = "".join(
        f'<rect x="{560 + (i%7)*12}" y="{130 + (i//7)*12}" width="10" height="10" rx="2" fill="{LIGHT if (i*7+i//3)%3 else DEEP}"/>'
        for i in range(49))
    return f"""
  <rect x="290" y="86" width="220" height="210" rx="22" fill="{PANEL}" stroke="{STROKE}" stroke-width="2"/>
  <circle cx="400" cy="116" r="20" fill="url(#gRing)"/>
  <text class="s" x="400" y="123" font-size="16" font-weight="800" fill="{BG}" text-anchor="middle">CB</text>
  <text class="s" x="400" y="146" font-size="0" fill="{TEXT}">.</text>
  {btns}
  <g>
    <rect x="548" y="118" width="108" height="108" rx="14" fill="{PANEL}" stroke="{STROKE}"/>
    {qr}
    <text class="m" x="602" y="252" font-size="12" fill="{MUTED}" text-anchor="middle">QR dinámico</text>
  </g>
  <g>
    <rect x="96" y="132" width="160" height="96" rx="14" fill="{PANEL}" stroke="{STROKE}"/>
    <circle cx="124" cy="160" r="14" fill="{DEEP}"/>
    <rect x="146" y="152" width="90" height="8" rx="4" fill="{LIGHT}"/>
    <rect x="146" y="166" width="60" height="6" rx="3" fill="{MUTED}"/>
    <rect x="112" y="192" width="128" height="22" rx="11" fill="{ACCENT}"/>
    <text class="s" x="176" y="207" font-size="11" font-weight="700" fill="{TEXT}" text-anchor="middle">+ Nuevo lead</text>
  </g>"""


def portfolio_mock():
    return f"""
  <rect x="60" y="86" width="680" height="30" fill="#0D1622"/>
  <text class="s" x="80" y="106" font-size="15" font-weight="800" fill="{TEXT}">cesar<tspan fill="{ACCENT}">.</tspan></text>
  <text class="s" x="470" y="106" font-size="12" fill="{MUTED}">Sobre mí    Proyectos    Contacto</text>
  <rect x="664" y="92" width="58" height="18" rx="9" fill="{PANEL2}" stroke="{STROKE}"/>
  <rect x="666" y="94" width="27" height="14" rx="7" fill="{ACCENT}"/>
  <text class="s" x="679" y="105" font-size="9" font-weight="700" fill="{TEXT}" text-anchor="middle">ES</text>
  <text class="s" x="707" y="105" font-size="9" fill="{MUTED}" text-anchor="middle">EN</text>
  <text class="m" x="80" y="152" font-size="13" fill="{ACCENT}">— hola, soy</text>
  <text class="s" x="80" y="196" font-size="40" font-weight="800" fill="{TEXT}">Cesar Bolivar</text>
  <rect x="80" y="214" width="250" height="8" rx="4" fill="{STROKE}"/>
  <rect x="80" y="230" width="190" height="8" rx="4" fill="{STROKE}"/>
  <rect x="80" y="252" width="110" height="30" rx="15" fill="{ACCENT}"/>
  <text class="s" x="135" y="272" font-size="12" font-weight="700" fill="{TEXT}" text-anchor="middle">Ver proyectos</text>
  <rect x="200" y="252" width="96" height="30" rx="15" fill="none" stroke="{STROKE}" stroke-width="1.5"/>
  <text class="s" x="248" y="272" font-size="12" fill="{LIGHT}" text-anchor="middle">Contacto</text>
  <g transform="translate(560 196)">
    <circle r="78" fill="none" stroke="{STROKE}" stroke-dasharray="3 7"/>
    <circle r="58" fill="url(#gRing)" opacity=".9"/>
    <text class="s" y="12" font-size="34" font-weight="800" fill="{BG}" text-anchor="middle">CB</text>
    <g style="animation:spin 10s linear infinite;transform-box:view-box;transform-origin:0 0"><circle cx="78" cy="0" r="6" fill="{LIGHT}"/></g>
  </g>"""


def build_projects():
    netbio = project_card(
        "NetBio", "netbio.site",
        ["Todos tus enlaces en un solo lugar: tarjetas vCard,", "códigos QR y captura de clientes potenciales."],
        ["Next.js 16", "TypeScript", "Prisma", "Postgres", "Tailwind 4"], netbio_mock(), "🔗")
    porta = project_card(
        "Portafolio Web", "cesarbolivar.site",
        ["Mi perfil profesional, interactivo y bilingüe,", "con animaciones fluidas."],
        ["React 19", "Vite", "TypeScript", "Tailwind 4", "Framer Motion"], portfolio_mock(), "💼")
    return {"project-netbio.svg": netbio, "project-portfolio.svg": porta}


# --------------------------------------------------------------------- SECCIONES Y PIE
def section_title(text, sub):
    W, H = 1600, 110
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
{style(".ln{animation:grow 1.4s cubic-bezier(.2,.8,.2,1) backwards;transform-origin:center;transform-box:fill-box} @keyframes grow{from{transform:scaleX(0)}}")}
<line class="ln" x1="80" y1="55" x2="560" y2="55" stroke="url(#gL)" stroke-width="2"/>
<line class="ln" x1="1040" y1="55" x2="1520" y2="55" stroke="url(#gR)" stroke-width="2"/>
<defs><linearGradient id="gL"><stop offset="0" stop-color="{ACCENT}" stop-opacity="0"/><stop offset="1" stop-color="{ACCENT}"/></linearGradient>
<linearGradient id="gR"><stop offset="0" stop-color="{ACCENT}"/><stop offset="1" stop-color="{ACCENT}" stop-opacity="0"/></linearGradient></defs>
<text class="m" x="800" y="40" font-size="16" fill="{ACCENT}" text-anchor="middle" letter-spacing="5">{sub}</text>
<text class="s" x="800" y="80" font-size="38" font-weight="800" fill="{TEXT}" text-anchor="middle" style="font-family:{FONT}">{text}</text>
</svg>
"""


def build_sections():
    return {
        "title-projects.svg": section_title("Proyectos destacados", "01 · LO QUE CONSTRUYO"),
        "title-stack.svg": section_title("Stack tecnológico", "02 · MIS HERRAMIENTAS"),
        "title-activity.svg": section_title("Actividad en GitHub", "03 · CÓDIGO EN NÚMEROS"),
    }


def build_footer():
    W, H = 1600, 220
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
{style(".w1{animation:wave 9s ease-in-out infinite alternate} .w2{animation:wave 13s ease-in-out infinite alternate-reverse} @keyframes wave{from{transform:translateX(-60px)}to{transform:translateX(60px)}}")}
<defs><linearGradient id="gF" x1="0" x2="1"><stop offset="0" stop-color="{DEEP}"/><stop offset="1" stop-color="{ACCENT}"/></linearGradient></defs>
<path class="w2" d="M-80 120 C200 60 420 170 760 110 S1300 60 1680 120 V220 H-80Z" fill="{DEEP}" opacity=".55"/>
<path class="w1" d="M-80 150 C260 100 520 200 820 140 S1340 100 1680 150 V220 H-80Z" fill="url(#gF)" opacity=".9"/>
<text class="s" x="800" y="200" font-size="22" font-weight="700" fill="{TEXT}" text-anchor="middle" style="font-family:{FONT}">Construyamos algo juntos ✦</text>
</svg>
"""


def build_all():
    out = {"hero.svg": build_hero(), "footer.svg": build_footer()}
    out.update(build_projects())
    out.update(build_sections())
    return out
