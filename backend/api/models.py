from sqlalchemy import Column, Integer, SmallInteger, Numeric, String, TIMESTAMP
from sqlalchemy.sql import func

from api.database import Base


class Submission(Base):
    """Odgovara tabeli submissions napravljenoj u db/init.sql."""

    __tablename__ = "submissions"

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(TIMESTAMP, server_default=func.now())

    age = Column(SmallInteger, nullable=False)
    feeling_sad = Column(Numeric(3, 2), nullable=False)
    irritable = Column(Numeric(3, 2), nullable=False)
    trouble_sleeping = Column(Numeric(3, 2), nullable=False)
    concentration_problems = Column(Numeric(3, 2), nullable=False)
    appetite_problems = Column(Numeric(3, 2), nullable=False)
    guilt = Column(Numeric(3, 2), nullable=False)
    bonding_problems = Column(Numeric(3, 2), nullable=False)
    suicide_attempt = Column(Numeric(3, 2), nullable=False)

    predicted_risk = Column(SmallInteger, nullable=False)
    predicted_probability = Column(Numeric(5, 4))
    model_version = Column(String(50), nullable=False)


class TrainingRow(Base):
    """Skup podataka za treniranje - Kaggle seed + anketni doprinosi.

    Kolona feeling_depressed (ranije feeling_anxious) je ciljna promenljiva.
    Kod Kaggle redova znaci "prijavljuje anksioznost kao simptom", a kod
    anketnih redova "ima lekarsku dijagnozu PPD". Kolona source ih razdvaja.
    """

    __tablename__ = "training_data"

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(TIMESTAMP, server_default=func.now())

    age = Column(SmallInteger, nullable=False)
    feeling_sad = Column(Numeric(3, 2), nullable=False)
    irritable = Column(Numeric(3, 2), nullable=False)
    trouble_sleeping = Column(Numeric(3, 2), nullable=False)
    concentration_problems = Column(Numeric(3, 2), nullable=False)
    appetite_problems = Column(Numeric(3, 2), nullable=False)
    guilt = Column(Numeric(3, 2), nullable=False)
    bonding_problems = Column(Numeric(3, 2), nullable=False)
    suicide_attempt = Column(Numeric(3, 2), nullable=False)

    feeling_depressed = Column(Numeric(3, 2), nullable=False)
    source = Column(String(20), nullable=False)
