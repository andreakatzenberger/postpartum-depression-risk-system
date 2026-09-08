from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# lokalni PostgreSQL server (Windows servis), baza i nalog napravljeni
# rucno preko pgAdmin - videti README za tacne komande
DATABASE_URL = "postgresql://ppd_user:ppd_pass@localhost:5432/postpartum_depression"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
