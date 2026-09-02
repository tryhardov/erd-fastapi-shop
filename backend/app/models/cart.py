from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import func, ForeignKey
from datetime import datetime

from app.database import Base


class Cart(Base):
    __tablename__ = 'carts'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), unique=True)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())

    user: Mapped['User'] = relationship(back_populates='cart')
    items: Mapped[list['CartItem']] = relationship(back_populates='cart')

    def __repr__(self):
        return f'Cart(id = {self.id} || user_id = {self.user_id})'