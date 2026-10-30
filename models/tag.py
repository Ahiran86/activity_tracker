from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.connection import Base


class Tag(Base):
    __tablename__ = "tags"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True
    )

    name: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        nullable=False
    )

    activities: Mapped[list["Activity"]] = relationship(
        secondary="activity_tags",
        back_populates="tags"
    )