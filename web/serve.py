# -*- coding: utf-8 -*-
"""Sirve el dashboard con charset UTF-8 (la n y las tildes)."""

from __future__ import annotations

import sys
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8765


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT), **kwargs)

    def guess_type(self, path):
        ctype = super().guess_type(path)
        if ctype.startswith(("text/", "application/javascript", "application/json")):
            if "charset=" not in ctype:
                ctype = f"{ctype}; charset=utf-8"
        if path.endswith(".js"):
            return "text/javascript; charset=utf-8"
        if path.endswith(".json") or path.endswith(".geojson"):
            return "application/json; charset=utf-8"
        if path.endswith(".css"):
            return "text/css; charset=utf-8"
        if path.endswith(".html"):
            return "text/html; charset=utf-8"
        return ctype


if __name__ == "__main__":
    httpd = ThreadingHTTPServer(("127.0.0.1", PORT), Handler)
    print(f"Dashboard en http://127.0.0.1:{PORT}/")
    httpd.serve_forever()
