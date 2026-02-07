from app.core.database import Base
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

class Advertisement(Base):
    __tablename__='advertisements'

    id: Mapped[int] = mapped_column(primary_key=True)
    advert_id: Mapped[int] = mapped_column(unique=True)
    title: Mapped[str] = mapped_column(String(255))
    image_url: Mapped[str]
    price: Mapped[int]
    location_and_date: Mapped[str]
    advert_url: Mapped[str] = mapped_column(unique=True)
