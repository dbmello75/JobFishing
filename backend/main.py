from fastapi import FastAPI, HTTPException, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from ads import router as ads_router, redirect_short
from groups import router as groups_router
from db import db_connection
from fastapi.responses import RedirectResponse

app = FastAPI(title="JobFishing API")

@app.get("/r/{short_id}")
def public_redirect_short(short_id: str):
    return redirect_short(short_id)  # ✅ já retorna RedirectResponse


# CORS para permitir o frontend acessar a API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/states")
def get_states():
    try:
        with db_connection() as conn:
            cur = conn.cursor()
            cur.execute("SELECT id, name FROM states WHERE active = 1")
            states = [{"id": row["id"], "name": row["name"]} for row in cur.fetchall()]
            return states
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/regions")
def get_regions():
    try:
        with db_connection() as conn:
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
            return regions
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Registra os roteadores
app.include_router(ads_router, prefix="/ads", tags=["Anúncios"])
app.include_router(groups_router, prefix="/groups", tags=["Grupos"])
