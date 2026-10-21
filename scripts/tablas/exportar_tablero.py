# -*- coding: utf-8 -*-
"""Arma web/tablero.html: un solo archivo para mandar o abrir.

No hace falta servidor ni Railway. El mapa pide internet (Leaflet + teselas).
Si cambian JSON o el JS: vuelve a correr este script.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from rutas import TABLERO, WEB, WEB_DATA

JS_ORDER = ("config.js", "state.js", "data.js", "filters.js", "map.js", "panel.js", "main.js")
JSON_KEYS = (
    ("meta", "meta.json"),
    ("departamentos", "departamentos.json"),
    ("enares", "enares.json"),
    ("cem", "cem.json"),
    ("perfiles", "perfiles.json"),
    ("vivienda", "vivienda.json"),
    ("geo_deptos", "peru_departamentos.geojson"),
    ("geo_cem", "cem.geojson"),
)


def strip_module(src: str) -> str:
    out = []
    for line in src.splitlines():
        if re.match(r"^import\s+", line):
            continue
        line = re.sub(r"^export\s+async\s+function\s+", "async function ", line)
        line = re.sub(r"^export\s+function\s+", "function ", line)
        line = re.sub(r"^export\s+const\s+", "const ", line)
        out.append(line)
    return "\n".join(out)


def dumps(obj) -> str:
    text = json.dumps(obj, ensure_ascii=False, separators=(",", ":"))
    return text.replace("<", "\\u003c")


def main() -> None:
    pack = {}
    for key, name in JSON_KEYS:
        pack[key] = json.loads((WEB_DATA / name).read_text(encoding="utf-8"))
    css = (WEB / "css" / "app.css").read_text(encoding="utf-8")
    js = "\n\n".join(strip_module((WEB / "js" / name).read_text(encoding="utf-8")) for name in JS_ORDER)
    html = (WEB / "index.html").read_text(encoding="utf-8")
    html = re.sub(
        r'<link rel="stylesheet" href="css/app\.css[^"]*">',
        lambda _: f"<style>\n{css}\n</style>",
        html,
        count=1,
    )
    html = re.sub(
        r'<script type="module" src="js/main\.js[^"]*"></script>',
        lambda _: (
            f"<script>globalThis.__DASHBOARD__ = {dumps(pack)};</script>\n"
            f'<script type="module">\n{js}\n</script>'
        ),
        html,
        count=1,
    )
    TABLERO.write_text(html, encoding="utf-8")
    kb = TABLERO.stat().st_size / 1024
    print(f"Listo: {TABLERO} ({kb:.0f} KB). Ábrelo o mándalo; no necesita servidor.")


if __name__ == "__main__":
    main()
