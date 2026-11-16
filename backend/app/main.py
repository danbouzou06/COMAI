from fastapi import FastAPI

app = FastAPI(
    title="COMAI API",
    version="0.1.0",
    description="API de la plateforme SaaS multi-agents COMAI.",
)


@app.get("/health", tags=["system"])
def health() -> dict[str, str]:
    return {"status": "ok", "service": "comai-api"}
