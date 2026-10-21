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

    def end_headers(self):
        self.send_header("Cache-Control", "no-store")
        super().end_headers()

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
    try:
        httpd = ThreadingHTTPServer(("127.0.0.1", PORT), Handler)
    except OSError as exc:
        print(f"El puerto {PORT} ya esta ocupado. Cierra la otra ventana o usa otro: python web/serve.py 8766", flush=True)
        print(exc, flush=True)
        sys.exit(1)
    print(f"Dashboard en http://127.0.0.1:{PORT}/", flush=True)
    print("Deja esta ventana abierta. Ctrl+C para parar.", flush=True)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nListo, servidor cerrado.")
        httpd.server_close()
