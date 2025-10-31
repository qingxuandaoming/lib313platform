import os
import requests

BASE_URL = os.environ.get("API_BASE_URL", "http://localhost:8000/api/v1")


def test_login_and_me():
    # 使用默认管理员凭据登录
    payload = {"username": "admin", "password": "admin123"}
    resp = requests.post(f"{BASE_URL}/auth/login", json=payload)
    assert resp.status_code == 200, f"login failed: {resp.text}"
    data = resp.json()
    assert "access_token" in data

    # 使用token访问 /me
    token = data["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    me = requests.get(f"{BASE_URL}/auth/me", headers=headers)
    assert me.status_code == 200, f"/me failed: {me.text}"
    me_data = me.json()
    assert me_data.get("username") == "admin"