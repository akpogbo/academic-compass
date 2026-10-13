
from pathlib import Path

import joblib
import pandas as pd
import streamlit as st

# Application configuration
st.set_page_config(
    page_title="Academic Compass",
    page_icon="🎓",
    layout="centered",
)

BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "academic_model.pkl"

st.title("🎓 Academic Compass")
st.subheader("Your Personal AI Academic Advisor")
st.write(
    "Enter your academic information to receive an AI-generated "
    "performance classification and practical recommendations."
)

# Load the trained model
@st.cache_resource
def load_model():
    package = joblib.load(MODEL_PATH)
    return package["model"], package["features"]

try:
    model, features = load_model()
except FileNotFoundError:
    st.error(
        "Model file not found. Place academic_model.pkl "
        "in the same folder as app.py."
    )
    st.stop()
except Exception as exc:
    st.error(f"Could not load the model: {exc}")
    st.stop()

# Student information form
with st.form("academic_form"):
    st.header("Student Information")

    cgpa = st.number_input(
        "Current CGPA (out of 5.00)",
        min_value=0.0,
        max_value=5.0,
        value=3.2,
        step=0.1,
    )

    attendance = st.slider(
        "Class attendance (%)",
        min_value=0,
        max_value=100,
        value=82,
    )

    study_hours = st.number_input(
        "Study hours per week",
        min_value=0.0,
        max_value=168.0,
        value=12.0,
        step=1.0,
    )

    failed_courses = st.number_input(
        "Number of failed courses",
        min_value=0,
        max_value=50,
        value=0,
        step=1,
    )

    submitted = st.form_submit_button(
        "Assess My Academic Performance",
        use_container_width=True,
    )

if submitted:
    student = pd.DataFrame(
        [{
            "cgpa": cgpa,
            "attendance": attendance,
            "study_hours": study_hours,
            "failed_courses": failed_courses,
        }],
        columns=features,
    )

    prediction = model.predict(student)[0]
    probabilities = model.predict_proba(student)[0]
    classes = model.classes_

    st.divider()
    st.header("Your Assessment")

    if prediction == "On Track":
        st.success(f"Predicted status: {prediction}")
    elif prediction == "Needs Improvement":
        st.warning(f"Predicted status: {prediction}")
    else:
        st.error(f"Predicted status: {prediction}")

    st.caption(
        "This is a demonstration model trained on synthetic data, "
        "not validated university outcomes. Use this assessment "
        "as guidance, not a definitive academic judgment."
    )

    st.subheader("Model class probabilities")
    st.bar_chart(
        pd.DataFrame(
            {"Probability": probabilities},
            index=classes,
        )
    )

    st.subheader("Personalized Recommendations")
    recommendations = []

    if cgpa < 3.5:
        recommendations.append(
            "Create a weekly revision timetable and prioritize "
            "courses with the lowest grades."
        )
    else:
        recommendations.append(
            "Maintain your study routine and review difficult "
            "topics before assessments."
        )

    if attendance < 75:
        recommendations.append(
            "Improve class attendance and catch up on missed lectures."
        )

    if study_hours < 8:
        recommendations.append(
            "Schedule more focused study sessions throughout the week."
        )

    if failed_courses > 0:
        recommendations.append(
            "Review failed courses and seek help from lecturers "
            "or academic advisers."
        )

    if not recommendations:
        recommendations.append(
            "Maintain consistent attendance, study habits, "
            "and regular progress reviews."
        )

    for item in recommendations:
        st.markdown(f"- {item}")

    st.info(
        "The classification is learned from synthetic examples. "
        "Recommendations are generated from the entered values "
        "using explicit rules."
    )

st.divider()
st.caption("Academic Compass | CSC 303 Software Engineering Project")
