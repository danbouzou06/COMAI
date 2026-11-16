from fastapi import FastAPI

from app.api.routes.agents import router as agents_router
from app.api.routes.missions import router as missions_router

app = FastAPI(
    title="COMAI API",
    version="0.1.0",
    description="API de la plateforme SaaS multi-agents COMAI.",
)
app.include_router(agents_router, prefix="/api/v1")
app.include_router(missions_router, prefix="/api/v1")


@app.get("/health", tags=["system"])
def health() -> dict[str, str]:
    return {"status": "ok", "service": "comai-api"}
