from fastapi import APIRouter, HTTPException
from fastapi.responses import RedirectResponse, HTMLResponse
from pydantic import BaseModel
from uuid import UUID, uuid4
from datetime import datetime, timedelta
import string, random
from ..main import get_db_connection

router = APIRouter()

class AdCreateRequest(BaseModel):
    title: str
    description: str
    employer_phone: str
    days_valid: int = 7

def generate_short_id(length=4):
    chars = string.ascii_lowercase + string.digits
    return ''.join(random.choices(chars, k=length))

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

@router.post("/deactivate-ad/{short_id}")
def deactivate_ad(short_id: str):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("UPDATE ads SET active = 0 WHERE short_id = ?", (short_id,))
    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Anúncio não encontrado")

    conn.commit()
    conn.close()

    return {"message": "Anúncio desativado com sucesso."}

@router.get("/r/{short_id}")
def redirect_link(short_id: str):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM ads WHERE short_id = ?", (short_id,))
    ad = cursor.fetchone()

    if not ad:
        raise HTTPException(status_code=404, detail="Link não encontrado")

    if not ad["active"] or ad["expires_at"] <= datetime.utcnow().isoformat():
        return HTMLResponse("<h2>Esta vaga foi preenchida ou expirou.</h2>", status_code=410)

    cursor.execute("UPDATE ads SET click_count = click_count + 1 WHERE short_id = ?", (short_id,))
    conn.commit()
    conn.close()

    return RedirectResponse(url=f"https://jobfishing.us/anuncio.html?id={ad['id']}")

@router.get("/anuncio/{ad_id}")
def get_anuncio(ad_id: UUID):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM ads WHERE id = ?", (str(ad_id),))
    ad = cursor.fetchone()

    conn.close()

    if not ad:
        raise HTTPException(status_code=404, detail="Anúncio não encontrado")

    return dict(ad)
