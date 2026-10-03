import os
import json
from http.server import BaseHTTPRequestHandler, HTTPServer

NOTES = ["buy milk", "walk the dog", "write code"]


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/healthz":
            self._send(200, b"ok")
        elif self.path == "/":
            self._send(200, b"notes api")
        elif self.path == "/notes":
            body = json.dumps(NOTES).encode()
            self._send(200, body)
        else:
            self._send(404, b"not found")

    def do_POST(self):
        if self.path == "/notes":
            length = int(self.headers.get("Content-Length", 0))
            raw = self.rfile.read(length)
            try:
                data = json.loads(raw)
                text = data.get("text", "").strip()
            except Exception:
                text = ""
            if not text:
                self._send(400, b"text required")
                return
            NOTES.append(text)
            self._send(201, json.dumps(NOTES).encode())
        else:
            self._send(404, b"not found")

    def do_DELETE(self):
        if self.path.startswith("/notes/"):
            try:
                idx = int(self.path.split("/notes/")[1])
            except ValueError:
                self._send(400, b"invalid index")
                return
            if 0 <= idx < len(NOTES):
                NOTES.pop(idx)
                self._send(200, json.dumps(NOTES).encode())
            else:
                self._send(404, b"note not found")
        else:
            self._send(404, b"not found")

    def _send(self, code, body):
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, *a):
        pass


def make_server(port):
    return HTTPServer(("0.0.0.0", port), Handler)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "8080"))
    make_server(port).serve_forever()
