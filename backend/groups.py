from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from db import get_db_connection
import random, string
from datetime import datetime

router = APIRouter()

class GroupLinkCreate(BaseModel):
    group_id: int

def generate_short_id(length=4):
    chars = string.ascii_lowercase + string.digits
    return ''.join(random.choices(chars, k=length))

@router.post("/group-link")
def create_group_link(data: GroupLinkCreate):
    short_id = generate_short_id()
    now = datetime.utcnow().isoformat()
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO group_links (short_id, group_id, click_count, created_at) VALUES (?, ?, 0, ?)",
        (short_id, data.group_id, now)
    )
    conn.commit()
    conn.close()
    return {"short_link": f"https://jfsh.io/g/{short_id}"}

@router.get("/g/{short_id}")
def redirect_group(short_id: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT group_id, click_count FROM group_links WHERE short_id = ?", (short_id,))
    row = cursor.fetchone()
    if not row:
        raise HTTPException(status_code=404, detail="Link não encontrado")
    group_id, count = row
    cursor.execute("UPDATE group_links SET click_count = ? WHERE short_id = ?", (count + 1, short_id))
    cursor.execute("SELECT link_whatsapp FROM whatsapp_groups WHERE id = ? AND active = 1", (group_id,))
    result = cursor.fetchone()
    conn.commit()
    conn.close()
    if not result:
        raise HTTPException(status_code=404, detail="Grupo não encontrado ou inativo")
    return {"redirect": result["link_whatsapp"]}
