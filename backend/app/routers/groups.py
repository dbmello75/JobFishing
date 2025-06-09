# routers/groups.py

import sqlite3
from fastapi import APIRouter, HTTPException
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
from datetime import datetime
import os
import random
import string

router = APIRouter()
DB_PATH = os.getenv("DB_PATH", "jobfishing.db")


class GroupLinkCreate(BaseModel):
    group_id: int


@router.post("/create-group-link")
def create_group_link(data: GroupLinkCreate):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    short_id = generate_short_id()
    created_at = datetime.utcnow().isoformat()

    try:
        cur.execute("""
            INSERT INTO group_links (short_id, group_id, created_at)
            VALUES (?, ?, ?)
        """, (short_id, data.group_id, created_at))
        conn.commit()
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=400, detail="Erro ao criar link para grupo.")
    finally:
        conn.close()

    return {"short_link": f"https://jfsh.io/g/{short_id}"}


@router.get("/g/{short_id}")
def redirect_group_link(short_id: str):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("SELECT group_id, click_count FROM group_links WHERE short_id = ?", (short_id,))
    row = cur.fetchone()

    if not row:
        conn.close()
        raise HTTPException(status_code=404, detail="Link não encontrado.")

    group_id, clicks = row
    cur.execute("UPDATE group_links SET click_count = ? WHERE short_id = ?", (clicks + 1, short_id))

    cur.execute("SELECT link_whatsapp FROM whatsapp_groups WHERE id = ? AND active = 1", (group_id,))
    group = cur.fetchone()
    conn.commit()
    conn.close()

    if not group:
        raise HTTPException(status_code=404, detail="Grupo não encontrado ou inativo.")

    return RedirectResponse(url=group[0])


def generate_short_id(length=4):
    chars = string.ascii_lowercase + string.digits
    return ''.join(random.choices(chars, k=length))
