# Metadata-Driven UI Platform

Working reference project for defining UI metadata and rendering/submitting dynamic forms.

## Architecture decision
PostgreSQL is used. Relational columns support lifecycle/version/status queries, while JSONB stores evolving templates, fields, rules, actions, and submitted payloads. This gives stronger integrity and reporting than a document-only design while retaining schema flexibility.

## Run with Docker
```bash
docker compose up --build
```
Open:
- UI: http://localhost:5173/metadata
- API docs: http://localhost:8000/docs

Routes:
- `/metadata`: metadata designer
- `/runtime`: dynamic form renderer with metadata selector

Demo auth accepts every request. Send `Authorization: Bearer demo-token`; the frontend does this automatically.

## Local development
Backend:
```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```
Frontend:
```bash
cd frontend
npm install
npm run dev
```

## Included
- React, TypeScript, Material UI, React Router, Redux Toolkit
- FastAPI, SQLAlchemy async, Pydantic model validation, DI, CORS, auth dependency
- Metadata CRUD, metadata versioning, dynamic form submissions
- Input controls for string, number, date, time, datetime, picklist, user and translatable data
- Conditional field editor options and datasource-driven picklists
- JSON template, rules and actions editors
- PostgreSQL JSONB persistence

This is a secure starter, not a production security implementation. Replace the demo auth dependency, constrain CORS, add migrations/secrets management, audit logging and tenant isolation before production use.
