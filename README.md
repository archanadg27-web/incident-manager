# 🚨 Incident Management System

A web-based incident management portal built with Flask, SQLite, and Docker.

## Tools Used
- Python 3.13
- Flask
- Flask-SQLAlchemy
- SQLite
- Bootstrap 5
- Docker

## Features
- Create, view, resolve and delete incidents
- Priority levels (High, Medium, Low)
- Assign incidents to team members
- Containerized with Docker

## How to Run Locally
```bash
python app.py
```

## How to Run with Docker
```bash
docker build -t incident-manager .
docker run -p 5000:5000 incident-manager
```
