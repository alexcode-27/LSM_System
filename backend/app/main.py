"""
LSM System - v1
Punto de entrada de la API. v1 solo expone el módulo de Rankings
para Club Irapuato. Nada más se monta aquí a propósito.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import rankings
from app.database import init_db

app = FastAPI(
    title="LSM System API",
    description="Plataforma de inteligencia futbolística - Club Irapuato",
    version="1.0.0",
)

# CORS abierto en v1 porque el frontend corre local/sin dominio propio todavía.
# Restringir cuando haya despliegue real.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(rankings.router, prefix="/api/rankings", tags=["rankings"])


@app.on_event("startup")
def on_startup():
    init_db()


@app.get("/")
def root():
    return {"status": "ok", "service": "LSM System API", "version": "1.0.0"}
