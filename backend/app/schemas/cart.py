from pydantic import ConfigDict, BaseModel, Field
from datetime import datetime
from decimal import Decimal

from app.schemas.user import UserResponse
from app.schemas.cart_item import CartItemResponse


class CartResponse(BaseModel):
    id: int
    user: UserResponse
    items: list[CartItemResponse]
    total_items: int
    total_price: Decimal
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)