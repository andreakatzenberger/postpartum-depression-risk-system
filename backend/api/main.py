import pandas as pd
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import func as sa_func

from api.admin import router as admin_router
from api.database import SessionLocal
from api.model_store import store
from api.models import Submission, TrainingRow
from api.schemas import UpitnikInput, PredictionOutput, AnketaInput, ContributionOutput
from scripts.mappings import FEATURE_NAME_MAP


CRISIS_MESSAGE = (
    "You mentioned having thoughts of self-harm. "
    "If you are in danger, call emergency services at 194."
)

app = FastAPI(title="PPD Risk Prediction API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(admin_router)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/predict", response_model=PredictionOutput)
def predict(payload: UpitnikInput):
    store.ensure_fresh()
    encoded = payload.to_encoded_dict()
    row = {FEATURE_NAME_MAP[key]: value for key, value in encoded.items()}
    X = pd.DataFrame([row])[store.feature_names]
    prediction = int(store.model.predict(X)[0])
    probability = float(store.model.predict_proba(X)[0][1])
    crisis_flag = payload.suicide_attempt != "no"
    crisis_message = CRISIS_MESSAGE if crisis_flag else None
    db = SessionLocal()
    try:
        submission = Submission(
            **encoded,
            predicted_risk=prediction,
            predicted_probability=probability,
            model_version=store.version,
        )
        db.add(submission)
        db.commit()
    finally:
        db.close()
    return PredictionOutput(
        predicted_risk=prediction,
        predicted_probability=probability,
        model_version=store.version,
        crisis_flag=crisis_flag,
        crisis_message=crisis_message,
    )


@app.post("/contribute", response_model=ContributionOutput)
def contribute(payload: AnketaInput):
    """Accepts a survey record and adds it to the training dataset.

    The model is NOT called here - this part of the app only collects data.
    """
    row = payload.to_training_row()

    db = SessionLocal()
    try:
        db.add(TrainingRow(**row))
        db.commit()

        total = db.query(sa_func.count(TrainingRow.id)).scalar()
        survey = (
            db.query(sa_func.count(TrainingRow.id))
            .filter(TrainingRow.source == "anketa")
            .scalar()
        )
    finally:
        db.close()

    crisis_flag = payload.suicide_attempt != "no"

    return ContributionOutput(
        saved=True,
        total_records=total,
        survey_records=survey,
        crisis_flag=crisis_flag,
        crisis_message=CRISIS_MESSAGE if crisis_flag else None,
    )


@app.get("/stats")
def stats():
    """Basic metrics - the foundation for the admin page."""
    store.ensure_fresh()
    db = SessionLocal()
    try:
        total = db.query(sa_func.count(TrainingRow.id)).scalar()
        survey = (
            db.query(sa_func.count(TrainingRow.id))
            .filter(TrainingRow.source == "anketa")
            .scalar()
        )
        predictions = db.query(sa_func.count(Submission.id)).scalar()
    finally:
        db.close()

    return {
        "training_total": total,
        "training_kaggle": total - survey,
        "training_anketa": survey,
        "predictions_made": predictions,
        "active_model": store.version,
    }
