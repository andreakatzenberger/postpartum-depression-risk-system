"""
Zajednicka logika treniranja - koriste je i train_model.py (rucno) i
admin endpoint za pretreniranje.

VAZNO: holdout (test) skup se odredjuje determinisicki, po id-u reda
(id % 5 == 0). Razlog: da bi poredjenje starog i novog modela bilo
posteno, oba moraju biti merena na ISTOM skupu koji nijedan od njih
nije video pri treniranju. Nasumicna podela bi se menjala pri svakom
pozivu, pa poredjenje ne bi znacilo nista.
"""
import os
from datetime import datetime

import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import roc_auc_score, accuracy_score, f1_score

from scripts.mappings import FEATURE_NAME_MAP

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_DIR = os.path.join(BASE_DIR, "model")
ARCHIVE_DIR = os.path.join(MODEL_DIR, "archive")

HOLDOUT_MODULO = 5  # svaki 5. red ide u holdout -> 20%

RF_PARAMS = dict(
    n_estimators=300,
    max_depth=20,
    min_samples_split=3,
    min_samples_leaf=1,
    max_features="log2",
    random_state=42,
)


def load_dataset(engine):
    df = pd.read_sql("SELECT * FROM training_data ORDER BY id", engine)

    holdout_mask = df["id"] % HOLDOUT_MODULO == 0
    return df[~holdout_mask].copy(), df[holdout_mask].copy(), df


def to_xy(df):
    X = df[list(FEATURE_NAME_MAP.keys())].rename(columns=FEATURE_NAME_MAP)
    y = df["feeling_depressed"].astype(int)
    return X, y


def evaluate(model, X, y):
    y_pred = model.predict(X)
    y_proba = model.predict_proba(X)[:, 1]
    return {
        "auc": round(float(roc_auc_score(y, y_proba)), 4),
        "accuracy": round(float(accuracy_score(y, y_pred)), 4),
        "f1": round(float(f1_score(y, y_pred, average="weighted", zero_division=0)), 4),
    }


def train_challenger(engine):
    """Trenira novi model na trening delu i meri ga na holdout-u.

    Vraca (model, feature_names, metrike, statistika_o_podacima).
    """
    train_df, holdout_df, full_df = load_dataset(engine)

    X_train, y_train = to_xy(train_df)
    X_hold, y_hold = to_xy(holdout_df)

    model = RandomForestClassifier(**RF_PARAMS)
    model.fit(X_train, y_train)

    metrics = evaluate(model, X_hold, y_hold)

    counts = full_df["source"].value_counts().to_dict()
    stats = {
        "rows_total": int(len(full_df)),
        "rows_train": int(len(train_df)),
        "rows_holdout": int(len(holdout_df)),
        "rows_kaggle": int(counts.get("kaggle", 0)),
        "rows_anketa": int(counts.get("anketa", 0)),
    }

    return model, X_train.columns.tolist(), metrics, stats


def evaluate_champion(engine):
    """Meri trenutno aktivni model na istom holdout skupu."""
    champion_path = os.path.join(MODEL_DIR, "model.joblib")
    if not os.path.exists(champion_path):
        return None

    model = joblib.load(champion_path)
    feature_names = joblib.load(os.path.join(MODEL_DIR, "feature_names.joblib"))

    _, holdout_df, _ = load_dataset(engine)
    X_hold, y_hold = to_xy(holdout_df)
    return evaluate(model, X_hold[feature_names], y_hold)


def read_metadata():
    path = os.path.join(MODEL_DIR, "metadata.json")
    if not os.path.exists(path):
        return None
    import json

    with open(path, encoding="utf-8") as f:
        return json.load(f)


def save_model(model, feature_names, metrics, stats, version):
    """Snima model kao aktivan, a prethodni premesta u arhivu."""
    import json
    import shutil

    os.makedirs(MODEL_DIR, exist_ok=True)
    os.makedirs(ARCHIVE_DIR, exist_ok=True)

    active_path = os.path.join(MODEL_DIR, "model.joblib")

    # prethodni model cuvamo, da se moze vratiti unazad
    previous = read_metadata()
    if previous and os.path.exists(active_path):
        stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        archived = os.path.join(ARCHIVE_DIR, f"{previous['version']}_{stamp}.joblib")
        shutil.copy2(active_path, archived)

    joblib.dump(model, active_path)
    joblib.dump(feature_names, os.path.join(MODEL_DIR, "feature_names.joblib"))

    metadata = {
        "version": version,
        "trained_at": datetime.now().isoformat(timespec="seconds"),
        "metrics": metrics,
        **stats,
    }
    with open(os.path.join(MODEL_DIR, "metadata.json"), "w", encoding="utf-8") as f:
        json.dump(metadata, f, ensure_ascii=False, indent=2)

    return metadata


def next_version():
    meta = read_metadata()
    if not meta:
        return "rf_v1"
    current = meta.get("version", "rf_v1")
    try:
        number = int(current.split("_v")[-1])
    except ValueError:
        number = 1
    return f"rf_v{number + 1}"
