from sqlalchemy import String, Integer, ForeignKey, Column
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session,relationship

class Base(DeclarativeBase):
    pass

class Crisis(Base):

    __tablename__ = "crises"
    id: Mapped[int] = mapped_column(Integer,primary_key=True,autoincrement=True)
    slang: Mapped[str] = mapped_column(String,unique=True,nullable=False)
    title: Mapped[str] = mapped_column(String,nullable=False)
    country: Mapped[str] = mapped_column(String,nullable=False)
    category: Mapped[str] = mapped_column(String,nullable=False)
    search_query: Mapped[str] = mapped_column(String,nullable=False)
    donation_links: Mapped[list["DonationLink"]] = relationship(back_populates="crisis")

class DonationLink(Base):
    __tablename__ = "donation_links"
    id: Mapped[int] = mapped_column(Integer,primary_key=True,autoincrement=True)
    organization: Mapped[str] = mapped_column(String,nullable=False)
    url: Mapped[str] = mapped_column(String,nullable=False)
    crisis_id: Mapped[int] = mapped_column(ForeignKey("crises.id"),nullable=False)
    crisis: Mapped["Crisis"] = relationship(back_populates="donation_links")

