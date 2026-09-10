# LSM System — v1

Plataforma de inteligencia futbolística. **v1 está acotada a propósito:**

- Solo **Club Irapuato** (sin Club León todavía).
- Un solo módulo: **Rankings** (goleadores, goles/partido, minutos jugados,
  % de minutos, titularidades).
- Sin login, sin Android, sin API pública, sin Docker/K8s/CI-CD.

Cualquier otra cosa (scouting, ficha de jugador, comparativas, alertas,
Club León, despliegue) es v2+ y se agrega solo después de que esta versión
funcione de punta a punta con datos reales.

## Estructura

```
lsm-system/
├── backend/
│   ├── app/
│   │   ├── main.py          # arranque de la API
│   │   ├── database.py      # SQLite + sesión
│   │   ├── models.py        # Player, Match, Appearance
│   │   ├── schemas.py       # RankingEntry
│   │   └── routers/
│   │       └── rankings.py  # único endpoint: GET /api/rankings
│   ├── data/                # aquí vive lsm.db (SQLite) y datasets fuente
│   └── requirements.txt
├── frontend/
│   └── index.html           # tabla simple, sin build step
└── README.md
```

## Cómo correrlo

```bash
cd backend
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Luego abrir `frontend/index.html` directo en el navegador (apunta a
`http://localhost:8000`).

## Siguiente paso pendiente

Todavía no hay datos cargados. Falta:
1. Definir de dónde salen los datos de jugadores/partidos de Irapuato
   (CSV manual, scraping, fuente ya existente).
2. Escribir un script de carga (`backend/data/seed.py`) que llene
   `players`, `matches` y `appearances`.

No agregar módulos nuevos hasta que Rankings funcione con datos reales
de principio a fin.
