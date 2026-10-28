"""Deterministic dependency integration checks; no external services are contacted."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import asyncio
import json
import os
from unittest.mock import patch
import httpx
os.environ.update(METABASE_API_KEY="synthetic-test-key", METABASE_URL="https://example.invalid")
import utils

async def validate():
    requests = []
    def handler(request):
        requests.append(request)
        assert request.headers["x-api-key"] == "synthetic-test-key"
        if request.url.path == "/api/error":
            return httpx.Response(403, json={"error": "denied"})
        return httpx.Response(200, json={"ok": True})
    client_type = httpx.AsyncClient
    with patch.object(utils.httpx, "AsyncClient", side_effect=lambda: client_type(transport=httpx.MockTransport(handler))):
        assert await utils.make_api_request("/api/example") == {"ok": True}
        assert await utils.make_api_request("/api/example", {"value": 1}) == {"ok": True}
        try:
            await utils.make_api_request("/api/error")
        except httpx.HTTPStatusError:
            pass
        else:
            raise AssertionError("HTTP errors must propagate")
    assert [r.method for r in requests] == ["GET", "POST", "GET"]
    assert json.loads(requests[1].content) == {"value": 1}
asyncio.run(validate())
print("HTTP transport, authentication, JSON and error behavior passed")
