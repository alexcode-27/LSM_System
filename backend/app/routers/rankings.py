"""
Único módulo de v1. Todo criterio de ranking se calcula aquí
a partir de Appearance. Si en el futuro se agrega Scouting/Ficha
de jugador, ese va en su propio router — no se mezcla aquí.
"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, Integer, cast

from app.database import get_db
from app.models import Player, Appearance
from app.schemas import RankingEntry

router = APIRouter()

VALID_CRITERIA = {
    "goals": "goles",
    "goals_per_match": "goles por partido",
    "minutes_played": "minutos jugados",
    "minutes_percentage": "porcentaje de minutos",
    "starts": "titularidades",
}


@router.get("", response_model=list[RankingEntry])
def get_rankings(
    season: str | None = Query(None, description="ej. 2025-2026"),
    category: str | None = Query(None, description="ej. Primer equipo, Juvenil"),
    criteria: str = Query("goals", description=f"Uno de: {', '.join(VALID_CRITERIA)}"),
    limit: int = Query(20, le=100),
    db: Session = Depends(get_db),
):
    query = (
        db.query(
            Player.id.label("player_id"),
            Player.full_name,
            Player.jersey_number,
            Player.position,
            Player.category,
            func.count(Appearance.id).label("matches_played"),
            func.coalesce(func.sum(Appearance.goals), 0).label("goals"),
            func.coalesce(func.sum(Appearance.minutes_played), 0).label("minutes_played"),
            func.coalesce(func.sum(cast(Appearance.started, Integer)), 0).label("starts"),
        )
        .join(Appearance, Appearance.player_id == Player.id)
        .group_by(Player.id)
    )

    if category:
        query = query.filter(Player.category == category)

    results = query.all()

    entries = []
    for r in results:
        goals_per_match = round(r.goals / r.matches_played, 2) if r.matches_played else 0.0
        # % de minutos: referencia simple = 90 min * partidos jugados
        max_possible_minutes = r.matches_played * 90
        minutes_percentage = (
            round((r.minutes_played / max_possible_minutes) * 100, 1)
            if max_possible_minutes else 0.0
        )
        entries.append(
            RankingEntry(
                player_id=r.player_id,
                full_name=r.full_name,
                jersey_number=r.jersey_number,
                position=r.position,
                category=r.category,
                matches_played=r.matches_played,
                goals=r.goals,
                goals_per_match=goals_per_match,
                minutes_played=r.minutes_played,
                minutes_percentage=minutes_percentage,
                starts=r.starts,
            )
        )

    sort_key = criteria if criteria in VALID_CRITERIA else "goals"
    entries.sort(key=lambda e: getattr(e, sort_key), reverse=True)

    return entries[:limit]
