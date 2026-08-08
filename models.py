from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session

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

    donation_links = relationship("DonationLink", back_populate="crisis")
class DonationLink(Base):
    __tablename__ = "donation_links"
    id: Mapped[int] = mapped_column(Integer,primary_key=True,autoincrement=True)
    organization: Mapped[str] = mapped_column(String,nullable=False)
    url: Mapped[str] = mapped_column(String,nullable=False)
    crisis_id: Mapped[int] = mapped_column(ForeignKey("crises.id"),nullable=False)

    crisis = relationship("Crisis", back_populates="donation_links")

