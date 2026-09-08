# Predikcija rizika od postporođajne depresije

Master rad — sistem za procenu rizika od postporođajne depresije (PPD) na osnovu anketnih
podataka, sa responzivnom web aplikacijom i mehanizmom za prikupljanje
novih podataka i pretreniranje modela.

## Arhitektura

```
postpartum-depression-backend/   backend + ML
├── api/                  FastAPI aplikacija
│   ├── main.py           /predict, /contribute, /stats
│   ├── admin.py          /admin/* (pregled i pretreniranje)
│   ├── model_store.py    drži aktivni model, menja ga bez restarta
│   ├── models.py         SQLAlchemy tabele
│   ├── schemas.py        validacija ulaza (Pydantic)
│   └── database.py       konekcija na PostgreSQL
├── scripts/
│   ├── mappings.py       mapiranje odgovora u brojeve (koristi ga i trening i API)
│   ├── preprocessing.py  obrada Kaggle CSV-a
│   ├── training.py       zajednička logika treniranja + holdout
│   └── *_model.py        implementacije četiri algoritma (eksperimentalna faza)
├── db/                   SQL šeme
├── model/                model.joblib, metadata.json, archive/
├── train_model.py        ručno treniranje
├── seed_database.py      jednokratno punjenje baze Kaggle podacima
└── main.py               poređenje četiri algoritma (za rad, ne za aplikaciju)

postpartum-depression-frontend/  React (Vite)
└── src/
    ├── data/questions.js jedino mesto gde se menjaju pitanja
    ├── api/client.js     pozivi ka backendu
    └── components/       Welcome, Questionnaire, Result, SurveyComplete, Admin
```

## Baza podataka

PostgreSQL (lokalni server, ne Docker). Dve tabele:

- **`training_data`** — skup za treniranje: Kaggle seed (`source='kaggle'`) + anketni doprinosi
  (`source='anketa'`).
- **`submissions`** — dnevnik napravljenih procena (šta je model predvideo, koja verzija).

Prvo podešavanje (jednom, u pgAdmin Query Tool-u, svaka komanda posebno):

```sql
CREATE ROLE ppd_user WITH LOGIN PASSWORD 'ppd_pass';
```

```sql
CREATE DATABASE postpartum_depression OWNER ppd_user;
```

Zatim šeme i punjenje:

```bash
psql -U ppd_user -d postpartum_depression -h localhost -f db/init.sql
```

```bash
psql -U ppd_user -d postpartum_depression -h localhost -f db/training_data.sql
```

```bash
python seed_database.py
```

## Treniranje modela

Holdout skup je **fiksan** — redovi gde je `id % 5 = 0`. Determinističan je namerno: da bi
poređenje starog i novog modela bilo pošteno, oba moraju biti merena na istom skupu koji
nijedan nije video pri treniranju.

```bash
python train_model.py
```

Snima `model/model.joblib`, `model/feature_names.joblib` i `model/metadata.json`, a prethodni
model premešta u `model/archive/`. Server sam preuzme novi model, bez restarta.

## Pokretanje

```bash
pip install -r requirements.txt
```

Backend (iz `postpartum-depression-backend`):

```bash
python -m uvicorn api.main:app --reload
```

Frontend (iz `postpartum-depression-frontend`):

```bash
npm run dev
```

Aplikacija: `http://localhost:5173` · Swagger: `http://127.0.0.1:8000/docs`

### Prikaz na telefonu

Telefon i računar moraju biti na **istoj WiFi mreži**. Oba servera se pokreću tako da
prihvataju veze sa mreže, ne samo sa samog računara:

```bash
python -m uvicorn api.main:app --reload --host 0.0.0.0
```

```bash
npm run dev -- --host
```

Vite ispiše „Network" adresu (npr. `http://192.168.1.5:5173`) koja se otvori u pregledaču na
telefonu. Adresa backenda se izvodi automatski iz adrese stranice, pa se kod ne menja.

Ako se stranica ne otvori, Windows Firewall verovatno blokira dolazne veze — pri prvom
pokretanju treba dozvoliti pristup za privatne mreže.

## Administracija

Dostupna na `http://localhost:5173/#admin`. Prikazuje stanje skupa podataka, metrike aktivnog
modela, statistiku korišćenja i dugme za pretreniranje.

Lozinka se čita iz promenljive okruženja `ADMIN_PASSWORD` (podrazumevano `admin123`):

```bash
$env:ADMIN_PASSWORD = "moja-lozinka"
```

> Ovo **nije** prava autentifikacija — nema naloga, uloga ni sesija, samo jedna deljena lozinka.
> Dovoljno je da endpoint za pretreniranje ne stoji otvoren, ali u radu to treba tako i opisati.

### Pretreniranje (champion/challenger)

Novi model zamenjuje postojeći **samo ako je bolji** po AUC-u na istom holdout skupu. U
suprotnom se odbacuje, a stari ostaje aktivan. Sve verzije se čuvaju u `model/archive/`.

### Sintetički dopunjeni negativni primeri

U `training_data` je jednokratno dodato ~500 redova sa `feeling_depressed=0`, kao
`source='anketa'`, generisanih po zadatim raspodelama verovatnoće po atributu (skripta
`add_negative_survey_data.py` je posle toga obrisana — bila je jednokratna, kao
`seed_database.py`). Razlog: Kaggle skup nema nijedan potpuno "zdrav" zapis (ograničenje 1
ispod) i klasno je neuravnotežen. Ovi redovi **nisu** stvarni odgovori korisnica — generisani
su skriptom po definisanim raspodelama, ne prikupljeni kroz `/contribute`; to treba navesti u
metodologiji rada, jer se u bazi ne razlikuju od stvarnih anketnih doprinosa. Kolona je pre
toga preimenovana iz `feeling_anxious` (vidi `db/migrate_rename_feeling_depressed.sql`).

## Poznata ograničenja

1. **Model ne prepoznaje zdravu osobu.** U Kaggle skupu ne postoji nijedan zapis gde su svi
   simptomi „ne" (najmanji zbir je 0.5 od 8, prosek 3.57). Model takav slučaj nikad nije video,
   pa za sve odgovore „ne" vraća visok rizik. Skup je uzorak žena koje već imaju simptome, ne
   opšte populacije. *Delimično ublaženo* sintetičkim negativnim primerima (vidi gore) — i dalje
   vredi napomenuti u radu da su ti primeri generisani, ne prikupljeni.
2. **Cirkularnost ciljne promenljive** kod Kaggle dela podataka — `feeling_depressed` (ranije
   `feeling_anxious`) je jedan od simptoma iz istog upitnika, što objašnjava nerealno visok AUC
   u odnosu na literaturu (0.78–0.88). Preimenovanje kolone ovo ne rešava samo po sebi.
3. **Mešano značenje ciljne promenljive** između Kaggle i anketnih redova (vidi gore).
4. **Broj za krizne situacije nije popunjen** — u `api/main.py` stoji `[POPUNITI BROJ]`.
5. **Curenje podataka između trening i holdout skupa preko dupliranih redova.** Zbog malog broja
   mogućih kombinacija atributa, veliki deo Kaggle skupa se ponavlja identično — ~94% redova u
   holdout skupu ima potpuno isti vektor atributa kao neki red u trening skupu, pa RF/KNN delom
   pamte već viđene redove umesto da generalizuju. Ovo dodatno objašnjava nerealno visok AUC.
