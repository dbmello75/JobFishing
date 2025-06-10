from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from uuid import uuid4, UUID
from datetime import datetime, timedelta
import sqlite3
import os
import random
import string


router = APIRouter()

DB_PATH = os.getenv("DB_PATH", "jobfishing.db")

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

class AdCreateRequest(BaseModel):
    title: str
    description: str
    employer_phone: str
    days_valid: int
    state: str
    region: str
    ingles: str
    precisa_carro: bool
    requer_itin: bool


def generate_short_id(length=4):
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))

@router.post("/create-ad")
def create_ad(payload: AdCreateRequest):
    ad_id = uuid4()
    now = datetime.utcnow()
    expires = now + timedelta(days=payload.days_valid)
    short_id = generate_short_id()

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO ads (id, short_id, title, description, employer_phone, created_at, expires_at)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (str(ad_id), short_id, payload.title, payload.description, payload.employer_phone, now.isoformat(), expires.isoformat()))
    conn.commit()
    conn.close()

    return {"message": "Anúncio criado com sucesso!", "short_link": f"https://jfsh.io/r/{short_id}"}

@router.get("/anuncio/{ad_id}")
def get_anuncio(ad_id: UUID):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM ads WHERE id = ?", (str(ad_id),))
    ad = cursor.fetchone()
    conn.close()

    if not ad:
        raise HTTPException(status_code=404, detail="Anúncio não encontrado")

    return {key: ad[key] for key in ad.keys()}

@router.get("/r/{short_id}")
def redirect_short(short_id: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM ads WHERE short_id = ?", (short_id,))
    result = cursor.fetchone()
    conn.close()

    if not result:
        raise HTTPException(status_code=404, detail="Link não encontrado")

    ad_id = result["id"]
    return {"redirect_to": f"https://jobfishing.us/anuncio.html?id={ad_id}"}


@router.get("/regions")
def get_regions():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM regions WHERE active = 1")
    rows = cursor.fetchall()
    conn.close()
    return [row[0] for row in rows]

    
@router.get("/locations")    
def get_locations():
    """
    Retorna lista de estados ativos e suas regiões ativas para preenchimento do formulário.
    Estrutura: [{ "state": "MA", "regions": ["MetroWest", ...] }, ...]
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT s.code, r.name
        FROM states s
        JOIN regions r ON r.state_id = s.id
        WHERE s.active = 1 AND r.active = 1
        ORDER BY s.code, r.name
    """)
    rows = cursor.fetchall()
    conn.close()

    locations = {}
    for state_code, region_name in rows:
        locations.setdefault(state_code, []).append(region_name)

    return [
        {"state": state, "regions": regions}
        for state, regions in locations.items()
    ]