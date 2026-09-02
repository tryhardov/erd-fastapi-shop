from sqlalchemy import String, func
from sqlalchemy.orm import mapped_column, Mapped, relationship
from datetime import datetime

from app.database import Base


class Category(Base):
    __tablename__ = 'categories'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    slug: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    description: Mapped[str | None]
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())

    products: Mapped[list['Product']] = relationship(back_populates='category')

    def __repr__(self):
        return f'Category(id = {self.id} || name = {self.name})'