-- Skup podataka za treniranje. Zamenjuje data/data.csv kao izvor istine.
--
-- Sadrzi originalni Kaggle skup (source='kaggle') i zapise prikupljene
-- kroz anketu u aplikaciji (source='anketa'). Iste kolone -> treniraju se
-- zajedno, bez ikakve konverzije.
--
-- NAPOMENA o koloni feeling_depressed:
--   kod Kaggle redova znaci "prijavljuje anksioznost kao simptom"
--   kod anketnih redova znaci "ima lekarsku dijagnozu PPD"
-- Kolona `source` postoji upravo zato da se ta dva slucaja mogu razdvojiti
-- pri analizi.

CREATE TABLE IF NOT EXISTS training_data (
    id                      SERIAL PRIMARY KEY,
    created_at              TIMESTAMP NOT NULL DEFAULT NOW(),

    -- ulazni atributi (vec kodirani u brojeve, isto kao u trening skupu)
    age                     SMALLINT NOT NULL,          -- 1-5
    feeling_sad             NUMERIC(3, 2) NOT NULL,      -- 0 / 0.5 / 1
    irritable               NUMERIC(3, 2) NOT NULL,
    trouble_sleeping        NUMERIC(3, 2) NOT NULL,
    concentration_problems  NUMERIC(3, 2) NOT NULL,
    appetite_problems       NUMERIC(3, 2) NOT NULL,
    guilt                   NUMERIC(3, 2) NOT NULL,
    bonding_problems        NUMERIC(3, 2) NOT NULL,
    suicide_attempt         NUMERIC(3, 2) NOT NULL,

    -- ciljna promenljiva koju model predvidja
    feeling_depressed       NUMERIC(3, 2) NOT NULL,      -- 0 / 1

    source                  VARCHAR(20) NOT NULL          -- 'kaggle' / 'anketa'
);

CREATE INDEX IF NOT EXISTS idx_training_data_source ON training_data (source);

COMMENT ON TABLE training_data IS 'Skup podataka za treniranje: Kaggle seed + anketni doprinosi.';
COMMENT ON COLUMN training_data.source IS 'Odakle red potice - kaggle (preuzeto) ili anketa (prikupljeno kroz aplikaciju).';
