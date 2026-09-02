from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Numeric, func, ForeignKey
from datetime import datetime
from decimal import Decimal

from app.database import Base


class Product(Base):
    __tablename__ = 'products'

    id: Mapped[int] = mapped_column(primary_key=True)
    category_id: Mapped[int] = mapped_column(ForeignKey('categories.id'))
    name: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    slug: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    description: Mapped[str | None] 
    price: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    image_url: Mapped[str | None] 
    stock: Mapped[int] = mapped_column(default=0)
    is_available: Mapped[bool] = mapped_column(default=True)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())

    category: Mapped['Category'] = relationship(back_populates='products')
    cart_items: Mapped[list['CartItem']] = relationship(back_populates='product')

    def __repr__(self):
        return f'Product(id = {self.id} || name = {self.name}) in stock {self.stock}'