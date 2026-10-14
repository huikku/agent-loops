#!/usr/bin/env python3
"""mock_backend_api.py: Simulates a real-world enterprise backend API with quirks.
Runs on localhost:8765.
"""
from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import urllib.parse
import threading

class MockAPIHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        pass  # Suppress default noisy console logs

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        params = urllib.parse.parse_qs(parsed.query)

        if parsed.path == "/api/v1/inventory":
            # Quirk 1: Limit silently clamps at 50 even if user asked for 200
            requested_limit = int(params.get("limit", [50])[0])
            effective_limit = min(requested_limit, 50)
            status_filter = params.get("status", ["all"])[0]

            items = [
                {"id": 1, "item": "Rapid Diagnostic Test Kits", "qty": 450, "status": "active", "clinic_id": "C-12"},
                {"id": 2, "item": "Artemether/Lumefantrine 20/120mg", "qty": 1200, "status": "active", "clinic_id": "C-12"},
                {"id": 3, "item": "Legacy PPE Masks (Expired 2018)", "qty": 80, "status": "archived", "clinic_id": "C-12"},
                {"id": 4, "item": "Amoxicillin 250mg Suspension", "qty": 310, "status": "active", "clinic_id": "C-14"},
            ]

            if status_filter != "all":
                items = [i for i in items if i["status"] == status_filter]

            response_data = {
                "count": len(items[:effective_limit]),
                "requested_limit": requested_limit,
                "effective_limit": effective_limit,
                "data": items[:effective_limit]
            }
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(response_data).encode("utf-8"))

        elif parsed.path == "/api/v1/metrics":
            # Quirk 2: Missing district_id causes 500 server error
            if "district_id" not in params:
                self.send_response(500)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"error": "InternalServerError: NullPointer district_id"}).encode("utf-8"))
                return

            district_id = params["district_id"][0]
            metrics = {
                "district_id": district_id,
                "malaria_positivity_rate": "14.2%",
                "reporting_clinics": ["C-12", "C-14"],
                "stockout_alerts": 0
            }
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(metrics).encode("utf-8"))
        else:
            self.send_response(404)
            self.end_headers()

def run_server(port=8765):
    server = HTTPServer(("localhost", port), MockAPIHandler)
    server.serve_forever()

if __name__ == "__main__":
    print("Mock API running on http://localhost:8765...")
    run_server()
