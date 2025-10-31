import os
import uuid
import requests
from datetime import date

BASE_URL = os.environ.get("API_BASE_URL", "http://localhost:8000/api/v1")


def create_member_for_duty():
    payload = {
        "name": f"值日成员-{uuid.uuid4().hex[:6]}",
        "student_id": uuid.uuid4().hex[:10],
        "grade": 2021,
        "major": "自动化",
        "role": "member",
    }
    resp = requests.post(f"{BASE_URL}/members", json=payload)
    assert resp.status_code == 201, resp.text
    return resp.json()["id"]


def test_duty_schedule_crud_flow():
    member_id = create_member_for_duty()

    # Create
    payload = {
        "member_id": member_id,
        "duty_date": date.today().isoformat(),
        "is_completed": False,
        "completion_notes": None,
    }
    resp = requests.post(f"{BASE_URL}/duty", json=payload)
    assert resp.status_code == 201, resp.text
    schedule = resp.json()
    schedule_id = schedule["id"]

    # Get
    get_resp = requests.get(f"{BASE_URL}/duty/{schedule_id}")
    assert get_resp.status_code == 200, get_resp.text
    assert get_resp.json()["member_id"] == member_id

    # List filter by date range
    list_resp = requests.get(f"{BASE_URL}/duty", params={"start_date": date.today().isoformat()})
    assert list_resp.status_code == 200, list_resp.text
    assert list_resp.json()["total"] >= 1

    # Update
    upd_payload = {"completion_notes": "已调整时间"}
    upd_resp = requests.put(f"{BASE_URL}/duty/{schedule_id}", json=upd_payload)
    assert upd_resp.status_code == 200, upd_resp.text
    assert upd_resp.json().get("completion_notes") == "已调整时间"

    # Complete
    complete_resp = requests.patch(f"{BASE_URL}/duty/{schedule_id}/complete", params={"completion_notes": "完成值日"})
    assert complete_resp.status_code == 200, complete_resp.text
    completed = complete_resp.json()
    assert completed["is_completed"] is True
    assert completed.get("completed_at") is not None

    # Delete
    del_resp = requests.delete(f"{BASE_URL}/duty/{schedule_id}")
    assert del_resp.status_code == 204, del_resp.text

    # Confirm 404
    not_found = requests.get(f"{BASE_URL}/duty/{schedule_id}")
    assert not_found.status_code == 404, not_found.text