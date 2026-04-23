import redis
import time
import os
import signal
import sys

# Read Redis configuration from environment variables
REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD", None)

# Create Redis client with auto‑decoding and connection pool
r = redis.Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    password=REDIS_PASSWORD,
    decode_responses=True,
    health_check_interval=30
)

# Graceful shutdown flag
running = True

def signal_handler(sig, frame):
    global running
    print("Shutting down worker gracefully...")
    running = False
    sys.exit(0)

signal.signal(signal.SIGTERM, signal_handler)
signal.signal(signal.SIGINT, signal_handler)

def process_job(job_id):
    print(f"Processing job {job_id}")
    time.sleep(2)  # simulate work
    r.hset(f"job:{job_id}", "status", "completed")
    print(f"Done: {job_id}")

def main():
    print(f"Worker started. Listening on Redis {REDIS_HOST}:{REDIS_PORT}")
    while running:
        try:
            # Block for up to 5 seconds for a new job
            result = r.brpop("job", timeout=5)
            if result:
                _, job_id = result  # job_id is already a string because decode_responses=True
                process_job(job_id)
        except redis.ConnectionError as e:
            print(f"Redis connection error: {e}. Retrying in 5 seconds...")
            time.sleep(5)
        except Exception as e:
            print(f"Unexpected error: {e}. Retrying in 1 second...")
            time.sleep(1)

if __name__ == "__main__":
    main()