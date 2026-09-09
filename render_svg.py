"""
render_svg.py

Builds dark_mode.svg and light_mode.svg from:
  - ascii_lines.txt   (output of build_ascii_art.py)
  - the static info block below (edit STATIC_LINES to taste)

Numeric GitHub stats are left as placeholder text with element ids
(commit_data, star_data, repo_data, etc.) so today.py can overwrite
them in place later, exactly like the reference template does.
"""

import html

ART_FONT_SIZE = 13
ART_LINE_HEIGHT = 17
ART_CHAR_WIDTH = 7.6
ART_X = 15
ART_Y0 = 30

INFO_FONT_SIZE = 15
INFO_LINE_HEIGHT = 20
INFO_X = 480
INFO_Y0 = 30

THEMES = {
    "light": {
        "bg": "#f6f8fa",
        "fg": "#24292f",
        "key": "#953800",
        "value": "#0a3069",
        "cc": "#c2cfde",
        "add": "#1a7f37",
        "del": "#cf222e",
        "art": "#24292f",
    },
    "dark": {
        "bg": "#0d1117",
        "fg": "#c9d1d9",
        "key": "#ffa657",
        "value": "#79c0ff",
        "cc": "#484f58",
        "add": "#3fb950",
        "del": "#f85149",
        "art": "#58a6ff",
    },
}


def load_ascii_lines(path="ascii_lines.txt"):
    with open(path) as f:
        lines = [l.rstrip("\n") for l in f.readlines()]
    while lines and not lines[0].strip():
        lines.pop(0)
    while lines and not lines[-1].strip():
        lines.pop()
    return lines


def esc(s):
    return html.escape(s, quote=False)


def build_art_tspans(lines, color):
    out = []
    y = ART_Y0
    for line in lines:
        out.append(f'<tspan x="{ART_X}" y="{y}">{esc(line) if line.strip() else " "}</tspan>')
        y += ART_LINE_HEIGHT
    height_used = y
    return "\n".join(out), height_used


# (key, value, id_prefix or None, extra) — kept close to a real neofetch/fastfetch block
STATIC_LINES = [
    ("header", "rishabh@black-bird7"),
    ("kv", "OS", "Arch Linux / Kali Linux"),
    ("kv", "Shell", "zsh"),
    ("kv", "Editor", "Neovim, VS Code"),
    ("kv_dyn", "GitHub Member Since", "uptime_data"),
    ("blank",),
    ("kv", "Focus.Security", "Offensive Sec, Reverse Engineering"),
    ("kv", "Focus.Systems", "Linux Internals, Binary Analysis"),
    ("kv", "Focus.Learning", "Satellite Mapping, Sec Research"),
    ("blank",),
    ("kv", "Languages.Programming", "C, C++, Python, Rust, Assembly"),
    ("kv", "Languages.Web", "HTML, CSS, JS, TS, React, Node"),
    ("kv", "Languages.Data", "MySQL, PostgreSQL, MongoDB, Redis"),
    ("section", "Contact"),
    ("kv", "Email", "Rishabhdev.2025@gmail.com"),
    ("kv", "Instagram", "@rishxbd"),
    ("kv", "Discord", "discord.gg/ED7Ms9fRYK"),
    ("kv", "GitHub", "black-bird7"),
    ("section", "GitHub Stats"),
    ("stats1",),
    ("stats2",),
    ("stats3",),
]


LINE_BUDGET = 63  # target character width of a stats line, keeps things inside the canvas


def rule(prefix_len):
    return "-" * max(4, LINE_BUDGET - prefix_len)


def dots(label_len, value_len, prefix_len=2):
    # ". " + key + ": " + dots + " " + value  ==  LINE_BUDGET chars
    n = max(2, LINE_BUDGET - prefix_len - label_len - 2 - value_len - 2)
    return " " + ("." * n) + " "


def build_info_tspans():
    out = []
    y = INFO_Y0
    for row in STATIC_LINES:
        kind = row[0]
        if kind == "header":
            out.append(f'<tspan x="{INFO_X}" y="{y}">{esc(row[1])}</tspan> {rule(len(row[1]) + 1)}')
        elif kind == "blank":
            out.append(f'<tspan x="{INFO_X}" y="{y}" class="cc">. </tspan>')
        elif kind == "section":
            out.append(f'<tspan x="{INFO_X}" y="{y}">- {esc(row[1])}</tspan> {rule(len(row[1]) + 3)}')
        elif kind == "kv":
            _, key, val = row
            d = dots(len(key), len(val))
            out.append(
                f'<tspan x="{INFO_X}" y="{y}" class="cc">. </tspan>'
                f'<tspan class="key">{esc(key)}</tspan>:'
                f'<tspan class="cc">{esc(d)}</tspan>'
                f'<tspan class="value">{esc(val)}</tspan>'
            )
        elif kind == "kv_dyn":
            _, key, elid = row
            out.append(
                f'<tspan x="{INFO_X}" y="{y}" class="cc">. </tspan>'
                f'<tspan class="key">{esc(key)}</tspan>:'
                f'<tspan class="cc" id="{elid}_dots">{esc(dots(len(key), 11))}</tspan>'
                f'<tspan class="value" id="{elid}">calculating...</tspan>'
            )
        elif kind == "stats1":
            out.append(
                f'<tspan x="{INFO_X}" y="{y}" class="cc">. </tspan>'
                f'<tspan class="key">Repos</tspan>:<tspan class="cc" id="repo_data_dots"> .... </tspan>'
                f'<tspan class="value" id="repo_data">0</tspan> '
                f'{{<tspan class="key">Contributed</tspan>: <tspan class="value" id="contrib_data">0</tspan>}} | '
                f'<tspan class="key">Stars</tspan>:<tspan class="cc" id="star_data_dots"> ... </tspan>'
                f'<tspan class="value" id="star_data">0</tspan>'
            )
        elif kind == "stats2":
            out.append(
                f'<tspan x="{INFO_X}" y="{y}" class="cc">. </tspan>'
                f'<tspan class="key">Commits</tspan>:<tspan class="cc" id="commit_data_dots"> ... </tspan>'
                f'<tspan class="value" id="commit_data">0</tspan> | '
                f'<tspan class="key">Followers</tspan>:<tspan class="cc" id="follower_data_dots"> ... </tspan>'
                f'<tspan class="value" id="follower_data">0</tspan>'
            )
        elif kind == "stats3":
            out.append(
                f'<tspan x="{INFO_X}" y="{y}" class="cc">. </tspan>'
                f'<tspan class="key">Lines of Code on GitHub</tspan>:'
                f'<tspan class="cc" id="loc_data_dots">. </tspan>'
                f'<tspan class="value" id="loc_data">0</tspan> ( '
                f'<tspan class="addColor" id="loc_add">0</tspan><tspan class="addColor">++</tspan>, '
                f'<tspan id="loc_del_dots"> </tspan>'
                f'<tspan class="delColor" id="loc_del">0</tspan><tspan class="delColor">--</tspan> )'
            )
        y += INFO_LINE_HEIGHT
    return "\n".join(out), y


def render(theme_name, art_lines):
    t = THEMES[theme_name]
    art_tspans, art_h = build_art_tspans(art_lines, t["art"])
    info_tspans, info_h = build_info_tspans()

    info_char_width = INFO_FONT_SIZE * 0.6
    width = int(INFO_X + LINE_BUDGET * info_char_width + 20)
    height = max(art_h, info_h) + 30

    return f'''<?xml version='1.0' encoding='UTF-8'?>
<svg xmlns="http://www.w3.org/2000/svg" font-family="ConsolasFallback,Consolas,monospace" width="{width}px" height="{height}px" font-size="{INFO_FONT_SIZE}px">
<style>
@font-face {{
src: local('Consolas'), local('Consolas Bold');
font-family: 'ConsolasFallback';
font-display: swap;
-webkit-size-adjust: 109%;
size-adjust: 109%;
}}
.key {{fill: {t["key"]};}}
.value {{fill: {t["value"]};}}
.addColor {{fill: {t["add"]};}}
.delColor {{fill: {t["del"]};}}
.cc {{fill: {t["cc"]};}}
.ascii {{fill: {t["art"]}; font-size: {ART_FONT_SIZE}px;}}
text, tspan {{white-space: pre;}}
</style>
<rect width="{width}px" height="{height}px" fill="{t["bg"]}" rx="15"/>
<text x="{ART_X}" y="{ART_Y0}" class="ascii">
{art_tspans}
</text>
<text x="{INFO_X}" y="{INFO_Y0}" fill="{t["fg"]}">
{info_tspans}
</text>
</svg>
'''


if __name__ == "__main__":
    lines = load_ascii_lines()
    for theme in ("light", "dark"):
        svg = render(theme, lines)
        with open(f"{theme}_mode.svg", "w") as f:
            f.write(svg)
        print(f"wrote {theme}_mode.svg")
