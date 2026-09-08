-- Automatski se izvrsava pri prvom pokretanju Postgres kontejnera.
-- Cuva svaki upitnik koji korisnica popuni preko aplikacije (Faza 2),
-- zamenjuje CSV/txt kao mesto za nove podatke.

CREATE TABLE IF NOT EXISTS submissions (
    id                      SERIAL PRIMARY KEY,
    created_at              TIMESTAMP NOT NULL DEFAULT NOW(),

    -- ulazni atributi, isti redosled/znacenje kao u trening skupu
    age                     SMALLINT NOT NULL,          -- 1-5 (mapirano iz opsega godina)
    feeling_sad             NUMERIC(3, 2) NOT NULL,      -- 0 / 0.5 / 1
    irritable               NUMERIC(3, 2) NOT NULL,
    trouble_sleeping        NUMERIC(3, 2) NOT NULL,
    concentration_problems  NUMERIC(3, 2) NOT NULL,
    appetite_problems       NUMERIC(3, 2) NOT NULL,
    guilt                   NUMERIC(3, 2) NOT NULL,
    bonding_problems        NUMERIC(3, 2) NOT NULL,
    suicide_attempt         NUMERIC(3, 2) NOT NULL,

    -- rezultat predikcije u trenutku unosa
    predicted_risk          SMALLINT NOT NULL,           -- 0/1, odgovor modela
    predicted_probability   NUMERIC(5, 4),                -- verovatnoca iz modela
    model_version           VARCHAR(50) NOT NULL          -- npr. 'rf_v1', da se zna koji model je odgovorio
);

COMMENT ON TABLE submissions IS 'Unosi korisnica kroz aplikaciju - buduca osnova za pretreniranje modela.';
