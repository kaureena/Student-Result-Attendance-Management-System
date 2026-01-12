from __future__ import annotations
from fastapi import FastAPI
from .routes import students, attendance, results

app = FastAPI(title="Student Analytics API", version="0.1.0")

app.include_router(students.router, prefix="/students", tags=["students"])
app.include_router(attendance.router, prefix="/attendance", tags=["attendance"])
app.include_router(results.router, prefix="/results", tags=["results"])
