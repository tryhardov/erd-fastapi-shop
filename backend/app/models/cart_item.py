from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import func, ForeignKey, UniqueConstraint
from datetime import datetime

from app.database import Base


class CartItem(Base):
    __tablename__ = 'cart_items'

    id: Mapped[int] = mapped_column(primary_key=True)
    cart_id: Mapped[int] = mapped_column(ForeignKey('carts.id'))
    product_id: Mapped[int] = mapped_column(ForeignKey('products.id'))
    quantity: Mapped[int] = mapped_column(default=1)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())

    cart: Mapped['Cart'] = relationship(back_populates='items')
    product: Mapped['Product'] = relationship(back_populates='cart_items')

    __table_args__ = (UniqueConstraint('cart_id', 'product_id', name='uq_cart_product'),)

    def __repr__(self):
        return f'Cartitem(id = {self.id})'