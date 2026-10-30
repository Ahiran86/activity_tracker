from sqlalchemy import select
from sqlalchemy.orm import Session

from models.tag import Tag


class TagService:

    @staticmethod
    def create_tag(db: Session, name: str) -> Tag:

        name = name.strip()

        if not name:
            raise ValueError("نام برچسب نمی‌تواند خالی باشد.")

        existing_tag = db.scalar(
            select(Tag).where(Tag.name == name)
        )

        if existing_tag:
            raise ValueError("این برچسب قبلاً ثبت شده است.")

        tag = Tag(name=name)

        try:
            db.add(tag)
            db.commit()
            db.refresh(tag)

            return tag

        except Exception:
            db.rollback()
            raise

    @staticmethod
    def get_all_tags(db: Session):

        statement = select(Tag).order_by(Tag.name)

        return db.scalars(statement).all()

    @staticmethod
    def delete_tag(db: Session, tag_id: int):

        tag = db.get(Tag, tag_id)

        if tag is None:
            raise ValueError("برچسب موردنظر پیدا نشد.")

        try:
            db.delete(tag)
            db.commit()

        except Exception:
            db.rollback()
            raise