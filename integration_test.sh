#!/bin/bash
set -e
JOB_ID=$(curl -s -X POST http://localhost:8000/jobs | jq -r .job_id)
echo "Job ID: $JOB_ID"
for i in {1..30}; do
  STATUS=$(curl -s http://localhost:8000/jobs/$JOB_ID | jq -r .status)
  echo "Status: $STATUS"
  if [ "$STATUS" = "completed" ]; then
    echo "Integration test passed"
    exit 0
  fi
  sleep 2
done
echo "Job did not complete within timeout"
exit 1
