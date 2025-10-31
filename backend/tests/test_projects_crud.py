import os
import uuid
import requests

BASE_URL = os.environ.get("API_BASE_URL", "http://localhost:8000/api/v1")


def create_member_for_leader():
    payload = {
        "name": f"项目负责人-{uuid.uuid4().hex[:6]}",
        "student_id": uuid.uuid4().hex[:10],
        "grade": 2023,
        "major": "软件工程",
        "role": "leader",
    }
    resp = requests.post(f"{BASE_URL}/members", json=payload)
    assert resp.status_code == 201, resp.text
    return resp.json()["id"]


def test_project_crud_flow():
    # Prepare leader
    leader_id = create_member_for_leader()

    # Create project
    payload = {
        "name": f"项目-{uuid.uuid4().hex[:6]}",
        "description": "项目描述",
        "status": "planning",
        "leader_id": leader_id,
        "github_url": "https://github.com/org/repo",
        "demo_url": "https://demo.example.com",
        "tags": "AI,Web",
        "member_ids": [leader_id],
    }
    resp = requests.post(f"{BASE_URL}/projects", json=payload)
    assert resp.status_code == 201, resp.text
    project = resp.json()
    project_id = project["id"]

    # Get
    get_resp = requests.get(f"{BASE_URL}/projects/{project_id}")
    assert get_resp.status_code == 200, get_resp.text
    assert get_resp.json()["leader_id"] == leader_id

    # List with search filter
    list_resp = requests.get(f"{BASE_URL}/projects", params={"search": payload["name"]})
    assert list_resp.status_code == 200, list_resp.text
    data = list_resp.json()
    assert data["total"] >= 1
    assert any(p["id"] == project_id for p in data["data"])

    # Update
    update_payload = {"description": "更新后的项目描述", "status": "in_progress", "cover_image": "http://example.com/cover.png"}
    upd_resp = requests.put(f"{BASE_URL}/projects/{project_id}", json=update_payload)
    assert upd_resp.status_code == 200, upd_resp.text
    updated = upd_resp.json()
    assert updated["description"] == "更新后的项目描述"
    assert updated["status"] == "in_progress"
    assert updated.get("cover_image") == "http://example.com/cover.png"

    # Add member to project (re-use leader_id)
    add_resp = requests.post(f"{BASE_URL}/projects/{project_id}/members/{leader_id}")
    # May be 400 if already added in create; accept 201 or 400
    assert add_resp.status_code in (201, 400), add_resp.text

    # Remove member
    del_member_resp = requests.delete(f"{BASE_URL}/projects/{project_id}/members/{leader_id}")
    assert del_member_resp.status_code in (204, 404), del_member_resp.text

    # Delete project
    del_resp = requests.delete(f"{BASE_URL}/projects/{project_id}")
    assert del_resp.status_code == 204, del_resp.text

    # Confirm 404
    not_found = requests.get(f"{BASE_URL}/projects/{project_id}")
    assert not_found.status_code == 404, not_found.text