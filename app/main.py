from fastapi import FastAPI
from app.core.db import create_db_and_tables
from app.api.v1.endpoints import auth

app = FastAPI()

@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.get("/")
def root():
    return {"message": "API is working"}

app.include_router(auth.router, prefix="/auth")