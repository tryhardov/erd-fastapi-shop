from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.cart_item import CartItem
from app.schemas.cart_item import CartItemCreate, CartItemUpdate


class CartItemRepository:
    def __init__(self, db: AsyncSession):
        self.db = db


    async def get_by_id(self, cart_item_id: int) -> CartItem | None:
        result = await self.db.execute(
            select(CartItem)
            .where(CartItem.id==cart_item_id)
        )

        return result.scalar_one_or_none()


    async def get_cart_items_by_cart(self, cart_id: int) -> list[CartItem]:
        result = await self.db.execute(
            select(CartItem)
            .where(CartItem.cart_id==cart_id)
        )

        return result.scalars().all()


    async def get_by_product(self, product_id: int, cart_id: int) -> CartItem | None:
        result = await self.db.execute(
            select(CartItem)
            .where(CartItem.product_id==product_id,
                   CartItem.cart_id==cart_id)
        )

        return result.scalar_one_or_none()


    async def create(self,cart_id: int, cart_item_data: CartItemCreate) -> CartItem | None:
        db_cart_item = CartItem(**cart_item_data.model_dump(), cart_id=cart_id)

        existing_item = await self.get_by_product(cart_item_data.product_id, cart_id)
        
        if existing_item:
            return None

        self.db.add(db_cart_item)
        await self.db.commit()
        await self.db.refresh(db_cart_item)

        return db_cart_item


    async def update(self, cart_item_id: int, cart_item_data: CartItemUpdate) -> CartItem | None:
        result = await self.db.execute(
            select(CartItem)
            .where(CartItem.id==cart_item_id)
        )
        db_cart_item = result.scalar_one_or_none()

        if db_cart_item is None:
            return None

        for field, value in cart_item_data.model_dump(exclude_unset=True).items():
            setattr(db_cart_item, field, value)

        await self.db.commit()
        await self.db.refresh(db_cart_item)

        return db_cart_item


    async def delete(self, cart_item_id: int) -> None:
        result = await self.db.execute(
            select(CartItem)
            .where(CartItem.id==cart_item_id)
        )
        db_cart_item = result.scalar_one_or_none()

        if db_cart_item is None:
            return None

        await self.db.delete(db_cart_item)
        await self.db.commit()