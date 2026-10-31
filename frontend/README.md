# Frontend — Postpartum Depression Risk Assessment System

A React (Vite) application for assessing the risk of postpartum depression (PPD). It communicates
with the backend through a REST API (FastAPI).

## Structure

The application has two modes. **Assess my risk** (`predict`) gives an approximate risk estimate
based on nine symptom questions. **Contribute to research** (`contribute`) adds a self-assessment
question and stores the answers directly in the model's training dataset.

The admin panel is available at the `#admin` route.

## Getting Started

Requires Node.js (18+) and a running backend (by default on port 8000).

```bash
npm install
npm run dev
```

By default, the app expects the backend at `http://<host>:8000`. If the backend runs at a different
address, set it with the `VITE_API_URL` environment variable (e.g. in a `.env` file:
`VITE_API_URL=http://localhost:8000`).

## Other Commands

```bash
npm run build     # production build (dist/ folder)
npm run preview   # local preview of the production build
npm run lint      # ESLint check
```
