from sqlalchemy import select, func
from sqlalchemy.orm import Session, selectinload

from models.activity import Activity
from models.tag import Tag


class ActivityService:

    @staticmethod
    def create_activity(
        db: Session,
        name: str,
        duration_minutes: int,
        achievement: str | None = None,
        tag_ids: list[int] | None = None
    ) -> Activity:

        name = name.strip()

        if not name:
            raise ValueError("نام فعالیت نمی‌تواند خالی باشد.")

        if duration_minutes <= 0:
            raise ValueError("زمان فعالیت باید بیشتر از صفر باشد.")

        tag_ids = list(set(tag_ids or []))

        tags = []

        if tag_ids:
            tags = db.scalars(
                select(Tag).where(Tag.id.in_(tag_ids))
            ).all()

            if len(tags) != len(tag_ids):
                raise ValueError("یکی از برچسب‌های انتخاب‌شده وجود ندارد.")

        activity = Activity(
            name=name,
            duration_minutes=duration_minutes,
            achievement=achievement.strip() if achievement else None,
            tags=tags
        )

        try:
            db.add(activity)
            db.commit()
            db.refresh(activity)
            return activity

        except Exception:
            db.rollback()
            raise

    @staticmethod
    def get_all_activities(db: Session):

        statement = (
            select(Activity)
            .options(selectinload(Activity.tags))
            .order_by(Activity.created_at.desc())
        )

        return db.scalars(statement).all()

    @staticmethod
    def get_activity(db: Session, activity_id: int):

        statement = (
            select(Activity)
            .options(selectinload(Activity.tags))
            .where(Activity.id == activity_id)
        )

        return db.scalar(statement)

    @staticmethod
    def update_activity(
        db: Session,
        activity_id: int,
        name: str,
        duration_minutes: int,
        achievement: str | None = None,
        tag_ids: list[int] | None = None
    ) -> Activity:

        activity = ActivityService.get_activity(db, activity_id)

        if activity is None:
            raise ValueError("فعالیت موردنظر پیدا نشد.")

        name = name.strip()

        if not name:
            raise ValueError("نام فعالیت نمی‌تواند خالی باشد.")

        if duration_minutes <= 0:
            raise ValueError("زمان فعالیت باید بیشتر از صفر باشد.")

        tag_ids = list(set(tag_ids or []))

        tags = []

        if tag_ids:
            tags = db.scalars(
                select(Tag).where(Tag.id.in_(tag_ids))
            ).all()

            if len(tags) != len(tag_ids):
                raise ValueError("یکی از برچسب‌های انتخاب‌شده وجود ندارد.")

        try:
            activity.name = name
            activity.duration_minutes = duration_minutes
            activity.achievement = (
                achievement.strip() if achievement else None
            )
            activity.tags = tags

            db.commit()
            db.refresh(activity)

            return activity

        except Exception:
            db.rollback()
            raise

    @staticmethod
    def delete_activity(db: Session, activity_id: int):

        activity = db.get(Activity, activity_id)

        if activity is None:
            raise ValueError("فعالیت موردنظر پیدا نشد.")

        try:
            db.delete(activity)
            db.commit()

        except Exception:
            db.rollback()
            raise

    @staticmethod
    def get_total_duration(db: Session):

        statement = select(
            func.coalesce(
                func.sum(Activity.duration_minutes),
                0
            )
        )

        return db.scalar(statement)

    @staticmethod
    def filter_by_tags(
        db: Session,
        tag_ids: list[int],
        match_all: bool = False
    ):

        tag_ids = list(set(tag_ids or []))

        if not tag_ids:
            return ActivityService.get_all_activities(db)

        statement = (
            select(Activity)
            .options(selectinload(Activity.tags))
            .join(Activity.tags)
            .where(Tag.id.in_(tag_ids))
            .group_by(Activity.id)
        )

        if match_all:
            statement = statement.having(
                func.count(func.distinct(Tag.id)) == len(tag_ids)
            )

        statement = statement.order_by(Activity.created_at.desc())

        return db.scalars(statement).all()

    @staticmethod
    def search_activities(db: Session, keyword: str):

        keyword = keyword.strip()

        statement = (
            select(Activity)
            .options(selectinload(Activity.tags))
            .where(Activity.name.ilike(f"%{keyword}%"))
            .order_by(Activity.created_at.desc())
        )

        return db.scalars(statement).all()