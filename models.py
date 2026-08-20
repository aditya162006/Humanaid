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
    donation_links: Mapped[list["DonationLink"]] = relationship(back_populates="crisis", cascade="all, delete-orphan")

class DonationLink(Base):

    __tablename__ = "donation_links"
    id: Mapped[int] = mapped_column(Integer,primary_key=True,autoincrement=True)
    organization: Mapped[str] = mapped_column(String,nullable=False)
    url: Mapped[str] = mapped_column(String,nullable=False)
    crisis_id: Mapped[int] = mapped_column(ForeignKey("crises.id"),nullable=False)
    crisis: Mapped["Crisis"] = relationship(back_populates="donation_links")

class Submission(Base):
    __tablename__ = "submissions"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    slang: Mapped[str] = mapped_column(String, nullable=False)
    title: Mapped[str] = mapped_column(String, nullable=False)
    country: Mapped[str] = mapped_column(String, nullable=False)
    category: Mapped[str] = mapped_column(String, nullable=False)
    search_query: Mapped[str] = mapped_column(String, nullable=False)
    submission_links: Mapped[list["SubmissionLink"]] = relationship( back_populates="submission", cascade="all, delete-orphan")

class SubmissionLink(Base):
    __tablename__ = "submission_links"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    organization: Mapped[str] = mapped_column(String, nullable=False)
    url: Mapped[str] = mapped_column(String, nullable=False)
    submission_id: Mapped[int] = mapped_column(ForeignKey("submissions.id"), nullable=False)
    submission: Mapped["Submission"] = relationship(back_populates="submission_links")
