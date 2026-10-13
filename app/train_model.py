
from pathlib import Path

import joblib
import pandas as pd
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier

BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_PATH = BASE_DIR / "models" / "academic_advisor_model.pkl"

FEATURES = [
    "cgpa",
    "programming_score",
    "math_score",
    "attendance_pct",
    "data_interest",
    "software_interest",
    "ai_interest",
]


def create_dataset(samples=1000, seed=42):
    data = pd.DataFrame()

    data["cgpa"] = 0.5 + (
        pd.Series(range(samples)).sample(frac=1, random_state=seed)
        .reset_index(drop=True) % 450
    ) / 100

    # Generate reproducible student profiles.
    data = pd.DataFrame({
        "cgpa": [
            round(0.5 + ((i * 37 + seed) % 451) / 100, 2)
            for i in range(samples)
        ],
        "programming_score": [
            (i * 17 + seed) % 101 for i in range(samples)
        ],
        "math_score": [
            (i * 29 + seed) % 101 for i in range(samples)
        ],
        "attendance_pct": [
            (i * 23 + seed) % 101 for i in range(samples)
        ],
        "data_interest": [
            (i * 13 + seed) % 10 + 1 for i in range(samples)
        ],
        "software_interest": [
            (i * 19 + seed) % 10 + 1 for i in range(samples)
        ],
        "ai_interest": [
            (i * 31 + seed) % 10 + 1 for i in range(samples)
        ],
    })

    labels = []

    for row in data.itertuples(index=False):
        if row.cgpa < 2.0 or row.attendance_pct < 40:
            pathway = "academic_support"
        else:
            scores = {
                "data_science": (
                    row.data_interest
                    + row.math_score / 15
                ),
                "software_engineering": (
                    row.software_interest
                    + row.programming_score / 15
                ),
                "ai_ml": (
                    row.ai_interest
                    + row.math_score / 20
                    + row.programming_score / 20
                ),
            }
            pathway = max(scores, key=scores.get)

        labels.append(pathway)

    data["pathway"] = labels
    return data


def train_model():
    MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)

    data = create_dataset()

    X = data[FEATURES]
    y = data["pathway"]

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y,
    )

    model = DecisionTreeClassifier(
        max_depth=6,
        min_samples_leaf=5,
        random_state=42,
    )

    model.fit(X_train, y_train)

    predictions = model.predict(X_test)
    accuracy = accuracy_score(y_test, predictions)

    joblib.dump(model, MODEL_PATH)

    print("Model training completed!")
    print(f"Test accuracy: {accuracy:.2%}")
    print(f"Model saved to: {MODEL_PATH}")


if __name__ == "__main__":
    train_model()
