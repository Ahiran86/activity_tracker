from datetime import datetime, time, timedelta

from sqlalchemy import select, func
from sqlalchemy.orm import Session

from models.activity import Activity


class ReportService:

    @staticmethod
    def daily_report(db: Session, target_date=None):

        if target_date is None:
            target_date = datetime.now().date()

        start = datetime.combine(target_date, time.min)
        end = start + timedelta(days=1)

        statement = (
            select(
                func.count(Activity.id),
                func.coalesce(func.sum(Activity.duration_minutes), 0)
            )
            .where(
                Activity.created_at >= start,
                Activity.created_at < end
            )
        )

        count, total = db.execute(statement).one()

        return {
            "date": target_date,
            "activity_count": count,
            "total_minutes": total
        }

    @staticmethod
    def weekly_report(db: Session, target_date=None):

        if target_date is None:
            target_date = datetime.now().date()

        week_start = target_date - timedelta(
            days=target_date.weekday()
        )

        start = datetime.combine(week_start, time.min)
        end = start + timedelta(days=7)

        statement = (
            select(
                func.count(Activity.id),
                func.coalesce(func.sum(Activity.duration_minutes), 0)
            )
            .where(
                Activity.created_at >= start,
                Activity.created_at < end
            )
        )

        count, total = db.execute(statement).one()

        return {
            "week_start": week_start,
            "activity_count": count,
            "total_minutes": total
        }