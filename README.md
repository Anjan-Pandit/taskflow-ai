# TaskFlow AI

## Full-Stack AI-Assisted Task Management Platform

TaskFlow AI is a full-stack task and project management platform built with FastAPI, SQLAlchemy, JavaScript, and a relational database.

The application allows users to create, update, delete, search, sort, and manage tasks. It also includes an Algorithms Engine for sorting/searching and an AI Quick Add feature that converts natural-language task descriptions into structured tasks.

---

# Features

## Core Task Management

- Create tasks
- List tasks
- Get task by ID
- Update tasks
- Delete tasks
- Mark tasks as completed/pending
- Task priority management
- Due-date support
- Project ID support
- Task statistics
- Search tasks
- Filter tasks
- Sort tasks
- Responsive dashboard
- LocalStorage caching

## Algorithms Engine

- Insertion Sort
- Binary Search
- Linear Search
- Priority sorting endpoint
- Exact-title search endpoint
- Comparison-count benchmarks
- Automated PASS/FAIL algorithm checks

## AI Quick Add

- Natural-language task input
- Deterministic rule-based parser
- Automatic priority detection
- Automatic due-date hint detection
- Automatic title extraction
- Zero API keys required
- Zero external API/network calls required

---

# Tech Stack

## Frontend

- HTML5
- CSS3
- JavaScript
- Fetch API
- LocalStorage

## Backend

- Python
- FastAPI
- Uvicorn
- SQLAlchemy
- Pydantic

## Database

- PostgreSQL in production
- SQLite for local development

---

# Project Structure

```text
TaskFlow AI/
│
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── database.py
│   │   ├── models.py
│   │   ├── schemas.py
│   │   ├── crud.py
│   │   ├── ai.py
│   │   ├── routers/
│   │   └── utils/
│   │
│   ├── requirements.txt
│   └── ...
│
├── frontend/
│   ├── index.html
│   ├── styles.css
│   └── script.js
│
├── README.md
└── .gitignore