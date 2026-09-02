from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from slugify import slugify

from app.models.product import Product
from app.schemas.product import ProductCreate, ProductUpdate


class ProductRepository:
    def __init__(self, db: AsyncSession):
        self.db = db


    async def get_all(self) -> list[Product]:
        result = await self.db.execute(
            select(Product)
        )

        return result.scalars().all()


    async def get_by_id(self, product_id: int) -> Product | None:
        result = await self.db.execute(
            select(Product)
            .where(Product.id==product_id)
        )

        return result.scalar_one_or_none()


    async def get_by_slug(self, product_slug: str) -> Product | None:
        result = await self.db.execute(
            select(Product)
            .where(Product.slug==product_slug)
        )

        return result.scalar_one_or_none()


    async def get_by_category(self, category_id: int) -> list[Product]:
        result = await self.db.execute(
            select(Product)
            .where(Product.category_id==category_id)
        )

        return result.scalars().all()


    async def create(self, product_data: ProductCreate) -> Product:
        product_slug = slugify(product_data.name)
        db_product = Product(**product_data.model_dump(), slug=product_slug)

        self.db.add(db_product)
        await self.db.commit()
        await self.db.refresh(db_product)

        return db_product


    async def update(self, product_id: int, product_data: ProductUpdate) -> Product | None:
        result = await self.db.execute(
            select(Product)
            .where(Product.id==product_id)
        )

        db_product = result.scalar_one_or_none()

        if db_product is None:
            return None

        for field, value in product_data.model_dump(exclude_unset=True).items():
            setattr(db_product, field, value)

        await self.db.commit()
        await self.db.refresh(db_product)

        return db_product


    async def delete(self, product_id: int) -> None:
        result = await self.db.execute(
            select(Product)
            .where(Product.id==product_id)
        )

        db_product = result.scalar_one_or_none()

        if db_product is None:
            return None

        await self.db.delete(db_product)
        await self.db.commit()