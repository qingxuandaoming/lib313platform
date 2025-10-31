import os
import requests

BASE_URL = os.environ.get("API_BASE_URL", "http://localhost:8000/api/v1")


def test_stats_endpoint():
    resp = requests.get(f"{BASE_URL}/stats")
    assert resp.status_code == 200, f"stats failed: {resp.text}"
    data = resp.json()
    for key in ["members", "projects", "sessions", "devices", "files"]:
        assert key in data
        assert isinstance(data[key], int)