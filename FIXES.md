# FIXES.md

## API
- Hardcoded Redis host → environment variables
- Added `/health` endpoint
- Added graceful shutdown

## Worker
- Hardcoded Redis → environment + signal handlers
- Added error handling & retries

## Frontend
- Hardcoded API URL → `API_URL` env var
- Added `/health` endpoint
- Added SIGTERM handler
