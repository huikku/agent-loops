#!/usr/bin/env python3
"""mcp_server.py: Lightweight MCP server adapter sitting on top of an API.
Incorporates the Translation & Caveat Layer ('Cliff Notes for the Codebase')
to guarantee clean, zero-noise execution on real-world quirky APIs.
"""
import json
import os
import urllib.request
import urllib.parse
import sys

API_BASE_URL = "http://localhost:8765"
CAVEATS_PATH = os.path.join(os.path.dirname(__file__), "api_caveats.json")

def load_caveats() -> dict:
    if os.path.exists(CAVEATS_PATH):
        with open(CAVEATS_PATH, "r") as f:
            return json.load(f)
    return {}

CAVEATS = load_caveats()

# --- MCP Tool Handlers ---

def tool_consult_api_caveats(endpoint: str = None) -> dict:
    """Resource / Tool: Returns known API quirks, safe parameters, and limits."""
    if endpoint and endpoint in CAVEATS.get("endpoints", {}):
        return {endpoint: CAVEATS["endpoints"][endpoint]}
    return CAVEATS

def tool_get_clinic_inventory(limit: int = 50, status: str = "active") -> dict:
    """Tool: Fetches clinic stock and inventory levels.
    Automatically applies safe defaults (status=active, limit<=50) from caveat layer.
    """
    safe_limit = min(limit, 50)
    query = urllib.parse.urlencode({"limit": safe_limit, "status": status})
    url = f"{API_BASE_URL}/api/v1/inventory?{query}"

    req = urllib.request.Request(url)
    with urllib.request.urlopen(req, timeout=5) as response:
        data = json.loads(response.read().decode("utf-8"))

    # Enrich response with caveat metadata
    data["_caveat_applied"] = f"Clamped limit to safe max 50; filtered status='{status}'"
    return data

def tool_get_health_metrics(district_id: str) -> dict:
    """Tool: Fetches district-level epidemiological metrics.
    Prevents 500 error by validating mandatory district_id parameter.
    """
    if not district_id:
        return {"error": "ValidationError: district_id is required by the API."}

    query = urllib.parse.urlencode({"district_id": district_id})
    url = f"{API_BASE_URL}/api/v1/metrics?{query}"

    req = urllib.request.Request(url)
    with urllib.request.urlopen(req, timeout=5) as response:
        return json.loads(response.read().decode("utf-8"))

# Simple JSON-RPC Dispatcher
def dispatch_request(req_json: dict) -> dict:
    method = req_json.get("method")
    params = req_json.get("params", {})
    req_id = req_json.get("id")

    if method == "tools/list":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "tools": [
                    {
                        "name": "consult_api_caveats",
                        "description": "Inspect known quirks, safe defaults, and limitations of the backend API.",
                        "inputSchema": {"type": "object", "properties": {"endpoint": {"type": "string"}}}
                    },
                    {
                        "name": "get_clinic_inventory",
                        "description": "Query clinic stock levels. Defaults to active items and safe page sizes.",
                        "inputSchema": {"type": "object", "properties": {"limit": {"type": "integer"}, "status": {"type": "string"}}}
                    },
                    {
                        "name": "get_health_metrics",
                        "description": "Query epidemiological metrics for a specified district.",
                        "inputSchema": {"type": "object", "properties": {"district_id": {"type": "string"}}, "required": ["district_id"]}
                    }
                ]
            }
        }
    elif method == "tools/call":
        tool_name = params.get("name")
        args = params.get("arguments", {})

        if tool_name == "consult_api_caveats":
            res = tool_consult_api_caveats(args.get("endpoint"))
        elif tool_name == "get_clinic_inventory":
            res = tool_get_clinic_inventory(limit=args.get("limit", 50), status=args.get("status", "active"))
        elif tool_name == "get_health_metrics":
            res = tool_get_health_metrics(district_id=args.get("district_id"))
        else:
            return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32601, "message": f"Unknown tool: {tool_name}"}}

        return {"jsonrpc": "2.0", "id": req_id, "result": {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}}

    return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32600, "message": "Invalid Request"}}

if __name__ == "__main__":
    # If called via CLI with test json
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        print(json.dumps(dispatch_request({"method": "tools/list", "id": 1}), indent=2))
