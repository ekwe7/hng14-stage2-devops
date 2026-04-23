import pytest
from fastapi.testclient import TestClient
import fakeredis

# Import the app module (but not the app instance yet)
import api.main

# Replace the real Redis client with a fake one *before* creating the TestClient
fake_redis = fakeredis.FakeRedis(decode_responses=True)
api.main.r = fake_redis

# Now import the app instance (it will use the fake redis)
from api.main import app

client = TestClient(app)

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert data.get("status") == "ok"

def test_create_job():
    fake_redis.flushall()  # clean slate
    response = client.post("/jobs")
    assert response.status_code == 200
    data = response.json()
    assert "job_id" in data
    job_id = data["job_id"]
    # Verify the job was stored in fake Redis
    status = fake_redis.hget(f"job:{job_id}", "status")
    assert status == "queued"

def test_get_job_not_found():
    response = client.get("/jobs/nonexistent")
    assert response.status_code == 200
    data = response.json()
    assert data.get("error") == "not found"

def test_get_job_found():
    # Manually insert a job into fake Redis
    job_id = "test-123"
    fake_redis.hset(f"job:{job_id}", "status", "completed")
    response = client.get(f"/jobs/{job_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["job_id"] == job_id
    assert data["status"] == "completed"