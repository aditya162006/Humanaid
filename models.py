from sqlalchemy.orm import String, Integer, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
    pass
class Crisis(Base):
    __tablename__ = "crises"
    id: Mapped[int] = mapped_column(Integer,primary_key= True, autoincrement=True)
    slang: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    title: Mapped[str] = mapped_column(String, nullable=False)
    country: Mapped[str] = mapped_column(String, nullable=False)
    category: Mapped[str] = mapped_column(String, nullable=False)
    search_query: Mapped[str] = mapped_column(String, nullable=False)
