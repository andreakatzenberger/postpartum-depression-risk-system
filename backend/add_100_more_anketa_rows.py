"""
Dodatnih 100 demo redova u training_data, oznacenih kao source='anketa',
da bi promena posle pretreniranja (npr. train_model.py ili /admin/retrain)
bila vidljivija nego sa svega 20 novih redova (koji su vec dodati skriptom
add_demo_anketa_rows.py) - 100 redova je vec ~5% od dosadasnjeg skupa, pa je
realnije ocekivati primetnu promenu u metrikama.

Vrednosti su kodirane na isti nacin kao stvarni odgovori iz upitnika
(0 / 0.5 / 1, age 1-5, feeling_depressed 0/1 - scripts/mappings.py), sa istim
blagim (ne savrsenim) razlikama izmedju "pozitivnih" i "negativnih" redova
kao i kod prve serije od 20.

Pokretanje:
    python add_100_more_anketa_rows.py
"""
from sqlalchemy import text

from api.database import engine

# (age, feeling_sad, irritable, trouble_sleeping, concentration_problems,
#  appetite_problems, guilt, bonding_problems, suicide_attempt, feeling_depressed)
DEMO_ROWS = [
    (2, 1, 0, 0.5, 0.5, 1, 0.5, 1, 1, 1),
    (4, 0, 1, 0.5, 1, 0.5, 0, 0, 0, 0),
    (1, 0.5, 0.5, 0, 0, 1, 0, 0, 0, 0),
    (1, 1, 1, 1, 1, 0.5, 0.5, 1, 1, 1),
    (5, 0.5, 1, 0.5, 0.5, 0, 1, 1, 1, 1),
    (1, 1, 0.5, 0.5, 0.5, 0, 1, 1, 1, 1),
    (4, 0.5, 0, 1, 0, 0.5, 0, 0, 0, 0),
    (3, 0, 0, 0, 0.5, 0, 0.5, 0, 0.5, 0),
    (4, 1, 1, 1, 1, 1, 1, 1, 1, 1),
    (1, 1, 1, 1, 0.5, 0, 0.5, 1, 1, 1),
    (4, 1, 1, 1, 0.5, 1, 0.5, 0.5, 1, 1),
    (2, 0, 0, 0, 1, 0.5, 0.5, 0, 0, 0),
    (1, 0, 0, 0, 0, 1, 0, 0.5, 1, 0),
    (1, 0, 0, 0, 0.5, 0, 0.5, 0.5, 0, 0),
    (4, 0.5, 0.5, 1, 0.5, 0, 0, 0.5, 0, 0),
    (2, 0, 1, 1, 0.5, 1, 0.5, 1, 1, 1),
    (2, 1, 0, 0, 0, 0, 0, 0.5, 0.5, 0),
    (5, 0, 0.5, 1, 1, 0.5, 1, 0, 0.5, 1),
    (5, 0.5, 0.5, 1, 1, 0, 1, 1, 1, 1),
    (5, 0, 0, 0.5, 0, 0, 0, 0, 0.5, 0),
    (3, 0, 1, 0.5, 0, 0, 0, 0, 0, 0),
    (2, 0.5, 1, 0.5, 0, 1, 1, 1, 1, 1),
    (5, 0.5, 0.5, 0.5, 1, 1, 1, 1, 1, 1),
    (3, 0, 0, 0, 0.5, 0, 0, 0, 0, 0),
    (3, 0.5, 0, 1, 0.5, 0, 0, 1, 1, 1),
    (1, 0.5, 0.5, 0, 0, 0.5, 1, 0.5, 0.5, 0),
    (4, 0.5, 1, 0.5, 1, 1, 0.5, 0, 0.5, 1),
    (2, 0.5, 0.5, 0, 1, 1, 0.5, 1, 0.5, 1),
    (2, 0, 0, 0, 0, 0, 0, 0, 0, 0),
    (5, 1, 1, 1, 1, 1, 0.5, 1, 0, 1),
    (5, 0.5, 0.5, 0, 0, 0, 0.5, 0, 0, 0),
    (5, 1, 1, 0.5, 1, 0.5, 1, 0.5, 0, 1),
    (1, 0.5, 0, 1, 0, 0, 0.5, 0, 0, 0),
    (5, 0.5, 1, 0, 0.5, 0.5, 0.5, 0, 0.5, 0),
    (3, 0.5, 0, 0.5, 0.5, 0, 0, 0, 0.5, 0),
    (2, 0, 1, 0, 0, 1, 0, 0, 0.5, 0),
    (2, 0.5, 0.5, 1, 1, 1, 1, 1, 1, 1),
    (3, 0, 0.5, 0, 0, 0, 0, 0, 0, 0),
    (5, 0.5, 0, 0.5, 0, 0, 0.5, 0.5, 0.5, 0),
    (3, 0.5, 0, 0.5, 1, 1, 0.5, 1, 0.5, 0),
    (1, 0.5, 1, 1, 1, 0.5, 0.5, 1, 1, 1),
    (2, 1, 0.5, 0.5, 1, 0, 0.5, 0, 0, 0),
    (5, 0, 0.5, 0.5, 0, 0, 1, 0, 0.5, 0),
    (3, 0.5, 1, 0.5, 1, 1, 0.5, 1, 0.5, 1),
    (5, 0, 0, 0.5, 0, 0, 0, 0.5, 0, 0),
    (3, 1, 0, 0.5, 0, 0, 0, 1, 0.5, 0),
    (5, 0.5, 0, 0.5, 0.5, 0.5, 0.5, 1, 0.5, 1),
    (4, 1, 1, 1, 1, 0.5, 0.5, 1, 1, 1),
    (2, 0.5, 0.5, 1, 0.5, 1, 0.5, 1, 0, 1),
    (3, 0.5, 0, 0, 0, 0.5, 0, 0.5, 0.5, 0),
    (2, 0.5, 0.5, 0.5, 0.5, 0.5, 0, 0, 0.5, 0),
    (2, 0.5, 0.5, 0, 0, 1, 0.5, 0, 0.5, 0),
    (2, 1, 0.5, 1, 0.5, 0.5, 1, 1, 0, 1),
    (2, 1, 0, 0, 0, 0, 0, 0, 0, 0),
    (2, 1, 0.5, 1, 0.5, 0.5, 0.5, 1, 1, 1),
    (2, 1, 0.5, 0, 1, 0.5, 0, 1, 0.5, 0),
    (3, 1, 0.5, 1, 1, 0.5, 1, 0.5, 1, 1),
    (3, 0, 1, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 1),
    (5, 0, 0, 0.5, 0.5, 0.5, 0, 0.5, 0.5, 0),
    (5, 0, 0, 0, 0.5, 0, 0, 0, 0, 0),
    (4, 0.5, 0, 0, 0.5, 0, 0, 0.5, 0, 0),
    (3, 0, 0, 1, 0, 0.5, 0.5, 0.5, 1, 0),
    (1, 1, 1, 1, 0.5, 1, 1, 1, 1, 1),
    (1, 0, 0, 0.5, 0.5, 0, 0.5, 0.5, 0, 0),
    (1, 0, 0, 0, 0, 0, 0, 0.5, 0, 0),
    (1, 0, 0, 0.5, 1, 0.5, 0, 0, 0.5, 0),
    (2, 0.5, 1, 0, 0, 0.5, 0, 0, 0.5, 0),
    (3, 0.5, 0.5, 0, 1, 1, 0.5, 1, 0, 1),
    (4, 0, 0.5, 0, 0.5, 0, 0.5, 0, 0, 0),
    (5, 0, 0, 0, 1, 0, 0, 0, 0, 0),
    (1, 1, 1, 0.5, 1, 1, 0.5, 1, 0.5, 1),
    (2, 1, 1, 1, 0.5, 1, 0, 0.5, 0, 1),
    (4, 1, 1, 0, 0.5, 1, 0.5, 0.5, 1, 1),
    (5, 0, 0, 0, 0, 0, 0, 0, 0.5, 0),
    (4, 1, 0, 0.5, 1, 1, 1, 0.5, 0, 1),
    (2, 1, 0.5, 1, 1, 0.5, 1, 0.5, 0.5, 1),
    (5, 0.5, 0.5, 0.5, 0.5, 0, 0.5, 1, 1, 1),
    (5, 1, 0.5, 1, 1, 0, 1, 1, 0.5, 1),
    (4, 0, 0, 0, 0, 1, 0, 0.5, 0, 0),
    (5, 0.5, 0, 0, 0.5, 0, 0.5, 0, 0, 0),
    (3, 0, 0.5, 0.5, 1, 0.5, 0, 0, 0, 0),
    (2, 0.5, 0.5, 1, 0, 0.5, 0.5, 0, 0.5, 0),
    (3, 0.5, 1, 1, 0, 1, 0.5, 1, 1, 1),
    (1, 1, 1, 1, 1, 1, 0.5, 1, 1, 1),
    (2, 0, 0.5, 0, 0.5, 0.5, 0.5, 0, 0.5, 0),
    (5, 0.5, 0, 0.5, 1, 0, 1, 0.5, 0, 0),
    (5, 0, 1, 1, 1, 1, 1, 0.5, 0, 1),
    (4, 1, 0, 0, 1, 0.5, 0.5, 0, 0.5, 0),
    (5, 0.5, 0.5, 1, 1, 1, 1, 1, 0.5, 1),
    (2, 0.5, 0, 0, 0, 0, 0, 1, 0, 0),
    (4, 1, 1, 0, 0.5, 1, 0.5, 1, 1, 1),
    (2, 0, 0, 1, 1, 1, 0.5, 1, 1, 1),
    (4, 1, 0.5, 0, 0.5, 0.5, 0, 1, 0.5, 1),
    (4, 1, 1, 1, 0.5, 0.5, 1, 1, 0.5, 1),
    (1, 0.5, 0, 0.5, 0.5, 0, 0, 0, 1, 0),
    (2, 0, 0.5, 0, 0.5, 0, 1, 0, 0, 0),
    (1, 0.5, 1, 1, 1, 1, 1, 1, 0.5, 1),
    (5, 1, 0.5, 0, 0.5, 0.5, 0, 0, 0, 0),
    (3, 0, 0, 0, 0, 0, 1, 0.5, 0, 0),
    (1, 0, 0.5, 0.5, 0, 1, 0, 0, 0.5, 0),
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
