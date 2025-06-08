import os
import random
import string
import sqlite3
from uuid import uuid4
from datetime import datetime, timedelta
from typing import Optional

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse, HTMLResponse
from pydantic import BaseModel

# Carrega variáveis do .env
env_path = os.path.join(os.path.dirname(__file__), '..', '.env')
load_dotenv(dotenv_path=env_path)

REDIRECT_DOMAIN = os.getenv("REDIRECT_DOMAIN", "https://jobfishing.us")
SHORTLINK_DOMAIN = os.getenv("SHORTLINK_DOMAIN", "https://jfsh.io")

app = FastAPI()

DB_FILE = "jobfishing.db"

def init_db():
    with sqlite3.connect(DB_FILE) as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS ads (
                id TEXT PRIMARY KEY,
                short_id TEXT UNIQUE,
                title TEXT,
                description TEXT,
                employer_phone TEXT,
                region TEXT,
                english_level TEXT,
                requires_car INTEGER,
                requires_itin INTEGER,
                created_at TEXT,
                expires_at TEXT,
                active INTEGER,
                click_count INTEGER
            )
        ''')

init_db()

class AdCreateRequest(BaseModel):
    title: str
    description: str
    employer_phone: str
    region: Optional[str] = None
    english_level: Optional[str] = None
    requires_car: Optional[bool] = False
    requires_itin: Optional[bool] = False
    days_valid: Optional[int] = 7

def generate_short_id(length=4):
    chars = string.ascii_lowercase + string.digits
    return ''.join(random.choices(chars, k=length))

def get_ad_by_short_id(short_id: str):
    with sqlite3.connect(DB_FILE) as conn:
        conn.row_factory = sqlite3.Row
        cur = conn.execute("SELECT * FROM ads WHERE short_id = ?", (short_id,))
        return cur.fetchone()

def get_ad_by_uuid(ad_id: str):
    with sqlite3.connect(DB_FILE) as conn:
        conn.row_factory = sqlite3.Row
        cur = conn.execute("SELECT * FROM ads WHERE id = ?", (ad_id,))
        return cur.fetchone()

@app.post("/create-ad")
def create_ad(payload: AdCreateRequest):
    ad_id = str(uuid4())
    now = datetime.utcnow()
    expires = now + timedelta(days=payload.days_valid)

    while True:
        short_id = generate_short_id()
        if not get_ad_by_short_id(short_id):
            break

    short_link = f"{SHORTLINK_DOMAIN}/r/{short_id}"

    with sqlite3.connect(DB_FILE) as conn:
        conn.execute('''INSERT INTO ads (
            id, short_id, title, description, employer_phone, region,
            english_level, requires_car, requires_itin,
            created_at, expires_at, active, click_count
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 1, 0)''', (
            ad_id, short_id, payload.title, payload.description,
            payload.employer_phone, payload.region,
            payload.english_level, int(payload.requires_car), int(payload.requires_itin),
            now.isoformat(), expires.isoformat()
        ))

    return {"message": "Anúncio criado com sucesso!", "short_link": short_link}

@app.post("/deactivate-ad/{short_id}")
def deactivate_ad(short_id: str):
    with sqlite3.connect(DB_FILE) as conn:
        cur = conn.execute("UPDATE ads SET active = 0 WHERE short_id = ?", (short_id,))
        if cur.rowcount == 0:
            raise HTTPException(status_code=404, detail="Anúncio não encontrado")
    return {"message": "Anúncio desativado com sucesso."}

@app.get("/r/{short_id}")
def redirect_link(short_id: str):
    ad = get_ad_by_short_id(short_id)
    if not ad:
        raise HTTPException(status_code=404, detail="Link não encontrado")

    if not ad["active"] or datetime.fromisoformat(ad["expires_at"]) <= datetime.utcnow():
        return HTMLResponse("<h2>Esta vaga foi preenchida ou expirou.</h2>", status_code=410)

    with sqlite3.connect(DB_FILE) as conn:
        conn.execute("UPDATE ads SET click_count = click_count + 1 WHERE short_id = ?", (short_id,))

    return RedirectResponse(url=f"{REDIRECT_DOMAIN}/anuncio.html?id={ad['id']}")

@app.get("/anuncio/{ad_id}")
def get_anuncio(ad_id: str):
    ad = get_ad_by_uuid(ad_id)
    if not ad:
        raise HTTPException(status_code=404, detail="Anúncio não encontrado")
    return dict(ad)
