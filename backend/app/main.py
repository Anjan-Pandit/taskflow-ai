from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import time

from .config import settings
from .database import Base, engine
from . import models

from .routes.tasks import router as task_router
from .routes.users import router as user_router
from .routes.projects import router as project_router


Base.metadata.create_all(bind=engine)


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION
)


# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5500",
        "http://127.0.0.1:5500"
    ],
    allow_credentials=True,
    allow_methods=[
        "GET",
        "POST",
        "PUT",
        "DELETE"
    ],
    allow_headers=[
        "Content-Type",
        "Authorization"
    ]
)


# Custom Middleware
@app.middleware("http")
async def log_request(request: Request, call_next):
    start_time = time.perf_counter()

    response = await call_next(request)

    process_time = (time.perf_counter() - start_time) * 1000

    print(
        f"{request.method} {request.url.path} "
        f"- {process_time:.2f} ms"
    )

    return response


@app.get("/")
def home():
    return {
        "message": "Welcome to TaskFlow AI",
        "version": settings.APP_VERSION
    }


app.include_router(task_router)
app.include_router(user_router)
app.include_router(project_router)