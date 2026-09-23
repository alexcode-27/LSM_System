"""
Modelos v1 - lo mínimo para calcular rankings:
goleadores, goles/partido, minutos jugados, % minutos, titularidades.

Sin tablas de scouting, comparativas ni alertas todavía.
"""
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Date
from sqlalchemy.orm import relationship

from app.database import Base


class Player(Base):
    __tablename__ = "players"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, nullable=False, index=True)
    jersey_number = Column(Integer, nullable=True)
    position = Column(String)          # ej. Delantero, Centrocampista
    category = Column(String)          # ej. Cadete, Juvenil, Primer equipo
    birth_date = Column(Date, nullable=True)

    appearances = relationship("Appearance", back_populates="player")


class Match(Base):
    __tablename__ = "matches"

    id = Column(Integer, primary_key=True, index=True)
    season = Column(String, nullable=False)     # ej. "2025-2026"
    competition = Column(String)
    match_date = Column(Date)
    opponent = Column(String)

    appearances = relationship("Appearance", back_populates="match")


class Appearance(Base):
    """Participación de un jugador en un partido: minutos, si fue titular, goles."""
    __tablename__ = "appearances"

    id = Column(Integer, primary_key=True, index=True)
    player_id = Column(Integer, ForeignKey("players.id"), nullable=False)
    match_id = Column(Integer, ForeignKey("matches.id"), nullable=False)

    minutes_played = Column(Integer, default=0)
    started = Column(Boolean, default=False)
    goals = Column(Integer, default=0)

    player = relationship("Player", back_populates="appearances")
    match = relationship("Match", back_populates="appearances")
