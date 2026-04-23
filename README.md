# HNG14 Stage 2 DevOps – Job Processing System

## Prerequisites
- Docker & Docker Compose

## Run the stack
1. Clone this repo.
2. Copy `.env.example` to `.env` and adjust values.
3. Run `docker compose up --build`
4. Open `http://localhost:3000`

## Health checks
- API: `curl http://localhost:8000/health`
- Frontend: open browser or `curl http://localhost:3000/health`

## Stop
`docker compose down`
