import os
import sqlite3
from dotenv import load_dotenv
from fastapi import FastAPI
from app.routers import ads, groups

# Carrega variáveis de ambiente
load_dotenv()
DB_PATH = os.getenv("DB_PATH", "jobfishing.db")

app = FastAPI(title="JobFishing Backend")

def get_connection():
    return sqlite3.connect(DB_PATH, check_same_thread=False)

# Registra os routers
app.include_router(ads.router, prefix="/ads", tags=["Anúncios"])
app.include_router(groups.router, prefix="/groups", tags=["Grupos"])


