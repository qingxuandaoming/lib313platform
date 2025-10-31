import os
import uuid
import requests
from datetime import datetime

BASE_URL = os.environ.get("API_BASE_URL", "http://localhost:8000/api/v1")


def create_member_for_speaker():
    payload = {
        "name": f"分享会讲者-{uuid.uuid4().hex[:6]}",
        "student_id": uuid.uuid4().hex[:10],
        "grade": 2022,
        "major": "信息工程",
        "role": "member",
    }
    resp = requests.post(f"{BASE_URL}/members", json=payload)
    assert resp.status_code == 201, resp.text
    return resp.json()["id"]


def test_session_crud_flow():
    speaker_id = create_member_for_speaker()

    # Create
    payload = {
        "session_number": 1,
        "semester": "2024秋",
        "title": f"主题-{uuid.uuid4().hex[:6]}",
        "description": "分享会介绍",
        "speaker_id": speaker_id,
        "session_date": datetime.now().isoformat(),
        "location": "会议室A",
    }
    resp = requests.post(f"{BASE_URL}/sessions", json=payload)
    assert resp.status_code == 201, resp.text
    session = resp.json()
    session_id = session["id"]

    # Get
    get_resp = requests.get(f"{BASE_URL}/sessions/{session_id}")
    assert get_resp.status_code == 200, get_resp.text
    assert get_resp.json()["speaker_id"] == speaker_id

    # List
    list_resp = requests.get(f"{BASE_URL}/sessions", params={"semester": payload["semester"]})
    assert list_resp.status_code == 200, list_resp.text
    data = list_resp.json()
    assert data["total"] >= 1

    # Update
    update_payload = {"title": "更新后的主题", "cover_image": "http://example.com/cover.png"}
    upd_resp = requests.put(f"{BASE_URL}/sessions/{session_id}", json=update_payload)
    assert upd_resp.status_code == 200, upd_resp.text
    updated = upd_resp.json()
    assert updated["title"] == "更新后的主题"
    assert updated.get("cover_image") == "http://example.com/cover.png"

    # Delete
    del_resp = requests.delete(f"{BASE_URL}/sessions/{session_id}")
    assert del_resp.status_code == 204, del_resp.text

    # Confirm 404
    not_found = requests.get(f"{BASE_URL}/sessions/{session_id}")
    assert not_found.status_code == 404, not_found.text