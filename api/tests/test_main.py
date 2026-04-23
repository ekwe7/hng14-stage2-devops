from fastapi.testclient import TestClient
import fakeredis

# Mock Redis BEFORE importing the app
import api.main
api.main.r = fakeredis.FakeRedis(decode_responses=True)

from api.main import app  # noqa: E402

client = TestClient(app)


def test_health():
    res = client.get("/health")
    assert res.status_code == 200
    assert res.json()["status"] == "ok"


def test_create_job():
    res = client.post("/jobs")
    assert res.status_code == 200
    assert "job_id" in res.json()


def test_get_job_not_found():
    res = client.get("/jobs/nonexistent")
    assert res.status_code == 200
    assert res.json()["error"] == "not found"


def test_job_status_flow():
    res = client.post("/jobs")
    job_id = res.json()["job_id"]
    res = client.get(f"/jobs/{job_id}")
    assert res.json()["status"] == "queued"
    api.main.r.hset(f"job:{job_id}", "status", "completed")
    res = client.get(f"/jobs/{job_id}")
    assert res.json()["status"] == "completed"
