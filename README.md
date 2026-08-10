# Farm Intel (AgroSmart AI)

An AI-powered crop recommendation and farm intelligence platform. The frontend lets users input location and soil parameters, and the backend serves ML-based crop predictions using historical and geospatial data.

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
