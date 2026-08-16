
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .database import Base, engine
from .routes.tasks import router as tasks_router
from .routes.users import router as users_router
from .routes.projects import router as projects_router
from .routes.ai import router as ai_router


# ==========================================
# CREATE DATABASE TABLES
# ==========================================

Base.metadata.create_all(bind=engine)


# ==========================================
# FASTAPI APP
# ==========================================

app = FastAPI(
    title="TaskFlow AI",
    version="1.0.0",
    description="AI-Assisted Task Management Dashboard"
)


# ==========================================
# CORS CONFIGURATION
# ==========================================

app.add_middleware(
    CORSMiddleware,

    allow_origins=[
        "https://taskflow-ai-frontend-tmd4.onrender.com",
        "http://localhost:5500",
        "http://127.0.0.1:5500",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"],
)


# ==========================================
# ROUTES
# ==========================================

app.include_router(
    tasks_router
)

app.include_router(
    users_router
)

app.include_router(
    projects_router
)

app.include_router(
    ai_router
)


# ==========================================
# ROOT ROUTE
# ==========================================

@app.get("/")
def root():
    return {
        "message": "TaskFlow AI Backend is running",
        "status": "success"
    }