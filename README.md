# Wayfarer — Personalized Travel Itinerary Planner

A responsive React travel dashboard that helps travelers shape a day-by-day trip around destination, dates, budget, and interests. The project uses Vite for the frontend and FastAPI for the optional itinerary API.

## Project links

- **Live demo:** https://itz-arnav-singh06.github.io/wayfarer-travel-planner/
- **GitHub:** https://github.com/Itz-Arnav-Singh06/wayfarer-travel-planner

The live demo currently previews the frontend with sample trips. Personalized API generation requires the FastAPI backend to be hosted separately.

## Run locally

Requirements: Node.js 20+ and Python 3.11+.

Start the frontend:

```bash
npm install
npm run dev
```

In a second terminal, start the API from the repository root:

```bash
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

Open http://localhost:5173. API health is at http://localhost:8000/api/health and API docs are at http://localhost:8000/docs.

## Optional AI generation

The API returns a key-free sample itinerary by default. To enable model-generated plans, configure `OPENAI_API_KEY` in your local environment. Keep API keys on the backend; do not put them in frontend code.

## Optional Supabase setup

Run `schema.sql` in the Supabase SQL editor. Database persistence and authentication are optional next steps.

## Stack

React · Vite · FastAPI · Pydantic · OpenAI API (optional) · Supabase (optional)
