import os
import uuid
import requests
from datetime import datetime

BASE_URL = os.environ.get("API_BASE_URL", "http://localhost:8000/api/v1")


def test_device_crud_and_uniqueness():
    serial = f"SN-{uuid.uuid4().hex[:8]}"

    # Create
    payload = {
        "name": f"设备-{uuid.uuid4().hex[:6]}",
        "device_type": "computer",
        "brand": "Lenovo",
        "model": "ThinkPad",
        "serial_number": serial,
        "specifications": "16G RAM, 512G SSD",
        "status": "available",
        "location": "A-101",
        "purchase_date": datetime.now().isoformat(),
        "notes": "办公电脑",
    }
    resp = requests.post(f"{BASE_URL}/devices", json=payload)
    assert resp.status_code == 201, resp.text
    device = resp.json()
    device_id = device["id"]

    # Get
    get_resp = requests.get(f"{BASE_URL}/devices/{device_id}")
    assert get_resp.status_code == 200, get_resp.text
    assert get_resp.json()["serial_number"] == serial

    # List filter
    list_resp = requests.get(f"{BASE_URL}/devices", params={"device_type": "computer"})
    assert list_resp.status_code == 200, list_resp.text
    assert list_resp.json()["total"] >= 1

    # Update
    upd_payload = {"location": "A-102", "status": "in_use"}
    upd_resp = requests.put(f"{BASE_URL}/devices/{device_id}", json=upd_payload)
    assert upd_resp.status_code == 200, upd_resp.text
    updated = upd_resp.json()
    assert updated["location"] == "A-102"
    assert updated["status"] == "in_use"

    # Duplicate serial_number should fail
    dup_payload = {
        "name": "设备-重复",
        "device_type": "computer",
        "serial_number": serial,
    }
    dup_resp = requests.post(f"{BASE_URL}/devices", json=dup_payload)
    assert dup_resp.status_code == 400, dup_resp.text

    # Delete
    del_resp = requests.delete(f"{BASE_URL}/devices/{device_id}")
    assert del_resp.status_code == 204, del_resp.text

    # Confirm 404
    not_found = requests.get(f"{BASE_URL}/devices/{device_id}")
    assert not_found.status_code == 404, not_found.text