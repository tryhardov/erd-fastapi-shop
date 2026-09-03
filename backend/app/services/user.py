from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException

from app.repositories.user import UserRepository
from app.schemas.user import UserResponse, UserCreate, UserLogin, UserUpdate
from app.core.security import verify


class UserService:
    def __init__(self, db: AsyncSession):
        self.user_repository = UserRepository(db)


    async def get_user_by_id(self, user_id: int) -> UserResponse | None:
        user = await self.user_repository.get_by_id(user_id)

        if user is None:
            raise HTTPException(
                status_code=404,
                detail=f'User with id {user_id} not found'
            )
        
        return UserResponse.model_validate(user)


    async def register_user(self, user_data: UserCreate) -> UserResponse | None:
        existing_user = await self.user_repository.get_by_username_or_email(user_data.username, user_data.email)

        if existing_user:
            if existing_user.username == user_data.username and existing_user.email == user_data.email:
                raise HTTPException(
                    status_code=409,
                    detail=f'Username {user_data.username} and email {user_data.email} already taken'
                )
            elif existing_user.username == user_data.username:
                raise HTTPException(
                    status_code=409,
                    detail=f'Username {user_data.username} already taken'
                )
            elif existing_user.email == user_data.email:
                raise HTTPException(
                    status_code=409,
                    detail=f'Email {user_data.email} already taken'
                )

        db_user = await self.user_repository.create(user_data)

        return UserResponse.model_validate(db_user)


    async def update_user(self, user_id: int, user_data: UserUpdate) -> UserResponse | None:

        db_user = await self.user_repository.get_by_id(user_id)

        if db_user is None:
            raise HTTPException(
                status_code=404,
                detail=f'User with id {user_id} not found'
            )

        try:
            updated_user = await self.user_repository.update(user_id, user_data)
            return UserResponse.model_validate(updated_user)
        except ValueError:
            raise HTTPException(
                status_code=409,
                detail=f'Email or username already taken'
            )


    async def delete_user(self, user_id: int) -> None:
        db_user = await self.user_repository.get_by_id(user_id)

        if db_user is None:
            raise HTTPException(
                status_code=404,
                detail=f'User with if {user_id} not found'
            )

        await self.user_repository.delete(user_id)


    async def authenticate_user(self, login_data: UserLogin) -> UserResponse:
        db_user = await self.user_repository.get_by_username_or_email(login_data.login, login_data.login)

        if db_user is None or not verify(login_data.password, db_user.password_hash):
            raise HTTPException(
                status_code=401,
                detail=f'Incorrect login or password'
            )

        return UserResponse.model_validate(db_user)