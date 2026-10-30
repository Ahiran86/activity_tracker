from PySide6.QtCore import (
    QAbstractTableModel,
    Qt,
    QModelIndex
)


class ActivityTableModel(QAbstractTableModel):

    HEADERS = [
        "شناسه",
        "نام فعالیت",
        "زمان (دقیقه)",
        "دستاورد",
        "برچسب‌ها",
        "تاریخ ثبت"
    ]

    def __init__(self, activities=None):
        super().__init__()

        self.activities = activities or []

    def rowCount(self, parent=QModelIndex()):

        return len(self.activities)

    def columnCount(self, parent=QModelIndex()):

        return len(self.HEADERS)

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):

        if not index.isValid():
            return None

        if role == Qt.ItemDataRole.DisplayRole:

            activity = self.activities[index.row()]

            values = [
                activity.id,
                activity.name,
                activity.duration_minutes,
                activity.achievement or "-",
                "، ".join(tag.name for tag in activity.tags) or "-",
                activity.created_at.strftime("%Y-%m-%d %H:%M")
            ]

            return str(values[index.column()])

        if role == Qt.ItemDataRole.TextAlignmentRole:
            return int(Qt.AlignmentFlag.AlignCenter)

        return None

    def headerData(self, section, orientation, role):

        if role != Qt.ItemDataRole.DisplayRole:
            return None

        if orientation == Qt.Orientation.Horizontal:
            return self.HEADERS[section]

        return section + 1

    def set_activities(self, activities):

        self.beginResetModel()

        self.activities = activities

        self.endResetModel()

    def get_activity(self, row):

        if 0 <= row < len(self.activities):
            return self.activities[row]

        return None