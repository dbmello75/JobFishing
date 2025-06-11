import sqlite3
import os
import logging
from contextlib import contextmanager

DB_PATH = os.getenv("DB_PATH", "jobfishing.db")
logger = logging.getLogger(__name__)

if not os.path.exists(DB_PATH):
    raise FileNotFoundError(f"Banco de dados não encontrado em: {DB_PATH}")

@contextmanager
def db_connection():
    logger.debug("Abrindo conexão com o banco de dados.")
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row  # Permite acessar por nome da coluna
    try:
        yield conn
    finally:
        conn.close()
        logger.debug("Conexão com o banco de dados fechada.")
