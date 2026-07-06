"""Main v1 API router that aggregates all sub-routers."""
from fastapi import APIRouter

from app.api.v1 import (
    auth,
    chat,
    city_mood,
    city_summary,
    events,
    news,
    profile,
    reports,
    search,
    traffic,
    trains,
    trending,
    weather,
)

api_router = APIRouter(prefix="/api/v1")

api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(news.router, prefix="/news", tags=["News"])
api_router.include_router(weather.router, prefix="/weather", tags=["Weather"])
api_router.include_router(traffic.router, prefix="/traffic", tags=["Traffic"])
api_router.include_router(trains.router, prefix="/trains", tags=["Trains"])
api_router.include_router(events.router, prefix="/events", tags=["Events"])
api_router.include_router(reports.router, prefix="/reports", tags=["Community Reports"])
api_router.include_router(trending.router, prefix="/trending", tags=["Trending"])
api_router.include_router(city_summary.router, prefix="/city-summary", tags=["City Summary"])
api_router.include_router(city_mood.router, prefix="/city-mood", tags=["City Mood"])
api_router.include_router(chat.router, prefix="/chat", tags=["Ask Tapri"])
api_router.include_router(profile.router, prefix="/profile", tags=["Profile"])
api_router.include_router(search.router, prefix="/search", tags=["Search"])
