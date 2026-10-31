# Postpartum Depression Risk Prediction

Master's thesis project: a system for assessing the risk of postpartum depression (PPD) from survey
data, with a responsive web application and a mechanism for collecting new data and retraining
the model.

## Database

PostgreSQL (local server, not Docker). Two tables:

- **`training_data`** — the training set: Kaggle seed data (`source='kaggle'`) + survey contributions.
- **`submissions`** — a log of all predictions made (what the model predicted and which model version was used).

Initial setup (once, in the pgAdmin Query Tool, running each command separately):

```sql
CREATE ROLE ppd_user WITH LOGIN PASSWORD 'ppd_pass';
```

```sql
CREATE DATABASE postpartum_depression OWNER ppd_user;
```

Then create the schemas and load the data:

```bash
psql -U ppd_user -d postpartum_depression -h localhost -f db/init.sql
```

```bash
psql -U ppd_user -d postpartum_depression -h localhost -f db/training_data.sql
```

```bash
python seed_database.py
```

## Model Training

The holdout set is **fixed**: rows where `id % 5 = 0`. It is deterministic on purpose: for the
comparison between the old and the new model to be fair, both must be evaluated on the same set
that neither of them saw during training.

```bash
python train_model.py
```

This saves `model/model.joblib`, `model/feature_names.joblib`, and `model/metadata.json`, and moves
the previous model to `model/archive/`. The server picks up the new model automatically, without a restart.

## Running the Project

```bash
pip install -r requirements.txt
```

Backend (from `postpartum-depression-backend`):

```bash
python -m uvicorn api.main:app --reload
```

Frontend (from `postpartum-depression-frontend`):

```bash
npm run dev
```

App: `http://localhost:5173` · Swagger: `http://127.0.0.1:8000/docs`

### Viewing on a Phone

The phone and the computer must be on the **same Wi-Fi network**. Both servers are started so that
they accept connections from the network, not only from the computer itself:

```bash
python -m uvicorn api.main:app --reload --host 0.0.0.0
```

```bash
npm run dev -- --host
```

Vite prints a "Network" address (e.g. `http://192.168.1.5:5173`) that you open in the phone's
browser. The backend address is derived automatically from the page address, so no code changes are needed.

If the page does not open, Windows Firewall is probably blocking incoming connections. Allow access
for private networks when prompted on first run.

## Administration

Available at `http://localhost:5173/#admin`. It shows the state of the dataset, the active model's
metrics, usage statistics, and a button for retraining.

The password is read from the `ADMIN_PASSWORD` environment variable (default: `admin123`):

```bash
$env:ADMIN_PASSWORD = "my-password"
```

> This is **not** real authentication: there are no accounts, roles, or sessions, only a single
> shared password. It is enough to keep the retraining endpoint from being publicly open, and it is
> documented as such.

### Retraining (champion/challenger)

A new model replaces the current one **only if it performs better** by AUC on the same holdout set.
Otherwise it is discarded and the current model stays active. All versions are kept in `model/archive/`.
