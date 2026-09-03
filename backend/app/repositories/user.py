from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_
from sqlalchemy.exc import IntegrityError

from app.models.cart import Cart
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.core.security import hash_password


class UserRepository:
    def __init__(self, db: AsyncSession):
        self.db = db


    async def get_by_id(self, user_id: int) -> User | None:
        result = await self.db.execute(
            select(User)
            .where(User.id==user_id)
        )

        return result.scalar_one_or_none()


    async def get_by_username(self, username: str) -> User | None:
        result = await self.db.execute(
            select(User)
            .where(User.username==username)
        )

        return result.scalar_one_or_none()


    async def get_by_email(self, email: str) -> User | None:
        result = await self.db.execute(
            select(User)
            .where(User.email==email)
        )

        return result.scalar_one_or_none()


    async def get_by_username_or_email(self, username: str, email: str) -> User | None:
        result = await self.db.execute(
            select(User)
            .where(or_(User.username==username, User.email==email))
        )

        return result.scalar_one_or_none()


    async def create(self, user_data: UserCreate) -> User | None:
        existing_user = await self.get_by_username_or_email(user_data.username, user_data.email)

        if existing_user:
            return None

        db_user = User(email=user_data.email, username=user_data.username,
                               password_hash=hash_password(user_data.password), bio=user_data.bio)

        self.db.add(db_user)

        await self.db.flush()

        cart = Cart(user_id=db_user.id)

        self.db.add(cart)

        await self.db.commit()
        await self.db.refresh(db_user)
        await self.db.refresh(cart)

        return db_user


    async def update(self, user_id, user_data: UserUpdate) -> User | None:
        db_user = await self.get_by_id(user_id)

        if db_user is None:
            return None

        update_data = user_data.model_dump(exclude_unset=True)

        if 'password' in update_data.keys():
            update_data['password_hash'] = hash_password(update_data.pop('password'))

        for field, value in update_data.items():
            setattr(db_user, field, value)

        try:
            await self.db.commit()
        except IntegrityError:
            await self.db.rollback()
            raise ValueError('Username or email already taken')

        await self.db.refresh(db_user)

        return db_user


    async def delete(self, user_id: int) -> None:
        db_user = await self.get_by_id(user_id)

        if db_user is None:
            return None

        await self.db.delete(db_user)
        await self.db.commit()