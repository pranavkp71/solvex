from fastapi import FastAPI
from solvex.routers import lp

app = FastAPI(
    title="Solvex",
    version="0.0.1",
    description="Solve linear programming problems easily via API",
)

app.include_router(lp.router)


@app.get("/")
def read_root():
    return {
        "title": "Solvex",
        "description": "Solve linear programming problems easily via API",
        "version": "0.0.1",
    }


@app.get("/health")
def health():
    return {"status": "healthy", "services": "Solvex"}
