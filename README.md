# Student Management API

A Flask REST API for managing student records with SQLite database, deployed on Render.

## Upgrade (v2.0)
- Added SQLite database for persistent data storage
- Deployed on Render with Gunicorn
- Full CRUD operations

## API Endpoints

| Method | Endpoint | Purpose |
|--------|----------|---------|
| POST | `/students` | Add student(s) |
| GET | `/students` | Get all students |
| GET | `/students/<name>` | Get specific student |
| PUT | `/students/<name>` | Update marks |
| DELETE | `/students/<name>` | Delete student |

## Installation

```bash
pip install -r requirements.txt
```

## Grade Scale
- A: > 90 | B: > 80 | C: > 70 | D: > 60 | E: > 34 | FAIL: ≤ 34

## Tech Stack
Flask | SQLite | Gunicorn | Render
