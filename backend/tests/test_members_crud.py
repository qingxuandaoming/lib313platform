import os
import uuid
import requests

BASE_URL = os.environ.get("API_BASE_URL", "http://localhost:8000/api/v1")


def make_member_payload():
    return {
        "name": f"测试成员-{uuid.uuid4().hex[:6]}",
        "student_id": uuid.uuid4().hex[:10],
        "grade": 2024,
        "major": "计算机科学",
        "role": "member",
        "email": "tester@example.com",
        "phone": "1234567890",
        "bio": "测试成员简介",
        "github": "https://github.com/tester",
    }


def test_member_crud_flow():
    # Create
    payload = make_member_payload()
    resp = requests.post(f"{BASE_URL}/members", json=payload)
    assert resp.status_code == 201, resp.text
    member = resp.json()
    member_id = member["id"]

    # Get
    get_resp = requests.get(f"{BASE_URL}/members/{member_id}")
    assert get_resp.status_code == 200, get_resp.text
    assert get_resp.json()["student_id"] == payload["student_id"]

    # List with search filter
    list_resp = requests.get(f"{BASE_URL}/members", params={"search": payload["student_id"]})
    assert list_resp.status_code == 200, list_resp.text
    data = list_resp.json()
    assert data["total"] >= 1
    assert any(m["id"] == member_id for m in data["data"])

    # Update
    update_payload = {"major": "软件工程", "avatar": "http://example.com/avatar.png"}
    upd_resp = requests.put(f"{BASE_URL}/members/{member_id}", json=update_payload)
    assert upd_resp.status_code == 200, upd_resp.text
    updated = upd_resp.json()
    assert updated["major"] == "软件工程"
    assert updated.get("avatar") == "http://example.com/avatar.png"

    # Delete
    del_resp = requests.delete(f"{BASE_URL}/members/{member_id}")
    assert del_resp.status_code == 204, del_resp.text

    # Confirm 404
    not_found = requests.get(f"{BASE_URL}/members/{member_id}")
    assert not_found.status_code == 404, not_found.text