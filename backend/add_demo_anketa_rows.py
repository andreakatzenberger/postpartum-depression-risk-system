"""
Jednokratno dodavanje 20 demo redova u training_data, oznacenih kao
source='anketa', da bi se moglo prikazati kako se model menja posle
pretreniranja (npr. kroz /admin/retrain ili train_model.py) kada se
skup za obucavanje dopuni novim anketnim doprinosima.

Vrednosti su vec kodirane na isti nacin kao stvarni odgovori iz upitnika
(0 / 0.5 / 1, age 1-5, feeling_depressed 0/1 - videti scripts/mappings.py),
sa blagom, ali ne savrsenom, razlikom u simptomima izmedju redova gde je
feeling_depressed = 1 i onih gde je 0 (kao i u stvarnim Kaggle podacima,
i "negativni" redovi imaju neki nivo simptoma, ne nulu).

Pokretanje:
    python add_demo_anketa_rows.py
"""
from sqlalchemy import text

from api.database import engine

# (age, feeling_sad, irritable, trouble_sleeping, concentration_problems,
#  appetite_problems, guilt, bonding_problems, suicide_attempt, feeling_depressed)
DEMO_ROWS = [
    (4, 1, 0, 0, 0.5, 1, 1, 0.5, 0.5, 0),
    (3, 1, 0.5, 0, 0.5, 0.5, 0, 0, 0.5, 0),
    (1, 1, 1, 1, 1, 1, 1, 0, 0.5, 1),
    (5, 0, 0.5, 0, 0.5, 0, 1, 0, 0, 0),
    (5, 1, 0.5, 1, 0.5, 1, 0.5, 0.5, 0.5, 1),
    (3, 1, 0, 1, 1, 0.5, 0.5, 1, 0.5, 1),
    (5, 1, 0.5, 0, 0, 0, 1, 0.5, 0, 0),
    (1, 0, 0, 0, 0.5, 0.5, 1, 0.5, 0, 0),
    (1, 0.5, 0, 0, 0.5, 0.5, 0, 0.5, 0, 0),
    (1, 0, 0.5, 1, 1, 1, 1, 0.5, 0.5, 1),
    (1, 0, 0.5, 0.5, 1, 1, 1, 0, 0.5, 1),
    (5, 0.5, 0.5, 1, 0, 1, 1, 0.5, 0, 1),
    (2, 0.5, 1, 0, 0, 0, 0.5, 0.5, 0, 0),
    (5, 0, 0, 0, 0.5, 0, 1, 0.5, 0, 0),
    (3, 1, 1, 1, 0.5, 0.5, 1, 0.5, 0.5, 1),
    (2, 0, 0, 0, 0.5, 0.5, 0.5, 0, 0, 0),
    (3, 0, 0.5, 0, 1, 0, 0, 0, 0, 0),
    (1, 0.5, 0.5, 0.5, 0.5, 0, 0.5, 0, 1, 1),
    (3, 1, 1, 0, 1, 1, 0.5, 0.5, 0.5, 1),
    (1, 0.5, 0, 0.5, 0.5, 0, 0.5, 0, 0.5, 0),
]

COLUMNS = [
    "age", "feeling_sad", "irritable", "trouble_sleeping",
    "concentration_problems", "appetite_problems", "guilt",
    "bonding_problems", "suicide_attempt", "feeling_depressed",
]


def run():
    rows = [dict(zip(COLUMNS, r)) for r in DEMO_ROWS]

    with engine.begin() as conn:
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
                    'anketa'
                )
            """),
            rows,
        )
        total = conn.execute(text("SELECT COUNT(*) FROM training_data")).scalar()
        anketa_total = conn.execute(
            text("SELECT COUNT(*) FROM training_data WHERE source = 'anketa'")
        ).scalar()

    print(f"Ubaceno {len(rows)} novih anketa redova u training_data.")
    print(f"Ukupno u training_data: {total} (od toga anketa: {anketa_total}).")


if __name__ == "__main__":
    run()
