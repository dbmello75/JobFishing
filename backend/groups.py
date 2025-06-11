from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from fastapi.responses import RedirectResponse
from db import db_connection
from datetime import datetime
import random, string
import os

router = APIRouter()

SHORTLINK_GROUP_PREFIX = os.getenv("SHORTLINK_GROUP_PREFIX", "https://jfsh.io/g/")

class GroupCreate(BaseModel):
    nome: str
    link_whatsapp: str

def generate_short_id(length=4):
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))

@router.post("/create")
def create(data: GroupCreate):
    short_id = generate_short_id()
    now = datetime.utcnow().isoformat()
    try:
        with db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO whatsapp_groups (nome, link_whatsapp, short_id, click_count, members_count, created_at, active)
                VALUES (?, ?, ?, 0, 0, ?, 1)
            """, (data.nome, data.link_whatsapp, short_id, now))
            conn.commit()
        return {"short_link": f"{SHORTLINK_GROUP_PREFIX}{short_id}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao cadastrar grupo: {str(e)}")

@router.get("/list")
def list_groups():
    try:
        with db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT nome, short_id, click_count FROM whatsapp_groups WHERE active = 1
            """)
            rows = cursor.fetchall()
        return [
            {
                "nome": row["nome"],
                "short_link": f"{SHORTLINK_GROUP_PREFIX}{row['short_id']}",
                "click_count": row["click_count"]
            }
            for row in rows
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao listar grupos: {str(e)}")

@router.get("/g/{short_id}")
def redirect_group(short_id: str):
    try:
        with db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT link_whatsapp, click_count FROM whatsapp_groups WHERE short_id = ? AND active = 1", (short_id,))
            row = cursor.fetchone()
            if not row:
                raise HTTPException(status_code=404, detail="Grupo não encontrado")
            link, count = row["link_whatsapp"], row["click_count"]
            cursor.execute("UPDATE whatsapp_groups SET click_count = ? WHERE short_id = ?", (count + 1, short_id))
            conn.commit()
        return RedirectResponse(url=link)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao redirecionar grupo: {str(e)}")
