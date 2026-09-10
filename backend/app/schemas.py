from pydantic import BaseModel


class RankingEntry(BaseModel):
    player_id: int
    full_name: str
    position: str | None
    category: str | None
    matches_played: int
    goals: int
    goals_per_match: float
    minutes_played: int
    minutes_percentage: float  # % de minutos posibles jugados
    starts: int

    class Config:
        from_attributes = True
