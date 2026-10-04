import sys
import os
import json
from http.server import BaseHTTPRequestHandler

# Allow importing src/ modules from the project root
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            content_length = int(self.headers.get("Content-Length", 0))
            body = json.loads(self.rfile.read(content_length))
            industry = body.get("industry", "SaaS")

            from src.crew import run_crew

            paths = run_crew(industry)

            with open(paths["swot"], "r", encoding="utf-8") as f:
                swot = f.read()
            with open(paths["brief"], "r", encoding="utf-8") as f:
                brief = f.read()

            self._respond(200, {"swot": swot, "brief": brief})

        except Exception as e:
            self._respond(500, {"error": str(e)})

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def _respond(self, status: int, data: dict):
        body = json.dumps(data).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format, *args):
        pass
