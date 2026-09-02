from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.cart import Cart


class CartRepository:
    def __init__(self, db: AsyncSession):
        self.db = db


    async def get_by_user(self, user_id: int) -> Cart | None:
        result = await self.db.execute(
            select(Cart)
            .where(Cart.user_id==user_id)
        )

        return result.scalar_one_or_none()


    async def get_by_id(self, cart_id: int) -> Cart | None:
        result = await self.db.execute(
            select(Cart)
            .where(Cart.id==cart_id)
        )

        return result.scalar_one_or_none()


    async def delete(self, cart_id: int) -> None:
        result = await self.db.execute(
            select(Cart)
            .where(Cart.id==cart_id)
        )

        db_cart = result.scalar_one_or_none()

        if db_cart is None:
            return None

        await self.db.delete(db_cart)
        await self.db.commit()