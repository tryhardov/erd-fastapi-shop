from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime
from decimal import Decimal

from app.schemas.category import CategoryResponse


class ProductBase(BaseModel):
    category_id: int
    name: str = Field(..., max_length=100)
    description: str | None = None
    price: Decimal = Field(..., gt=0, max_digits=10, decimal_places=2)
    image_url: str | None = None
    stock: int = Field(..., ge=0)
    is_available: bool = True


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    category_id: int | None = None
    name: str | None = None
    description: str | None = None
    price : Decimal | None = Field(None, gt=0)
    image_url: str | None = None
    stock: int | None = Field(None, ge=0)
    is_available: bool | None = None


class ProductResponse(ProductBase):
    id : int
    slug: str
    created_at: datetime
    updated_at: datetime
    category: CategoryResponse

    model_config = ConfigDict(from_attributes=True)


class ProductListResponse(BaseModel):
    products: list[ProductResponse]
    total: int