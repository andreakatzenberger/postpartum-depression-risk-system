# Frontend — Sistem za procenu rizika od postporođajne depresije
React (Vite) aplikacija za procenu rizika od postporođajne depresije (PPD). Komunicira sa
backend-om preko REST API-ja (FastAPI).
Struktura
```
src/
├── App.jsx                    tok kroz aplikaciju (welcome → pitanja → rezultat), #admin ruta bez react-router-a
├── api/client.js               poziva backend (/predict, /contribute, /admin/*)
├── data/questions.js           definicije pitanja upitnika
└── components/
    ├── Welcome.jsx              početni ekran, izbor režima
    ├── Questionnaire.jsx        prikaz pitanja i unos odgovora
    ├── Result.jsx               prikaz procene rizika (režim "Proceni moj rizik")
    ├── SurveyComplete.jsx       potvrda doprinosa (režim "Doprinesi istraživanju")
    ├── Admin.jsx                administratorski panel (#admin), pregled statistika i pretreniranje
    └── Icons.jsx                SVG ikonice
```
Aplikacija ima dva režima: "Proceni moj rizik" (`predict`) daje orijentacionu procenu na
osnovu devet pitanja o simptomima, dok "Doprinesi istraživanju" (`contribute`) dodaje i
pitanje o samoproceni pa odgovore direktno čuva u skup za treniranje modela.
Administratorski panel je dostupan na ruti `#admin`.
Pokretanje
Potreban je Node.js (18+) i pokrenut backend (podrazumevano
na portu 8000).
```
npm install
npm run dev
```
Aplikacija po podrazumevanoj vrednosti očekuje backend na `http://<host>:8000`. Ako backend radi
na drugoj adresi, podesiti je preko env promenljive `VITE_API_URL` (npr. u `.env` fajlu:
`VITE_API_URL=http://localhost:8000`).
Ostale komande:
```
npm run build     # produkciona verzija (folder dist/)
npm run preview   # lokalni pregled produkcione verzije
npm run lint      # ESLint provera
```
