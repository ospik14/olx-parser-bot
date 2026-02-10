from app.core.database import Base
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column


class Advertisement(Base):
    __tablename__='advertisements'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(255))
    image_url: Mapped[str]
    price: Mapped[str]
    location_and_date: Mapped[str]
    advert_url: Mapped[str] = mapped_column(unique=True)

class SearchTask(Base):
    __tablename__='search_tasks'

    id: Mapped[int] = mapped_column(primary_key=True)
    owner_id: Mapped[str]
    search_link: Mapped[str]
    is_active: Mapped[bool] = mapped_column(default=True)

class SearchAd(Base):
    __tablename__='search_ads'

    id: Mapped[int] = mapped_column(primary_key=True)
    ads_id: Mapped[int] = mapped_column(ForeignKey('advertisements.id', ondelete='CASCADE'))
    search_id: Mapped[int] = mapped_column(ForeignKey('search_tasks.id', ondelete='CASCADE'))
