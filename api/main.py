import os
from fastapi import FastAPI
import redis
import uuid

app = FastAPI()

# Read configuration from environment variables (with sensible defaults)
REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD", None)

# Create Redis connection with health check and decode responses
r = redis.Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    password=REDIS_PASSWORD,
    decode_responses=True,   # automatically decode bytes to str
    health_check_interval=30
)

@app.on_event("shutdown")
def shutdown():
    """Gracefully close Redis connection on app shutdown"""
    r.close()

@app.get("/health")
def health():
    """Health check endpoint for Docker HEALTHCHECK"""
    try:
        # Optionally ping Redis to verify connectivity
        r.ping()
        return {"status": "ok", "redis": "connected"}
    except redis.ConnectionError:
        return {"status": "degraded", "redis": "disconnected"}, 503

@app.post("/jobs")
def create_job():
    job_id = str(uuid.uuid4())
    r.lpush("job", job_id)
    r.hset(f"job:{job_id}", "status", "queued")
    return {"job_id": job_id}

@app.get("/jobs/{job_id}")
def get_job(job_id: str):
    status = r.hget(f"job:{job_id}", "status")
    if not status:
        return {"error": "not found"}
    return {"job_id": job_id, "status": status}