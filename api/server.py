import json
import os
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

from .domain import validate_request
from .repository import save_entry


class Handler(BaseHTTPRequestHandler):
    def headers_for(self, status: int) -> None:
        self.send_response(status)
        self.send_header('Access-Control-Allow-Origin', 'http://127.0.0.1:5173')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.send_header('Access-Control-Allow-Methods', 'POST,OPTIONS')
        self.send_header('Content-Type', 'application/json')
        self.end_headers()

    def do_OPTIONS(self) -> None:
        self.headers_for(204)

    def do_GET(self) -> None:
        self.headers_for(200)
        self.wfile.write(b'{"status":"ok"}')

    def do_POST(self) -> None:
        try:
            if self.path != '/entries':
                self.headers_for(404)
                return
            request = validate_request(json.loads(self.rfile.read(int(self.headers.get('Content-Length', '0')))))
            entry = save_entry(Path(os.environ['QUALIFICATION_DB']), request)
            self.headers_for(200)
            self.wfile.write(json.dumps(entry).encode())
        except (ValueError, KeyError, TypeError):
            self.headers_for(400)
            self.wfile.write(b'{"error":"invalid request"}')


if __name__ == '__main__':
    HTTPServer(('127.0.0.1', 8765), Handler).serve_forever()
