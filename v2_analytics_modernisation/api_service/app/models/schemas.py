"""Pydantic schemas (placeholders).

The current API endpoints return SQLite rows directly.
If/when you want stricter typing and clearer OpenAPI docs, you can start using these schemas.
"""

from __future__ import annotations
from typing import Optional
from pydantic import BaseModel, Field


class Student(BaseModel):
    roll_no: int = Field(..., ge=1)
    full_name: str = Field(..., min_length=1)
    class_name: str = Field(..., min_length=1)
    status: str = Field(..., min_length=1)


class AttendanceRecord(BaseModel):
    roll_no: int = Field(..., ge=1)
    full_name: str = Field(..., min_length=1)
    attendance_date: str = Field(..., description="YYYY-MM-DD (string for simplicity)")
    present: bool
    class_name: str = Field(..., min_length=1)


class ResultRecord(BaseModel):
    roll_no: int = Field(..., ge=1)
    full_name: str = Field(..., min_length=1)
    internal_marks: Optional[float] = None
    external_marks: Optional[float] = None
    total_marks: Optional[float] = None
    pass_fail: Optional[str] = None
