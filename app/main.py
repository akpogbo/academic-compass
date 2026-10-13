
from pathlib import Path

import joblib
import pandas as pd
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.recommendations import generate_advice
from app.schemas import StudentProfile

BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_PATH = BASE_DIR / "models" / "academic_advisor_model.pkl"
STATIC_DIR = BASE_DIR / "app" / "static"

app = FastAPI(
    title="Academic Compass API",
    description="AI-assisted academic and career pathway recommendations.",
    version="1.0.0",
)

model = joblib.load(MODEL_PATH)

app.mount(
    "/static",
    StaticFiles(directory=STATIC_DIR),
    name="static",
)


@app.get("/")
def home():
    return FileResponse(STATIC_DIR / "index.html")


@app.get("/health")
def health():
    return {"status": "healthy", "model_loaded": model is not None}


@app.post("/predict")
def predict(profile: StudentProfile):
    student_data = pd.DataFrame([profile.model_dump()])
    pathway = str(model.predict(student_data)[0])
    advice = generate_advice(profile, pathway)

    return {
        "recommendation": pathway.replace("_", " ").title(),
        "explanation": advice["explanation"],
        "strengths": advice["strengths"],
        "next_steps": advice["next_steps"],
    }
