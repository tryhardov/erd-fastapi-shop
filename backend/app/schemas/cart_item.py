from pydantic import ConfigDict, BaseModel, Field
from datetime import datetime
from decimal import Decimal

from app.schemas.product import ProductResponse


class CartItemBase(BaseModel):
    product_id: int
    quantity: int = Field(..., gt=0)


class CartItemCreate(CartItemBase):
    pass


class CartItemUpdate(BaseModel):
    quantity : int | None = Field(None, gt=0)


class CartItemResponse(CartItemBase):
    id: int
    product: ProductResponse
    total_price: Decimal
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)