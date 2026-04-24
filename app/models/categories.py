from app.db.base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, ForeignKey

class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(Integer,primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, default="Другое")
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="categories")