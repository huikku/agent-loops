# Example 05: MCP API Connector with Caveat Layer

This example demonstrates how to build an **MCP Connector** on top of an existing REST API, featuring the **Translation & Caveat Layer** ("Cliff Notes for the Codebase") described by Jonathan Nesbitt and TJ Muehleman.

---

## Architecture Overview

```
[Agent Query] ──► [mcp_server.py] ──(Consults)──► [api_caveats.json]
                         │
                         ▼ (Clean, optimized request with zero trial-and-error)
                [mock_backend_api.py]
```

1. **`mock_backend_api.py`:** Simulates a production enterprise API (health records and clinic inventory) with realistic quirks (hidden row ceilings, timezone assumptions, required soft-delete filters).
2. **`api_caveats.json`:** The translation layer documenting known quirks, safe pagination bounds, and mandatory filter combinations.
3. **`mcp_server.py`:** A lightweight MCP server that exposes:
   - Tool `get_clinic_inventory`: Fetches equipment and medicine levels, automatically enforcing safe pagination and soft-delete filters from the caveat layer.
   - Tool `get_health_metrics`: Queries attendance/incident data with timezone normalization.
   - Resource `api://caveats`: Exposes the live quirk dictionary to the LLM so it can inspect limitations before planning complex workflows.
4. **`test_client.py`:** A client script simulating an agent session connecting to the MCP server.

---

## Running the Example

In a terminal, run the automated integration test:
```bash
python3 test_client.py
```

This starts the mock API in the background, spins up the MCP server, and executes:
1. Direct inspection of the `api://caveats` resource.
2. Invocation of `get_clinic_inventory` showing automatic pagination clamp and active-status filtering.
3. Cross-endpoint joining of clinic inventory with district health metrics.

