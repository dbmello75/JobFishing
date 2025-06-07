# FastAPI backend com suporte a .env para links curtos com rastreamento e validade

import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse, HTMLResponse
from pydantic import BaseModel
from uuid import uuid4, UUID
from datetime import datetime, timedelta
from typing import Optional, Dict

# Carrega variáveis de ambiente
env_path = os.path.join(os.path.dirname(__file__), '..', '.env')
load_dotenv(dotenv_path=env_path)

REDIRECT_DOMAIN = os.getenv("REDIRECT_DOMAIN", "https://jobfising.us")
SHORTLINK_DOMAIN = os.getenv("SHORTLINK_DOMAIN", "https://jfsh.io")

app = FastAPI()

# Simulando banco de dados em memória
ads_db: Dict[str, "JobAd"] = {}

class JobAd(BaseModel):
    id: UUID
    title: str
    description: str
    employer_phone: str
    created_at: datetime
    expires_at: datetime
    active: bool = True
    short_link: str
    click_count: int = 0

@app.post("/create-ad")
def create_ad(title: str, description: str, employer_phone: str, days_valid: Optional[int] = 7):
    ad_id = uuid4()
    now = datetime.utcnow()
    expires = now + timedelta(days=days_valid)
    short_id = str(ad_id)[:8]
    short_link = f"{SHORTLINK_DOMAIN}/r/{short_id}"

    ad = JobAd(
        id=ad_id,
        title=title,
        description=description,
        employer_phone=employer_phone,
        created_at=now,
        expires_at=expires,
        short_link=short_link
    )
    ads_db[short_id] = ad
    return {"message": "Anúncio criado com sucesso!", "short_link": short_link}

@app.post("/deactivate-ad/{short_id}")
def deactivate_ad(short_id: str):
    ad = ads_db.get(short_id)
    if not ad:
        raise HTTPException(status_code=404, detail="Anúncio não encontrado")
    ad.active = False
    return {"message": "Anúncio desativado com sucesso."}

@app.get("/r/{short_id}")
def redirect_link(short_id: str):
    ad = ads_db.get(short_id)
    if not ad:
        raise HTTPException(status_code=404, detail="Link não encontrado")

    if not ad.active or ad.expires_at <= datetime.utcnow():
        return HTMLResponse(
            content="<h2>Esta vaga foi preenchida ou expirou.</h2>",
            status_code=410
        )

    ad.click_count += 1
    return RedirectResponse(url=f"{REDIRECT_DOMAIN}/anuncio/{ad.id}")
