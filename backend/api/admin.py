"""
Admin endpoint-i: pregled stanja i pretreniranje modela.

ZASTITA: jedna deljena lozinka iz promenljive okruzenja ADMIN_PASSWORD.
Ovo NIJE prava autentifikacija - nema naloga, uloga ni sesija - i tako
je treba i opisati u radu. Dovoljno je da endpoint za pretreniranje ne
stoji potpuno otvoren, sto je bio cilj.

Lozinka se salje kroz zaglavlje X-Admin-Password, nikad kroz URL.
"""
import os
import secrets

from fastapi import APIRouter, Header, HTTPException
from sqlalchemy import func as sa_func, text

from api.database import SessionLocal, engine
from api.model_store import store
from api.models import Submission, TrainingRow
from scripts.training import (
    train_challenger,
    evaluate_champion,
    save_model,
    next_version,
    read_metadata,
)

ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "admin123")

router = APIRouter(prefix="/admin", tags=["admin"])


def check_password(x_admin_password: str | None):
    if not x_admin_password or not secrets.compare_digest(x_admin_password, ADMIN_PASSWORD):
        raise HTTPException(status_code=401, detail="Invalid password.")


@router.post("/login")
def login(x_admin_password: str | None = Header(default=None)):
    check_password(x_admin_password)
    return {"ok": True}


@router.get("/overview")
def overview(x_admin_password: str | None = Header(default=None)):
    check_password(x_admin_password)
    store.ensure_fresh()

    db = SessionLocal()
    try:
        total = db.query(sa_func.count(TrainingRow.id)).scalar()
        anketa = (
            db.query(sa_func.count(TrainingRow.id))
            .filter(TrainingRow.source == "anketa")
            .scalar()
        )
        predictions = db.query(sa_func.count(Submission.id)).scalar()

        # koliko je anketnih zapisa (samoprocena) reklo da se oseca depresivno
        anketa_pozitivnih = (
            db.query(sa_func.count(TrainingRow.id))
            .filter(TrainingRow.source == "anketa", TrainingRow.feeling_depressed == 1)
            .scalar()
        )

        # prosecna predikcija - ako je blizu 1, model svima govori da su u riziku
        avg_prediction = db.execute(
            text("SELECT AVG(predicted_probability) FROM submissions")
        ).scalar()
    finally:
        db.close()

    metadata = read_metadata() or {}
    rows_at_training = metadata.get("rows_total", 0)

    return {
        "dataset": {
            "total": total,
            "kaggle": total - anketa,
            "anketa": anketa,
            "anketa_depresivnih": anketa_pozitivnih,
        },
        "model": {
            "version": store.version,
            "trained_at": metadata.get("trained_at"),
            "metrics": metadata.get("metrics"),
            "rows_at_training": rows_at_training,
        },
        "usage": {
            "predictions_made": predictions,
            "avg_predicted_probability": round(float(avg_prediction), 4) if avg_prediction else None,
        },
        # koliko je novih redova stiglo otkad je model treniran
        "new_rows_since_training": max(0, total - rows_at_training),
    }


@router.post("/retrain")
def retrain(x_admin_password: str | None = Header(default=None)):
    """Champion/challenger: the new model replaces the old one ONLY if better.

    Both are measured on the same fixed holdout set that neither has seen
    during training, so the comparison is fair.
    """
    check_password(x_admin_password)

    champion_metrics = evaluate_champion(engine)
    model, feature_names, challenger_metrics, stats = train_challenger(engine)

    # bez postojeceg modela nema sta da se poredi - novi automatski prolazi
    if champion_metrics is None:
        promoted = True
        reason = "There was no previous model."
    else:
        promoted = challenger_metrics["auc"] > champion_metrics["auc"]
        reason = (
            f"The new model is better (AUC {challenger_metrics['auc']} > {champion_metrics['auc']})."
            if promoted
            else f"The new model is not better (AUC {challenger_metrics['auc']} <= {champion_metrics['auc']}) - the existing model was kept."
        )

    new_version = None
    if promoted:
        version = next_version()
        metadata = save_model(model, feature_names, challenger_metrics, stats, version)
        store.load()  # aktiviramo novi model bez restarta servera
        new_version = metadata["version"]

    return {
        "promoted": promoted,
        "reason": reason,
        "champion": champion_metrics,
        "challenger": challenger_metrics,
        "active_version": store.version,
        "new_version": new_version,
        "data": stats,
    }
