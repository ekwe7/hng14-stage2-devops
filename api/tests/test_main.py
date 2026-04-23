import pytest
from fastapi.testclient import TestClient
import fakeredis

# Mock Redis BEFORE importing the app
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

import api.main
api.main.r = fakeredis.FakeRedis(decode_responses=True)

from api.main import app

client = TestClient(app)

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

def test_create_job():
    response = client.post("/jobs")
    assert response.status_code == 200
    data = response.json()
    assert "job_id" in data

def test_get_job_not_found():
    response = client.get("/jobs/nonexistent")
    assert response.status_code == 200
    assert response.json()["error"] == "not found"

def test_job_status_flow():
    # Create job
    res = client.post("/jobs")
    job_id = res.json()["job_id"]
    # Initially queued
    res = client.get(f"/jobs/{job_id}")
    assert res.json()["status"] == "queued"
    # Simulate worker completion
    api.main.r.hset(f"job:{job_id}", "status", "completed")
    res = client.get(f"/jobs/{job_id}")
    assert res.json()["status"] == "completed"
