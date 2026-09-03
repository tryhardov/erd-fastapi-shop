from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException

from app.schemas.product import ProductResponse, ProductListResponse, ProductCreate, ProductUpdate
from app.repositories.product import ProductRepository
from app.repositories.category import CategoryRepository


class ProductService:
    def __init__(self, db: AsyncSession):
        self.product_repository = ProductRepository(db)
        self.category_repository = CategoryRepository(db)


    async def get_all_products(self) -> ProductListResponse:
        products = await self.product_repository.get_all()
        product_response = [ProductResponse.model_validate(prod) for prod in products]

        return ProductListResponse(products=product_response, total=len(product_response))


    async def get_product_by_slug(self, product_slug: str) -> ProductResponse | None:
        product = await self.product_repository.get_by_slug(product_slug)

        if product is None:
            raise HTTPException(
                status_code=404,
                detail=f'Product with slug {product_slug} not found'
            )

        return ProductResponse.model_validate(product)


    async def get_products_by_category(self, category_id: int) -> ProductListResponse | None:
        products = await self.product_repository.get_by_category(category_id)
        product_response = [ProductResponse.model_validate(prod) for prod in products]

        return ProductListResponse(products=product_response, total=len(product_response))


    async def create_product(self, product_data: ProductCreate) -> ProductResponse:
        category = await self.category_repository.get_by_id(product_data.category_id)

        if category is None:
            raise HTTPException(
                status_code=404,
                detail=f'Category with id {product_data.category_id} not found'
            )

        product = await self.product_repository.create(product_data)

        return ProductResponse.model_validate(product)


    async def update_product(self, product_id: int, product_data: ProductUpdate) -> ProductResponse | None:
        if product_data.category_id is not None:
            category = await self.category_repository.get_by_id(product_data.category_id)
        
            if category is None:
                raise HTTPException(
                    status_code=404,
                    detail=f'Category with id {product_data.category_id} not found'
                )

        product = await self.product_repository.get_by_id(product_id)

        if product is None:
            raise HTTPException(
                status_code=404,
                detail=f'Product with id {product_id} not found'
            )

        product_response = await self.product_repository.update(product_id, product_data)

        return ProductResponse.model_validate(product_response)


    async def delete_product(self, product_id: int) -> None:
        product = await self.product_repository.get_by_id(product_id)

        if product is None:
            raise HTTPException(
                status_code=404,
                detail=f'Product with id {product_id} not found'
            )

        await self.product_repository.delete(product_id)