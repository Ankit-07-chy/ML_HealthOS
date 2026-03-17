# Dockerfile Implementation TODO

## Completed
- [x] Create Dockerfile: python:3.13-slim, pip install requirements.txt, copy code, non-root user, expose 8000, CMD uvicorn api.api_call:app --host 0.0.0.0 --port 8000.

## Remaining Steps
- [x] Create .dockerignore (optional).
- [x] Create .env.example with GOOGLE_API_KEY placeholder.
- [ ] Build image: `docker build -t healthos-ml .`
- [ ] Run container: `docker run -p 8000:8000 --env-file .env healthos-ml`
- [ ] Test: `curl http://localhost:8000/health`
- [ ] Optional: docker-compose.yml for easier management.
