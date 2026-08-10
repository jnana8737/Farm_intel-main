# Farm Intel (AgroSmart AI)

An AI-powered crop recommendation and farm intelligence platform. The frontend lets users input location and soil parameters, and the backend serves ML-based crop predictions using historical and geospatial data.

![Node.js](https://img.shields.io/badge/Node.js-339933?style=for-the-badge&logo=nodedotjs&logoColor=white)
![React](https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB)
![TypeScript](https://img.shields.io/badge/TypeScript-007ACC?style=for-the-badge&logo=typescript&logoColor=white)
![Vite](https://img.shields.io/badge/Vite-646CFF?style=for-the-badge&logo=vite&logoColor=white)
![TailwindCSS](https://img.shields.io/badge/Tailwind_CSS-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![Supabase](https://img.shields.io/badge/Supabase-3ECF8E?style=for-the-badge&logo=supabase&logoColor=white)
![scikit-learn](https://img.shields.io/badge/scikit--learn-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)

## Tech Stack

### Frontend
- **Node.js** — JavaScript runtime (required to run npm/Vite tooling)
- **React 18** — UI library
- **TypeScript** — static typing
- **Vite** — build tool & dev server
- **Tailwind CSS** — utility-first styling
- **shadcn/ui** + **Radix UI** — accessible component primitives
- **React Router DOM** — client-side routing
- **TanStack Query (React Query)** — server state/data fetching
- **React Hook Form** + **Zod** — forms & schema validation
- **Recharts** — data visualization/charts
- **Supabase JS client** — auth/database integration
- **Lucide React** — icon set
- **Sonner** — toast notifications

### Backend
- **Python 3**
- **FastAPI** — REST API framework
- **Pydantic** — request/response validation
- **scikit-learn** (via `joblib` / `rf_model.pkl`) — Random Forest crop prediction model
- **pandas / numpy** — data processing
- **Google Earth Engine (`ee`)** — satellite/geospatial data
- **Geopy (Nominatim)** — geocoding (lat/lon <-> district)
- **Requests** — HTTP calls to external APIs

### Database / Infra
- **Supabase** — backend-as-a-service (auth, database)

### Tooling
- **ESLint** — linting
- **Vitest** + **Testing Library** — unit testing
- **Playwright** — end-to-end testing
- **Bun** / **npm** — package management (both lockfiles present)

## Project Structure

```
Farm_intel-main/
├── src/                  # React frontend source
├── backend/              # FastAPI backend
│   ├── main.py           # API entrypoint (/predict endpoint)
│   ├── utils.py          # Data processing & prediction logic
│   └── final_model/      # Trained ML model + encoders + lookup data
├── supabase/             # Supabase project config
├── public/               # Static assets
└── ...config files       # Vite, Tailwind, ESLint, TS configs
```

## Getting Started

### Frontend
Requires **Node.js** (v18+ recommended) and npm installed.
```bash
npm install
npm run dev       # start dev server
npm run build     # production build
npm run test      # run unit tests
```

### Backend
```bash
cd backend
pip install fastapi uvicorn pydantic pandas numpy joblib requests geopy earthengine-api
uvicorn main:app --reload
```

The API will serve a `/predict` endpoint that accepts district or lat/lon, season, mode, and soil NPK values, returning a crop recommendation.

## Environment Variables

Create a `.env` file (not committed to version control) with the required Supabase and any external API keys used by the app.
