from datetime import datetime
from core.database import Base
from sqlalchemy import String, ForeignKey, func, DateTime, BigInteger
from sqlalchemy.orm import Mapped, mapped_column


class Advertisement(Base):
    __tablename__='advertisements'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(255))
    image_url: Mapped[str | None]
    price: Mapped[str]
    location_and_date: Mapped[str]
    advert_url: Mapped[str] = mapped_column(unique=True)

class SearchTask(Base):
    __tablename__='search_tasks'

    id: Mapped[int] = mapped_column(primary_key=True)
    owner_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('users.id', ondelete='CASCADE'))
    search_link: Mapped[str]
    is_active: Mapped[bool] = mapped_column(default=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        server_default=func.now()
    )

class SearchAd(Base):
    __tablename__='search_ads'

    id: Mapped[int] = mapped_column(primary_key=True)
    ads_id: Mapped[int] = mapped_column(ForeignKey('advertisements.id', ondelete='CASCADE'))
    search_id: Mapped[int] = mapped_column(ForeignKey('search_tasks.id', ondelete='CASCADE'))

class User(Base):
    __tablename__='users'

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    username: Mapped[str]
    max_searches: Mapped[int] = mapped_column(default=3)

