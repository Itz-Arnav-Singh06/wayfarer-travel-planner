# Wayfarer — Personalized Travel Itinerary Planner

A calm, responsive trip-planning experience built for the **Transportation / Individual** project brief. Wayfarer turns a destination, dates, budget, travel style, and interests into a structured day-by-day plan.

## What’s included

- React + Vite trip dashboard with sample trips, day timeline, cost estimates, and a trip-builder form.
- FastAPI endpoint that returns a key-free demo itinerary by default, or a generated itinerary when an OpenAI key is configured.
- Optional Supabase schema with row-level security for per-user saved trips.
- Local-first dashboard demo so the interface can be explored before connecting external services.

## Run locally

Requirements: Node.js 20+ and Python 3.11+.

```bash
# Terminal 1: frontend
npm install
npm run dev

# Terminal 2: API
cd backend
python -m venv .venv
source .venv/bin/activate       # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env            # optional: add OPENAI_API_KEY
uvicorn main:app --reload --port 8000
```

Open http://localhost:5173. The FastAPI health check is at http://localhost:8000/api/health and the interactive API docs are at http://localhost:8000/docs.

## AI generation

Without `OPENAI_API_KEY`, `POST /api/itineraries` returns a representative demo itinerary so the API remains usable without paid services. Add an OpenAI API key to `backend/.env` to enable model-generated plans. The key stays on the backend and must never be placed in frontend code.

Example request:

```json
{
  "destination": "Lisbon, Portugal",
  "start_date": "2026-10-18",
  "duration_days": 4,
  "budget_per_day": 100,
  "interests": ["food", "culture", "slow mornings"],
  "travel_style": "balanced",
  "travelers": 1
}
```

## Supabase (optional)

Create a Supabase project and run [`supabase/schema.sql`](supabase/schema.sql) in its SQL editor. The schema is ready for authenticated trip persistence and applies row-level security. Configure `SUPABASE_URL` and `SUPABASE_SERVICE_ROLE_KEY` only on a trusted server; never expose the service-role key in the browser. Saving trips is a next integration step for this starter.

## Next steps for a complete submission

1. Connect the trip builder to `POST /api/itineraries` and render the returned itinerary.
2. Add Supabase Auth and persist trips through a server-side authenticated flow.
3. Add editable activities, day regeneration, destination-aware mapping, and deployment.

## Project links

- Demo: not deployed yet
- GitHub: https://github.com/Itz-Arnav-Singh06/wayfarer-travel-planner

## Stack

React · Vite · FastAPI · Pydantic · OpenAI API (optional) · Supabase (optional)
