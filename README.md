# 🚀 TaskFlow AI

### AI-Assisted Task Management Dashboard

TaskFlow AI is a full-stack task management application built with **FastAPI, SQLite, SQLAlchemy, HTML, CSS, JavaScript, and AI-assisted task analysis**.

It allows users to create, manage, search, filter, sort, complete, edit, and delete tasks. The application also includes an **AI Quick Add** feature that converts natural-language task descriptions into structured task information.

---

## ✨ Features

### 🤖 AI Quick Add

Describe a task in simple natural language and AI analyzes it to generate:

- Task title
- Description
- Priority
- Category
- Project ID
- Due date

Example:

> Complete my Python assignment tomorrow with high priority.

AI converts the input into structured task information that can be reviewed before creating the task.

---

### 📋 Task Management

- Create new tasks
- Edit existing tasks
- Delete tasks
- Mark tasks as completed
- Mark completed tasks as pending
- Task descriptions
- Optional Project ID
- Priority levels
- Due dates
- Overdue task detection

---

### 🔎 Search & Filtering

Search tasks by:

- Title
- Description

Filter tasks by:

- All
- Pending
- Completed
- High Priority
- Medium Priority
- Low Priority

---

### 📊 Sorting

Tasks can be sorted using:

- Priority
- Due Date

The project also implements custom algorithms including:

- Insertion Sort
- Linear Search
- Binary Search

---

### 📈 Dashboard Statistics

The dashboard displays:

- Total Tasks
- Pending Tasks
- Completed Tasks
- High Priority Tasks

---

## 🧠 Algorithms Engine

TaskFlow AI includes a custom algorithms module.

### Insertion Sort

Used for task sorting.

### Linear Search

Used for sequential task searching.

### Binary Search

Used for efficient searching on sorted data.

### Benchmark

The backend provides a benchmark endpoint to evaluate sorting/searching performance.

---

# 🛠️ Tech Stack

## Frontend

- HTML5
- CSS3
- JavaScript
- LocalStorage
- Fetch API
- Responsive Design

## Backend

- Python
- FastAPI
- Uvicorn
- SQLAlchemy
- SQLite
- Pydantic

## AI

- AI-assisted task analysis
- Natural-language task processing
- Automatic priority and due-date extraction

## Database

- SQLite
- SQLAlchemy ORM

---

# 📁 Project Structure

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
│   │   │
│   │   ├── routes/
│   │   │   ├── tasks.py
│   │   │   ├── users.py
│   │   │   ├── projects.py
│   │   │   └── ai.py
│   │   │
│   │   └── utils/
│   │       └── algorithms.py
│   │
│   ├── requirements.txt
│   └── taskflow.db
│
├── frontend/
│   ├── index.html
│   ├── style.css
│   └── script.js
│
├── .gitignore
└── README.md