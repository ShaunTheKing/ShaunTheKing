"""Generates the dark, Apple-style SVG cards used by README.md.

Edit the content below and run:  python3 build.py
"""
from pathlib import Path
from xml.sax.saxutils import escape

OUT = Path(__file__).parent / "assets"
FONT = "-apple-system, BlinkMacSystemFont, 'SF Pro Display', 'Segoe UI', 'Helvetica Neue', Helvetica, Arial, sans-serif"

INK = "#f5f5f7"
INK_2 = "#a1a1a6"
INK_3 = "#86868b"
TILE = "#000000"
TILE_2 = "#1d1d1f"
CHIP = "#2c2c2e"
BLUE = "#2997ff"
ORANGE = "#f56300"

STYLE = f"""
  <style>
    text {{ font-family: {FONT}; }}
    .fade {{ opacity: 0; animation: up .9s cubic-bezier(.2,.8,.2,1) forwards; }}
    .d1 {{ animation-delay: .1s; }} .d2 {{ animation-delay: .25s; }}
    .d3 {{ animation-delay: .4s; }} .d4 {{ animation-delay: .55s; }}
    @keyframes up {{ from {{ opacity: 0; transform: translateY(12px); }} to {{ opacity: 1; transform: none; }} }}
    @media (prefers-reduced-motion: reduce) {{ .fade {{ animation: none; opacity: 1; }} }}
  </style>"""

GRADS = """
  <defs>
    <linearGradient id="g" x1="0" x2="1" y1="0" y2="0">
      <stop offset="0" stop-color="#2997ff"/><stop offset="1" stop-color="#a259ff"/>
    </linearGradient>
    <radialGradient id="glowA" cx="0.15" cy="0.3" r="0.55">
      <stop offset="0" stop-color="#2997ff" stop-opacity="0.22"/><stop offset="1" stop-color="#2997ff" stop-opacity="0"/>
    </radialGradient>
    <radialGradient id="glowB" cx="0.88" cy="0.75" r="0.55">
      <stop offset="0" stop-color="#a259ff" stop-opacity="0.20"/><stop offset="1" stop-color="#a259ff" stop-opacity="0"/>
    </radialGradient>
  </defs>"""


def text_w(s, size):
    """Rough rendered width of s in a system sans-serif."""
    return len(s) * size * 0.54


def svg(w, h, body):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">'
            f"{STYLE}{GRADS}\n{body}\n</svg>\n")


def t(x, y, s, size, fill, weight=400, anchor="start", cls="", extra=""):
    c = f' class="{cls}"' if cls else ""
    return (f'<text x="{x}" y="{y}" font-size="{size}" font-weight="{weight}" fill="{fill}" '
            f'text-anchor="{anchor}" letter-spacing="-0.02em"{c}{extra}>{escape(s)}</text>')


def chips(x, y, items, size=13, max_x=None):
    out, cx = [], x
    for it in items:
        w = text_w(it, size) + 20
        if max_x and cx + w > max_x:
            cx, y = x, y + 34
        out.append(f'<rect x="{cx}" y="{y}" width="{w:.0f}" height="26" rx="13" fill="{CHIP}"/>')
        out.append(t(cx + w / 2, y + 17.5, it, size, INK_2, anchor="middle"))
        cx += w + 8
    chips.last_y = y
    return "\n".join(out)


def hero():
    w, h = 840, 400
    body = f"""
<rect width="{w}" height="{h}" rx="28" fill="{TILE}"/>
<rect width="{w}" height="{h}" rx="28" fill="url(#glowA)"/>
<rect width="{w}" height="{h}" rx="28" fill="url(#glowB)"/>
{t(w/2, 112, "Shaun Salvador Andrade", 21, INK_3, 600, "middle", "fade d1")}
{t(w/2, 186, "Software that thinks.", 60, INK, 700, "middle", "fade d2")}
{t(w/2, 256, "Built to ship.", 60, "url(#g)", 700, "middle", "fade d3")}
{t(w/2, 314, "CS @ UMBC  ·  Multi-agent systems  ·  Model fine-tuning  ·  ViT research", 17, INK_2, 500, "middle", "fade d4")}
"""
    return svg(w, h, body)


def stats():
    w, h = 840, 150
    items = [("250+", "model downloads"), ("115k+", "loans · SQL risk modeling"),
             ("625+", "tests written"), ("3.8", "GPA at UMBC")]
    col = w / len(items)
    parts = [f'<rect width="{w}" height="{h}" rx="28" fill="{TILE_2}"/>']
    for i, (num, label) in enumerate(items):
        cx = col * i + col / 2
        parts.append(t(cx, 78, num, 42, INK, 600, "middle", f"fade d{i+1}"))
        parts.append(t(cx, 108, label, 13, INK_2, 400, "middle", f"fade d{i+1}"))
        if i:
            parts.append(f'<rect x="{col*i:.0f}" y="40" width="1" height="70" fill="#38383a"/>')
    return svg(w, h, "\n".join(parts))


def section(title, sub):
    w, h = 840, 110
    body = (t(w/2, 58, title, 40, INK, 600, "middle", "fade d1") + "\n" +
            t(w/2, 92, sub, 17, INK_3, 400, "middle", "fade d2"))
    # Transparent background so it sits on GitHub's page; light text needs a dark plate.
    return svg(w, h, f'<rect width="{w}" height="{h}" rx="24" fill="{TILE}"/>\n{body}')


def card(tag, tag_color, title, lines, stack, link, glow=False):
    w, h = 412, 300
    p = 32
    parts = [f'<rect width="{w}" height="{h}" rx="28" fill="{TILE_2}"/>']
    if glow:
        parts.append(f'<rect width="{w}" height="{h}" rx="28" fill="url(#glowA)"/>')
        parts.append(f'<rect width="{w}" height="{h}" rx="28" fill="url(#glowB)"/>')
    parts.append(t(p, 50, tag, 13, tag_color, 600))
    parts.append(t(p, 92, title, 30, INK, 600))
    for i, ln in enumerate(lines):
        parts.append(t(p, 128 + i * 22, ln, 15, INK_2))
    parts.append(chips(p, 128 + len(lines) * 22 + 14, stack, max_x=w - p))
    parts.append(t(p, h - 30, link + "  ›", 15, BLUE))
    return svg(w, h, "\n".join(parts))


def toolkit():
    w = 840
    p = 40
    rows = [
        ("Languages", ["Python", "TypeScript", "SQL"]),
        ("Machine Learning", ["PyTorch", "Vision Transformers", "Fine-Tuning", "Computer Vision", "Hugging Face"]),
        ("Frameworks & Tools", ["React", "Node.js", "Electron", "Streamlit", "MySQL", "SQLite", "Git", "Linux", "Vercel"]),
    ]
    parts = [t(p, 58, "The toolkit.", 30, INK, 600)]
    y = 92
    for label, items in rows:
        parts.append(t(p, y + 17.5, label, 13, INK_3, 600))
        parts.append(chips(200, y, items, max_x=w - p))
        y = chips.last_y + 46
    h = y + 10
    parts.insert(0, f'<rect width="{w}" height="{h}" rx="28" fill="{TILE_2}"/>')
    return svg(w, h, "\n".join(parts))


def button(label, primary):
    size = 15
    w = int(text_w(label, size) + 44)
    h = 40
    if primary:
        shape = f'<rect width="{w}" height="{h}" rx="20" fill="#0071e3"/>'
        fill = "#ffffff"
    else:
        shape = f'<rect x="0.75" y="0.75" width="{w-1.5}" height="{h-1.5}" rx="19.25" fill="{TILE}" stroke="{BLUE}" stroke-width="1.5"/>'
        fill = BLUE
    return svg(w, h, shape + "\n" + t(w / 2, 25.5, label, size, fill, 500, "middle"))


def main():
    OUT.mkdir(exist_ok=True)
    files = {
        "hero.svg": hero(),
        "stats.svg": stats(),
        "work.svg": section("Featured work.", "Agents, models, and data — from research lab to production."),
        "whales.svg": card("In development · Oct 2026", ORANGE, "Whales.",
                           ["Local-first multi-agent workspace. Each",
                            "agent is an isolated Cordis context with",
                            "its own plugins, memory, skills and tools."],
                           ["TypeScript", "React", "Electron", "SQLite"], "View on GitHub", glow=True),
        "laya.svg": card("Machine Learning · 2026", INK_3, "Laya Browser Agent.",
                         ["Fine-tuned a 421M-param model on Mind2Web",
                          "to predict the next browser action. 74.3%",
                          "val accuracy · 250+ downloads."],
                         ["PyTorch", "Hugging Face", "Mind2Web"], "Model card"),
        "behaviorscope.svg": card("Research · UMBC", INK_3, "BehaviorScope‑X.",
                                  ["Trained a Vision Transformer to classify",
                                   "mouse behavior from video. 82.7% macro",
                                   "accuracy · bioRxiv preprint (2026)."],
                                  ["ViT", "PyTorch", "Computer Vision"], "View code"),
        "credit.svg": card("Data · Analytics", INK_3, "Credit Analytics.",
                           ["SQL-first KPIs, segmentation and risk-",
                            "return modeling across 115k+ real loans",
                            "and 30k credit-card clients."],
                           ["Python", "SQL", "DuckDB"], "View on GitHub"),
        "toolkit.svg": toolkit(),
        "btn-portfolio.svg": button("Portfolio", True),
        "btn-email.svg": button("Email", False),
        "btn-linkedin.svg": button("LinkedIn", False),
    }
    for name, content in files.items():
        (OUT / name).write_text(content)
    print("wrote", len(files), "files to", OUT)


if __name__ == "__main__":
    main()
