from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.core.db import create_db_and_tables
from app.api.v1.endpoints import auth
from app.api.v1.endpoints import user
from app.api.v1.endpoints import product


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup code
    await create_db_and_tables()
    yield
    # Shutdown code (optional)
    # e.g., close DB connections

# Create FastAPI app with lifespan
app = FastAPI(lifespan=lifespan)

# Root endpoint
@app.get("/")
async def root():
    return {"message": "API is working"}

# Include auth router
app.include_router(auth.router, prefix="/auth")

# Include user router
app.include_router(user.router, prefix="/users")

# Include product router
app.include_router(product.router, prefix="/products")