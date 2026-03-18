from pydantic import BaseModel


class ProductCreate(BaseModel):
    name: str
    description: str
    price: float


class ProductResponse(BaseModel):
    id: int
    name: str
    description: str
    price: float
    is_available: bool

    class Config:
        from_attributes = True

class ProductUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    price: float | None = None
    is_available: bool | None = None