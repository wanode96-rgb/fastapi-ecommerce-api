from fastapi import FastAPI
from app.core.db import create_db_and_tables
from app.api.v1.endpoints import auth

app = FastAPI()

# Async startup event
@app.on_event("startup")
async def on_startup():
    await create_db_and_tables()

@app.get("/")
async def root():
    return {"message": "API is working"}

# Include auth router
app.include_router(auth.router, prefix="/auth")