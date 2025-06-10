from fastapi import FastAPI
from ads import router as ads_router
from groups import router as groups_router
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import sqlite3
import os

app = FastAPI(title="JobFishing API")

DB_PATH = os.getenv("DB_PATH", "jobfishing.db")

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# CORS para permitir o frontend acessar a API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ou restrinja ao seu domínio
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/states")
def get_states():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, name FROM states WHERE active = 1")
    states = [{"id": row["id"], "name": row["name"]} for row in cur.fetchall()]
    conn.close()
    return states

@app.get("/regions")
def get_regions():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, name, state_id, active FROM regions")
    regions = [
        {
            "id": row["id"],
            "name": row["name"],
            "state_id": row["state_id"],
            "active": bool(row["active"])
        }
        for row in cur.fetchall()
    ]
    conn.close()
    return regions


# Registra os roteadores
app.include_router(ads_router, prefix="/ads", tags=["Anúncios"])
app.include_router(groups_router, prefix="/groups", tags=["Grupos"])

@app.get("/states")
def get_states():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, name FROM states WHERE active = 1")
    states = [{"id": row[0], "name": row[1]} for row in cur.fetchall()]
    conn.close()
    return states

@app.get("/regions")
def get_regions():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, name, state_id, active FROM regions")
    regions = [{"id": row[0], "name": row[1], "state_id": row[2], "active": row[3]} for row in cur.fetchall()]
    conn.close()
    return regions