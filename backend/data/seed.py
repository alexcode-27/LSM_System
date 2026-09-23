"""
Script de carga (seed) para LSM System v1.

Carga solo Club Deportivo Irapuato. No se guardan datos del rival:
el modelo Player no distingue equipo porque v1 solo trackea Irapuato.

Uso:
    cd backend
    python -m data.seed
    (o: python data/seed.py, ajustando el import de arriba según cómo lo corras)

IMPORTANTE: este script es idempotente a medias — si lo corres dos veces
vas a duplicar jugadores y partidos. Para v1 está bien correrlo una sola
vez sobre una base limpia. Si necesitas volver a correrlo, borra antes
backend/data/lsm.db.
"""
import sys
import os
from datetime import date

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import SessionLocal, init_db
from app.models import Player, Match, Appearance

# Números de camiseta confirmados en los informes arbitrales oficiales
# (J-1 a J-4). Solo se incluyen jugadores que efectivamente jugaron minutos.
JERSEY_NUMBERS = {
    "Padrón Romeo Sebastián": 1,
    "Morales Alejandro": 2,
    "Flores Rolando Daniel": 4,
    "Pérez Axel Oswaldo": 5,
    "Arriaga Johan Moisés": 6,
    "Montejano Emanuel": 7,
    "Sandoval Erick David": 9,
    "Martínez Francisco": 10,
    "Alatorre Jacobo": 11,
    "Barrientos José Manuel": 13,
    "Hernández Arturo Daniel": 14,
    "Villaseñor Gael Ronaldo": 15,
    "Nava Luis Joshua": 16,
    "García Tito Ian": 17,
    "Collazo Angel Gabriel": 19,
    "De La Rosa Heriberto": 21,
    "Sánchez Noé de Jesús": 23,
    "Aranda Juan Jesús": 31,
    "Arcila Jehan Nycolas": 44,
    "Araujo Luis Ángel": 50,
}


def get_or_create_player(db, full_name, position=None, category="Primer equipo"):
    player = db.query(Player).filter(Player.full_name == full_name).first()
    if player:
        return player
    player = Player(
        full_name=full_name,
        jersey_number=JERSEY_NUMBERS.get(full_name),
        position=position,
        category=category,
    )
    db.add(player)
    db.flush()  # para tener player.id sin hacer commit todavía
    return player


def seed_j1(db):
    """
    J-1: Club Deportivo Irapuato 2-1 Los Cabos United
    Sábado 29 de agosto de 2026, Estadio Sergio León Chávez.
    Fuente: informe arbitral oficial FMF (Torneo Liga 2026, Jornada 1).
    """
    match = Match(
        season="2026-2027",
        competition="Liga BBVA Expansión MX",
        match_date=date(2026, 8, 29),
        opponent="Los Cabos United",
    )
    db.add(match)
    db.flush()

    # (nombre completo, posición, minutos, goles)
    # Posiciones de titulares confirmadas en la página oficial de Liga BBVA
    # Expansión MX (mismo once que repitió completo en J-2). Posiciones de
    # suplentes que no aparecen ahí quedan en None a propósito: no inventar.
    appearances_data = [
        ("Padrón Romeo Sebastián", "Portero", 90, 0),
        ("Morales Alejandro", "Defensa", 90, 0),
        ("Flores Rolando Daniel", "Defensa", 90, 0),
        ("Pérez Axel Oswaldo", "Medio", 90, 0),
        ("García Tito Ian", "Defensa", 90, 1),          # gol min 35
        ("De La Rosa Heriberto", "Delantero", 90, 0),
        ("Sánchez Noé de Jesús", "Defensa", 90, 0),      # capitán, amarilla min 24
        ("Araujo Luis Ángel", "Medio", 90, 0),
        ("Hernández Arturo Daniel", "Delantero", 72, 0), # salió min 72
        ("Villaseñor Gael Ronaldo", "Medio", 81, 0),     # salió min 81
        ("Martínez Francisco", "Medio", 72, 0),          # salió min 72
        ("Arriaga Johan Moisés", None, 18, 0),           # entró min 72 (90-72)
        ("Barrientos José Manuel", "Medio", 9, 0),       # entró min 81 (90-81)
        ("Collazo Angel Gabriel", "Delantero", 18, 1),   # entró min 72, gol min 90+4
    ]

    starters = {
        "Padrón Romeo Sebastián", "Morales Alejandro", "Flores Rolando Daniel",
        "Pérez Axel Oswaldo", "García Tito Ian", "De La Rosa Heriberto",
        "Sánchez Noé de Jesús", "Araujo Luis Ángel", "Hernández Arturo Daniel",
        "Villaseñor Gael Ronaldo", "Martínez Francisco",
    }

    for full_name, position, minutes, goals in appearances_data:
        player = get_or_create_player(db, full_name, position=position)
        appearance = Appearance(
            player_id=player.id,
            match_id=match.id,
            minutes_played=minutes,
            started=full_name in starters,
            goals=goals,
        )
        db.add(appearance)


def seed_j2(db):
    """
    J-2: Cordobes Fútbol Club 0-3 Club Deportivo Irapuato
    Sábado 5 de septiembre de 2026, Estadio Municipal Los Pinos.
    Fuente: informe arbitral oficial FMF (Torneo Liga 2026, Jornada 2).

    El once titular es idéntico al de J-1 — mismos 11 jugadores, así que
    get_or_create_player los reutiliza en vez de duplicarlos.
    """
    match = Match(
        season="2026-2027",
        competition="Liga BBVA Expansión MX",
        match_date=date(2026, 9, 5),
        opponent="Cordobes Fútbol Club",
    )
    db.add(match)
    db.flush()

    appearances_data = [
        ("Padrón Romeo Sebastián", "Portero", 90, 0),
        ("Morales Alejandro", "Defensa", 90, 0),
        ("Flores Rolando Daniel", "Defensa", 90, 0),
        ("Pérez Axel Oswaldo", "Medio", 90, 0),
        ("García Tito Ian", "Defensa", 90, 0),            # amarilla min 69
        ("Sánchez Noé de Jesús", "Defensa", 90, 1),        # capitán, gol min 76
        ("Villaseñor Gael Ronaldo", "Medio", 45, 0),       # salió min 45
        ("Martínez Francisco", "Medio", 58, 0),            # salió min 58
        ("Hernández Arturo Daniel", "Delantero", 73, 1),   # salió min 73, gol min 13
        ("Araujo Luis Ángel", "Medio", 73, 0),             # salió min 73
        ("De La Rosa Heriberto", "Delantero", 83, 1),      # salió min 83, gol min 23
        ("Arcila Jehan Nycolas", None, 45, 0),             # entró min 45 (90-45)
        ("Barrientos José Manuel", None, 32, 0),           # entró min 58 (90-58)
        ("Montejano Emanuel", None, 17, 0),                # entró min 73 (90-73)
        ("Alatorre Jacobo", None, 17, 0),                  # entró min 73 (90-73)
        ("Sandoval Erick David", None, 7, 0),              # entró min 83 (90-83)
    ]

    starters = {
        "Padrón Romeo Sebastián", "Morales Alejandro", "Flores Rolando Daniel",
        "Pérez Axel Oswaldo", "García Tito Ian", "Sánchez Noé de Jesús",
        "Villaseñor Gael Ronaldo", "Martínez Francisco", "Hernández Arturo Daniel",
        "Araujo Luis Ángel", "De La Rosa Heriberto",
    }

    for full_name, position, minutes, goals in appearances_data:
        player = get_or_create_player(db, full_name, position=position)
        appearance = Appearance(
            player_id=player.id,
            match_id=match.id,
            minutes_played=minutes,
            started=full_name in starters,
            goals=goals,
        )
        db.add(appearance)


def seed_j3(db):
    """
    J-3: Club Deportivo Irapuato 2-1 Tigres de Álica FC
    Sábado 12 de septiembre de 2026, Estadio Sergio León Chávez.
    Fuente: informe arbitral oficial FMF (Torneo Liga 2026, Jornada 3).
    """
    match = Match(
        season="2026-2027",
        competition="Liga BBVA Expansión MX",
        match_date=date(2026, 9, 12),
        opponent="Tigres de Álica FC",
    )
    db.add(match)
    db.flush()

    appearances_data = [
        ("Padrón Romeo Sebastián", "Portero", 90, 0),
        ("Morales Alejandro", "Defensa", 90, 0),
        ("Flores Rolando Daniel", "Defensa", 90, 0),
        ("Pérez Axel Oswaldo", "Medio", 90, 0),
        ("García Tito Ian", "Defensa", 90, 0),             # amarilla min 30
        ("Sánchez Noé de Jesús", "Defensa", 90, 0),         # capitán
        ("Martínez Francisco", "Medio", 79, 0),             # salió min 79
        ("Hernández Arturo Daniel", "Delantero", 55, 1),    # salió min 55, gol min 40
        ("Villaseñor Gael Ronaldo", "Medio", 55, 0),        # salió min 55
        ("De La Rosa Heriberto", "Delantero", 79, 1),       # salió min 79, gol min 20
        ("Araujo Luis Ángel", "Medio", 64, 0),              # salió min 64
        ("Barrientos José Manuel", "Medio", 35, 0),         # entró min 55 (90-55)
        ("Collazo Angel Gabriel", "Delantero", 35, 0),      # entró min 55, amarilla min 90
        ("Alatorre Jacobo", None, 26, 0),                   # entró min 64 (90-64)
        ("Montejano Emanuel", None, 11, 0),                 # entró min 79 (90-79)
        ("Arcila Jehan Nycolas", None, 11, 0),               # entró min 79 (90-79)
    ]

    starters = {
        "Padrón Romeo Sebastián", "Morales Alejandro", "Flores Rolando Daniel",
        "Pérez Axel Oswaldo", "García Tito Ian", "Sánchez Noé de Jesús",
        "Martínez Francisco", "Hernández Arturo Daniel", "Villaseñor Gael Ronaldo",
        "De La Rosa Heriberto", "Araujo Luis Ángel",
    }

    for full_name, position, minutes, goals in appearances_data:
        player = get_or_create_player(db, full_name, position=position)
        appearance = Appearance(
            player_id=player.id,
            match_id=match.id,
            minutes_played=minutes,
            started=full_name in starters,
            goals=goals,
        )
        db.add(appearance)


def seed_j4(db):
    """
    J-4: Reboceros de La Piedad 2-3 Club Deportivo Irapuato
    Lunes 21 de septiembre de 2026, Estadio Juan N. López, La Piedad, Mich.
    Fuente: informe arbitral oficial FMF (Torneo Liga 2026, Jornada 4).

    El informe arbitral lista 4 "G" para jugadores de Irapuato, pero el
    marcador oficial solo acredita 3. Confirmado contra el detalle de goles
    de Liga BBVA Expansión MX: el gol de Barrientos José Manuel (min 64) fue
    autogol — cuenta para Reboceros, no para las estadísticas de Barrientos.
    Por eso su appearance queda con goals=0 aunque jugó esos minutos.
    """
    match = Match(
        season="2026-2027",
        competition="Liga BBVA Expansión MX",
        match_date=date(2026, 9, 21),
        opponent="Reboceros de La Piedad",
    )
    db.add(match)
    db.flush()

    appearances_data = [
        ("Flores Rolando Daniel", "Defensa", 90, 0),
        ("Pérez Axel Oswaldo", "Medio", 90, 0),
        ("Nava Luis Joshua", "Portero", 90, 0),
        ("García Tito Ian", "Defensa", 90, 0),
        ("Sánchez Noé de Jesús", "Defensa", 90, 0),          # capitán, amarilla min 18
        ("Martínez Francisco", "Medio", 90, 1),              # gol min 61
        ("Morales Alejandro", "Defensa", 45, 0),             # salió min 45
        ("Villaseñor Gael Ronaldo", "Medio", 45, 0),         # salió min 45
        ("Hernández Arturo Daniel", "Delantero", 45, 1),     # salió min 45, gol min 3
        ("De La Rosa Heriberto", "Delantero", 55, 1),        # salió min 55, gol min 54
        ("Araujo Luis Ángel", "Medio", 79, 0),               # salió min 79
        ("Aranda Juan Jesús", None, 45, 0),                  # entró min 45, amarilla min 86
        ("Arcila Jehan Nycolas", None, 45, 0),                # entró min 45 (90-45)
        ("Barrientos José Manuel", "Medio", 45, 0),          # entró min 45; autogol min 64, no cuenta como gol propio
        ("Sandoval Erick David", None, 35, 0),                # entró min 55 (90-55)
        ("Collazo Angel Gabriel", "Delantero", 11, 0),        # entró min 79 (90-79)
    ]

    starters = {
        "Flores Rolando Daniel", "Pérez Axel Oswaldo", "Nava Luis Joshua",
        "García Tito Ian", "Sánchez Noé de Jesús", "Martínez Francisco",
        "Morales Alejandro", "Villaseñor Gael Ronaldo", "Hernández Arturo Daniel",
        "De La Rosa Heriberto", "Araujo Luis Ángel",
    }

    for full_name, position, minutes, goals in appearances_data:
        player = get_or_create_player(db, full_name, position=position)
        appearance = Appearance(
            player_id=player.id,
            match_id=match.id,
            minutes_played=minutes,
            started=full_name in starters,
            goals=goals,
        )
        db.add(appearance)


def main():
    init_db()
    db = SessionLocal()
    try:
        seed_j1(db)
        seed_j2(db)
        seed_j3(db)
        seed_j4(db)
        db.commit()
        print("Carga completa: J-1, J-2, J-3 y J-4 cargados con datos reales verificados del informe arbitral FMF.")
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    main()
