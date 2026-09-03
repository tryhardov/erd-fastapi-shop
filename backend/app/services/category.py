from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException

from app.repositories.category import CategoryRepository
from app.schemas.category import CategoryResponse, CategoryCreate, CategoryUpdate


class CategoryService:
    def __init__(self, db: AsyncSession):
        self.category_repository = CategoryRepository(db)


    async def get_all_categories(self) -> list[CategoryResponse]:
        categories = await self.category_repository.get_all()

        return [CategoryResponse.model_validate(cat) for cat in categories]


    async def get_category_by_slug(self, category_slug: str) -> CategoryResponse | None:
        category = await self.category_repository.get_by_slug(category_slug)

        if category is None:
            raise HTTPException(
                status_code=404,
                detail=f'Category with slug {category_slug} not found'
            )

        return CategoryResponse.model_validate(category)


    async def create_category(self, category_data: CategoryCreate) -> CategoryResponse:
        category = await self.category_repository.create(category_data)

        return CategoryResponse.model_validate(category)


    async def update(self, category_id: int, category_data: CategoryUpdate) -> CategoryResponse | None:
        category = await self.category_repository.update(category_id, category_data)

        if category is None:
            raise HTTPException(
                status_code=404,
                detail=f'Category with id {category_id} not found'
            )

        return CategoryResponse.model_validate(category)


    async def delete(self, category_id: int) -> None:
        category = await self.category_repository.get_by_id(category_id)

        if category is None:
            raise HTTPException(
                status_code=404,
                detail=f'Category with id {category_id} not found'
            )

        await self.category_repository.delete(category_id)