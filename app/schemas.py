
from pydantic import BaseModel, Field


class StudentProfile(BaseModel):
    cgpa: float = Field(ge=0, le=5)
    programming_score: int = Field(ge=0, le=100)
    math_score: int = Field(ge=0, le=100)
    attendance_pct: int = Field(ge=0, le=100)
    data_interest: int = Field(ge=1, le=10)
    software_interest: int = Field(ge=1, le=10)
    ai_interest: int = Field(ge=1, le=10)
