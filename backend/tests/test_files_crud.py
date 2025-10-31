import os
import uuid
import requests

BASE_URL = os.environ.get("API_BASE_URL", "http://localhost:8000/api/v1")


def create_member_and_project():
    member_payload = {
        "name": f"文件成员-{uuid.uuid4().hex[:6]}",
        "student_id": uuid.uuid4().hex[:10],
        "grade": 2023,
        "role": "leader",
    }
    m_resp = requests.post(f"{BASE_URL}/members", json=member_payload)
    assert m_resp.status_code == 201, m_resp.text
    leader_id = m_resp.json()["id"]

    proj_payload = {
        "name": f"文件项目-{uuid.uuid4().hex[:6]}",
        "leader_id": leader_id,
        "status": "planning",
        "member_ids": [leader_id],
    }
    p_resp = requests.post(f"{BASE_URL}/projects", json=proj_payload)
    assert p_resp.status_code == 201, p_resp.text
    return p_resp.json()["id"]


def test_file_upload_update_download_delete_flow():
    project_id = create_member_and_project()

    # Upload
    files = {
        "file": ("hello.txt", b"Hello File", "text/plain"),
    }
    # FastAPI 在 UploadFile 伴随的其他参数未标注 Form 时按查询参数解析
    params = {"project_id": project_id, "description": "测试文件上传"}
    resp = requests.post(f"{BASE_URL}/files/upload", files=files, params=params)
    assert resp.status_code == 201, resp.text
    file_item = resp.json()
    file_id = file_item["id"]

    # List filter
    list_resp = requests.get(f"{BASE_URL}/files", params={"project_id": project_id})
    assert list_resp.status_code == 200, list_resp.text
    assert any(f["id"] == file_id for f in list_resp.json()["data"])

    # Update
    update_payload = {"description": "更新描述", "original_filename": "hello_updated.txt"}
    upd_resp = requests.put(f"{BASE_URL}/files/{file_id}", json=update_payload)
    assert upd_resp.status_code == 200, upd_resp.text
    updated = upd_resp.json()
    assert updated["description"] == "更新描述"
    assert updated["original_filename"] == "hello_updated.txt"

    # Download
    dl_resp = requests.get(f"{BASE_URL}/files/{file_id}/download")
    assert dl_resp.status_code == 200, dl_resp.text

    # Stats
    stats_resp = requests.get(f"{BASE_URL}/files/stats")
    assert stats_resp.status_code == 200, stats_resp.text
    stats = stats_resp.json()
    for key in ["total_files", "total_size", "type_stats"]:
        assert key in stats

    # Delete
    del_resp = requests.delete(f"{BASE_URL}/files/{file_id}")
    assert del_resp.status_code == 204, del_resp.text

    # Confirm 404
    not_found = requests.get(f"{BASE_URL}/files/{file_id}")
    assert not_found.status_code == 404, not_found.text