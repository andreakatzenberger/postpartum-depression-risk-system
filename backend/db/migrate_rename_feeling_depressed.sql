-- Jednokratna migracija: preimenovanje kolone feeling_anxious -> feeling_depressed
-- u vec postojecoj bazi (tabela training_data je napravljena pre ove izmene).
--
-- Pokrenuti JEDNOM, pre nego sto se pozove scripts/add_negative_survey_data.py
-- ili python train_model.py:
--
--   psql -U ppd_user -d postpartum_depression -h localhost -f db/migrate_rename_feeling_depressed.sql

ALTER TABLE training_data RENAME COLUMN feeling_anxious TO feeling_depressed;

COMMENT ON COLUMN training_data.feeling_depressed IS
    'Ciljna promenljiva. Kod Kaggle redova: prijavljuje anksioznost kao simptom. Kod anketnih redova: ima lekarsku dijagnozu PPD.';
