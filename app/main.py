from contextlib import asynccontextmanager
from fastapi import FastAPI
from app import models

from app.api.v1.endpoints import auth
from app.api.v1.endpoints import user
from app.api.v1.endpoints import product
from app.api.v1.endpoints import cart
from app.api.v1.endpoints import order
from app.api.v1.endpoints import category
from app.api.v1.endpoints import review


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup code
    # await create_db_and_tables()
    print("Application is starting up...")
    yield
    # Shutdown code (optional)
    # e.g., close DB connections
    print("Application is shutting down...")

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

# Include cart router
app.include_router(cart.router, prefix="/cart")

# Include order router
app.include_router(order.router, prefix="/orders")

# Include category router
app.include_router(category.router, prefix="/categories")

# Include reviews router
app.include_router(review.router, prefix="/reviews")