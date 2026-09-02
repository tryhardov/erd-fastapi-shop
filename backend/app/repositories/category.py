from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from slugify import slugify

from app.models.category import Category
from app.schemas.category import CategoryCreate, CategoryUpdate


class CategoryRepository:
    def __init__(self, db: AsyncSession):
        self.db = db


    async def get_all(self) -> list[Category]:
        result = await self.db.execute(
            select(Category)
            )

        return result.scalars().all()


    async def get_by_id(self, category_id: int) -> Category | None:
        result = await self.db.execute(
            select(Category)
            .where(Category.id==category_id)
            )
        
        return result.scalar_one_or_none()


    async def get_by_slug(self, category_slug: str) -> Category | None:
        result = await self.db.execute(
            select(Category)
            .where(Category.slug==category_slug)
            )
        
        return result.scalar_one_or_none()


    async def create(self, category_data: CategoryCreate) -> Category:
        category_slug = slugify(category_data.name)
        db_category = Category(**category_data.model_dump(), slug=category_slug)
        self.db.add(db_category)
        await self.db.commit()
        await self.db.refresh(db_category)

        return db_category


    async def update(self, category_id: int, category_data: CategoryUpdate) -> Category | None:
        result = await self.db.execute(
            select(Category)
            .where(Category.id==category_id)
        )

        db_category = result.scalar_one_or_none()

        if db_category is None:
            return None

        for field, value in category_data.model_dump(exclude_unset=True).items():
            setattr(db_category, field, value)

        await self.db.commit()
        await self.db.refresh(db_category)

        return db_category


    async def delete(self, category_id: int) -> None:
        result = await self.db.execute(
            select(Category)
            .where(Category.id==category_id)
        )

        db_category = result.scalar_one_or_none()

        if db_category is None: 
            return None

        await self.db.delete(db_category)
        await self.db.commit()