from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException

from app.repositories.cart import CartRepository
from app.repositories.cart_item import CartItemRepository
from app.schemas.cart import CartResponse
from app.schemas.cart_item import CartItemCreate, CartItemResponse, CartItemUpdate


class CartService:
    def __init__(self, db: AsyncSession):
        self.cart_repository = CartRepository(db)
        self.cart_item_repository = CartItemRepository(db)


    async def get_cart_by_user(self, user_id: int) -> CartResponse | None:
        cart = await self.cart_repository.get_by_user(user_id)

        if cart is None:
            raise HTTPException(
                status_code=404,
                detail=f'Cart with user_id {user_id} not found'
            )

        return CartResponse.model_validate(cart)


    async def add_to_cart(self, cart_id: int, cart_item_data: CartItemCreate) -> CartItemResponse:
        existing_item = await self.cart_item_repository.get_by_product_and_cart(
            cart_item_data.product_id, cart_id
        )

        if existing_item is None:
            cart_item = await self.cart_item_repository.create(cart_id, cart_item_data)
        else:
            quantity = CartItemUpdate(quantity=existing_item.quantity + cart_item_data.quantity)
            cart_item = await self.cart_item_repository.update(existing_item.id, quantity)

        return CartItemResponse.model_validate(cart_item)


    async def decrease_quantity(self, cart_item_id: int, amount: int = 1) -> CartItemResponse | None:
        db_cart_item = await self.cart_item_repository.get_by_id(cart_item_id)

        if db_cart_item is None:
            raise HTTPException(
                status_code=404,
                detail=f'Cart item with id {cart_item_id} not found'
            )

        new_quantity = db_cart_item.quantity - amount 

        if new_quantity <= 0:
            await self.cart_item_repository.delete(cart_item_id)
            return None

        cart_item = await self.cart_item_repository.update(cart_item_id, CartItemUpdate(quantity=new_quantity))

        return CartItemResponse.model_validate(cart_item)