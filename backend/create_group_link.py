import sqlite3
import random
import string
from datetime import datetime

DB_PATH = "jobfishing.db"
SHORTLINK_DOMAIN = "https://jfsh.io"

def generate_short_id(length=4):
    chars = string.ascii_lowercase + string.digits
    return ''.join(random.choices(chars, k=length))

def create_group_short_link(group_id: int):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    short_id = generate_short_id()
    now = datetime.utcnow().isoformat()

    try:
        cur.execute("INSERT INTO group_links (short_id, group_id, created_at) VALUES (?, ?, ?)",
                    (short_id, group_id, now))
        conn.commit()
        print(f"✅ Link curto criado: {SHORTLINK_DOMAIN}/g/{short_id}")
    except sqlite3.IntegrityError:
        print("❌ Erro: ID de grupo inválido ou link já existe.")
    finally:
        conn.close()

if __name__ == "__main__":
    group_id = input("Digite o ID do grupo no banco: ").strip()
    if group_id.isdigit():
        create_group_short_link(int(group_id))
    else:
        print("⚠️ ID inválido.")
