"""
Jednokratno punjenje tabele training_data originalnim Kaggle skupom.

Posle ovoga baza je izvor istine za treniranje, a data/data.csv ostaje
samo kao arhiva originalnog fajla.

Pokretanje:
    python seed_database.py
"""
from sqlalchemy import text

from api.database import engine
from scripts.preprocessing import preprocess_data
from scripts.mappings import FEATURE_NAME_MAP

# naziv kolone u DataFrame-u -> naziv kolone u bazi
DB_COLUMN_MAP = {original: db for db, original in FEATURE_NAME_MAP.items()}
DB_COLUMN_MAP["feeling anxious"] = "feeling_depressed"


def seed():
    train_df, test_df = preprocess_data()
    import pandas as pd

    df = pd.concat([train_df, test_df], ignore_index=True)
    df = df.rename(columns=DB_COLUMN_MAP)

    with engine.begin() as conn:
        existing = conn.execute(
            text("SELECT COUNT(*) FROM training_data WHERE source = 'kaggle'")
        ).scalar()

        if existing:
            print(f"Vec postoji {existing} Kaggle redova u bazi - preskacem punjenje.")
            print("Ako zelis ponovno punjenje, prvo obrisi te redove:")
            print("    DELETE FROM training_data WHERE source = 'kaggle';")
            return

        rows = df.to_dict(orient="records")
        conn.execute(
            text("""
                INSERT INTO training_data (
                    age, feeling_sad, irritable, trouble_sleeping,
                    concentration_problems, appetite_problems, guilt,
                    bonding_problems, suicide_attempt, feeling_depressed,
                    source
                ) VALUES (
                    :age, :feeling_sad, :irritable, :trouble_sleeping,
                    :concentration_problems, :appetite_problems, :guilt,
                    :bonding_problems, :suicide_attempt, :feeling_depressed,
                    'kaggle'
                )
            """),
            rows,
        )
        print(f"Ubaceno {len(rows)} Kaggle redova u training_data.")


if __name__ == "__main__":
    seed()
