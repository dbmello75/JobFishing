from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field, validator
from uuid import uuid4, UUID
from datetime import datetime, timedelta
from db import db_connection
import random
import string
import os

router = APIRouter()

SHORT_URL_PREFIX = os.getenv("SHORT_URL_PREFIX", "https://jfsh.io/r/")
FULL_URL_PREFIX = os.getenv("FULL_URL_PREFIX", "https://jobfishing.us/anuncio.html?id=")

class AdCreateRequest(BaseModel):
    title: str
    description: str
    employer_phone: str
    days_valid: int = Field(gt=0)
    state: str
    region: str
    ingles: str
    precisa_carro: bool
    requer_itin: bool

    @validator("employer_phone")
    def validate_phone(cls, v):
        if not v.isdigit():
            raise ValueError("Telefone deve conter apenas números.")
        return v


@app.get("/categories")
def get_categories():
    try:
        with db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, name FROM categories WHERE active = 1")
            rows = cursor.fetchall()
        return [{"id": row["id"], "name": row["name"]} for row in rows]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



def generate_short_id(length=4):
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))

@router.post("/create-ad")
def create_ad(payload: AdCreateRequest):
    ad_id = uuid4()
    now = datetime.utcnow()
    expires = now + timedelta(days=payload.days_valid)
    short_id = generate_short_id()

    try:
        with db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO ads (id, short_id, title, description, employer_phone, created_at, expires_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (str(ad_id), short_id, payload.title, payload.description, payload.employer_phone, now.isoformat(), expires.isoformat()))
            conn.commit()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao criar anúncio: {str(e)}")

    return {"message": "Anúncio criado com sucesso!", "short_link": f"{SHORT_URL_PREFIX}{short_id}"}

@router.get("/anuncio/{ad_id}")
def get_anuncio(ad_id: UUID):
    try:
        with db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM ads WHERE id = ?", (str(ad_id),))
            ad = cursor.fetchone()
            if not ad:
                raise HTTPException(status_code=404, detail="Anúncio não encontrado")
            return {key: ad[key] for key in ad.keys()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
from fastapi.responses import RedirectResponse

@router.get("/r/{short_id}")
def redirect_short(short_id: str):
    try:
        with db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, click_count FROM ads WHERE short_id = ?", (short_id,))
            result = cursor.fetchone()
            if not result:
                raise HTTPException(status_code=404, detail="Link não encontrado")

            ad_id, count = result["id"], result["click_count"]
            cursor.execute("UPDATE ads SET click_count = ? WHERE id = ?", (count + 1, ad_id))
            conn.commit()

            return RedirectResponse(url=f"{FULL_URL_PREFIX}{ad_id}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/regions")
def get_regions():
    try:
        with db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM regions WHERE active = 1")
            rows = cursor.fetchall()
            return [row["name"] for row in rows]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/locations")    
def get_locations():
    try:
        with db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT s.code, r.name
                FROM states s
                JOIN regions r ON r.state_id = s.id
                WHERE s.active = 1 AND r.active = 1
                ORDER BY s.code, r.name
            """)
            rows = cursor.fetchall()
        locations = {}
        for state_code, region_name in rows:
            locations.setdefault(state_code, []).append(region_name)
        return [
            {"state": state, "regions": regions}
            for state, regions in locations.items()
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
