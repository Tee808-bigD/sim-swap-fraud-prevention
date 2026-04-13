from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .config import get_settings
from .database import engine, Base
from .api import transactions, fraud, dashboard, verification

# Create tables
Base.metadata.create_all(bind=engine)

settings = get_settings()

app = FastAPI(title="SimGuard API", version="1.0.0")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(transactions.router, prefix="/api/transactions", tags=["transactions"])
app.include_router(fraud.router, prefix="/api/fraud", tags=["fraud"])
app.include_router(dashboard.router, prefix="/api/dashboard", tags=["dashboard"])
app.include_router(verification.router, prefix="/api/verification", tags=["verification"])

@app.get("/")
async def root():
    return {"message": "SimGuard API", "status": "running"}

@app.get("/health")
async def health():
    return {"status": "healthy"}