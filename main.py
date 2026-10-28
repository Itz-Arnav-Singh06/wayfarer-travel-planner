"""FastAPI service for Wayfarer. It works without keys using a local demo planner."""
import json
import os
from datetime import date
from typing import Literal

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

load_dotenv()
app = FastAPI(title="Wayfarer Travel Planner API", version="1.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[os.getenv("FRONTEND_ORIGIN", "http://localhost:5173")],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)


class TripRequest(BaseModel):
    destination: str = Field(min_length=2, max_length=100)
    start_date: date
    duration_days: int = Field(ge=1, le=21)
    budget_per_day: int = Field(default=100, ge=10, le=5000)
    interests: list[str] = Field(default_factory=list, max_length=10)
    travel_style: Literal["budget", "balanced", "premium"] = "balanced"
    travelers: int = Field(default=1, ge=1, le=20)


class Activity(BaseModel):
    time: str
    title: str
    place: str
    category: str
    description: str
    estimated_cost: int
    transport: str


class DayPlan(BaseModel):
    date: date
    theme: str
    activities: list[Activity]
    estimated_total: int


class TripPlan(BaseModel):
    destination: str
    summary: str
    days: list[DayPlan]
    estimated_total: int
    generated_by: str


def demo_plan(request: TripRequest) -> TripPlan:
    """Helpful, key-free sample plan so reviewers can run the app immediately."""
    city = request.destination.split(",")[0].strip()
    templates = [
        ("09:00", "Neighborhood coffee & breakfast", "A well-loved local cafe", "food", "Start gently with a local breakfast and a little people-watching.", 12, "Walk"),
        ("10:30", "Explore the historic quarter", "Old town streets", "culture", "Follow the small lanes and take time for the details along the way.", 0, "Walk · 1.4 km"),
        ("13:00", "A long, easy lunch", "Market-side restaurant", "food", "Try a regional specialty at a relaxed neighborhood spot.", 24, "Walk · 8 min"),
        ("15:00", "A museum or garden hour", "City museum & gardens", "culture", "A slower afternoon stop with room to sit and recharge.", 14, "Transit · 15 min"),
        ("18:00", "Golden hour viewpoint", "Riverside lookout", "nature", "Find a comfortable spot for the changing light and an unhurried evening.", 5, "Walk · 12 min"),
    ]
    days = []
    for day_index in range(request.duration_days):
        activities = [Activity(time=t, title=title, place=f"{place}, {city}", category=category,
                               description=description, estimated_cost=cost, transport=transport)
                      for t, title, place, category, description, cost, transport in templates]
        days.append(DayPlan(date=request.start_date.fromordinal(request.start_date.toordinal() + day_index),
                            theme=["Get your bearings", "Local favorites", "A change of scenery"][day_index % 3],
                            activities=activities, estimated_total=sum(a.estimated_cost for a in activities)))
    return TripPlan(destination=request.destination,
                    summary=f"A thoughtful {request.duration_days}-day outline for {city}, paced with time to wander.",
                    days=days, estimated_total=sum(d.estimated_total for d in days), generated_by="demo")


def ai_plan(request: TripRequest) -> TripPlan:
    from openai import OpenAI
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    prompt = f"""Create a practical {request.duration_days}-day travel itinerary for {request.destination}.
Start date: {request.start_date}; travelers: {request.travelers}; budget per person/day in USD: {request.budget_per_day}; style: {request.travel_style}; interests: {', '.join(request.interests) or 'local highlights'}.
Return only JSON matching this shape: {{"destination":string,"summary":string,"days":[{{"date":"YYYY-MM-DD","theme":string,"activities":[{{"time":"HH:MM","title":string,"place":string,"category":string,"description":string,"estimated_cost":integer,"transport":string}}],"estimated_total":integer}}],"estimated_total":integer}}.
Use 3-5 activities each day, realistic pacing, and clear estimates. Do not claim live availability or exact opening hours."""
    response = client.chat.completions.create(
        model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
        messages=[{"role": "system", "content": "You are a careful, locally-minded travel planner. Return valid JSON only."},
                  {"role": "user", "content": prompt}],
        response_format={"type": "json_object"}, temperature=0.7)
    return TripPlan.model_validate(json.loads(response.choices[0].message.content or "{}"))


@app.get("/api/health")
def health():
    return {"status": "ok", "ai_enabled": bool(os.getenv("OPENAI_API_KEY")),
            "database_enabled": bool(os.getenv("SUPABASE_URL") and os.getenv("SUPABASE_SERVICE_ROLE_KEY"))}


@app.post("/api/itineraries", response_model=TripPlan)
def create_itinerary(request: TripRequest):
    if not os.getenv("OPENAI_API_KEY"):
        return demo_plan(request)
    try:
        return ai_plan(request)
    except Exception as exc:
        raise HTTPException(status_code=502, detail="The AI planner could not create a plan. Please try again.") from exc
