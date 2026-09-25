from fastapi import FastAPI

from app.database import Base, engine

from app.models import (
    User,
    Doctor,
    Patient,
    Assignment
)

from app.routers import (
    auth,
    doctors,
    patients
)


Base.metadata.create_all(
    bind=engine
)


app = FastAPI(
    title="Doctor Patient Management System",
    description="FastAPI backend for managing doctors and patients",
    version="1.0.0"
)


app.include_router(
    auth.router
)

app.include_router(
    doctors.router
)

app.include_router(
    patients.router
)


@app.get("/")
def home():
    return {
        "message": "Doctor Patient Management API is running"
    }