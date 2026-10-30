
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QFrame, QLabel, QPushButton, QLineEdit,
    QTableView, QMessageBox, QFileDialog,
    QListWidget, QListWidgetItem, QCheckBox,
    QAbstractItemView, QHeaderView, QDialog
)

from PySide6.QtCore import Qt

from database.connection import SessionLocal

from services.activity_service import ActivityService
from services.tag_service import TagService
from services.report_service import ReportService
from services.excel_service import ExcelService

from ui.activity_dialog import ActivityDialog
from ui.tag_dialog import TagDialog
from ui.activity_table_model import ActivityTableModel


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Activity Tracker")
        self.resize(1250, 750)

        self.setup_ui()
        self.load_filter_tags()
        self.refresh_activities()

    def setup_ui(self):

        central = QWidget()
        self.setCentralWidget(central)

        main_layout = QHBoxLayout(central)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Sidebar

        sidebar = QFrame()
        sidebar.setObjectName("Sidebar")
        sidebar.setFixedWidth(220)

        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(18, 25, 18, 20)
        sidebar_layout.setSpacing(15)

        app_title = QLabel("ACTIVITY\nTRACKER")
        app_title.setObjectName("Title")

        sidebar_layout.addWidget(app_title)
        sidebar_layout.addSpacing(25)

        sidebar_layout.addWidget(QLabel("مدیریت فعالیت‌ها"))

        add_activity_button = QPushButton("＋  افزودن فعالیت")
        add_activity_button.setObjectName("PrimaryButton")
        add_activity_button.clicked.connect(self.add_activity)

        add_tag_button = QPushButton("＋  افزودن برچسب")
        add_tag_button.clicked.connect(self.add_tag)

        manage_tags_button = QPushButton("مدیریت / حذف برچسب‌ها")
        manage_tags_button.clicked.connect(self.manage_tags)

        sidebar_layout.addWidget(add_activity_button)
        sidebar_layout.addWidget(add_tag_button)
        sidebar_layout.addWidget(manage_tags_button)

        sidebar_layout.addSpacing(20)

        sidebar_layout.addWidget(QLabel("گزارش‌ها"))

        daily_button = QPushButton("گزارش روزانه")
        daily_button.clicked.connect(self.show_daily_report)

        weekly_button = QPushButton("گزارش هفتگی")
        weekly_button.clicked.connect(self.show_weekly_report)

        excel_button = QPushButton("خروجی Excel")
        excel_button.clicked.connect(self.export_excel)

        sidebar_layout.addWidget(daily_button)
        sidebar_layout.addWidget(weekly_button)
        sidebar_layout.addWidget(excel_button)

        sidebar_layout.addStretch()

        footer = QLabel("Personal Activity Manager")
        footer.setStyleSheet("color: #8996A8; font-size: 8pt;")

        sidebar_layout.addWidget(footer)

        # Main content

        content = QWidget()

        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(30, 25, 30, 25)
        content_layout.setSpacing(18)

        header_layout = QHBoxLayout()

        title = QLabel("فعالیت‌های من")
        title.setObjectName("Title")

        header_layout.addWidget(title)
        header_layout.addStretch()

        content_layout.addLayout(header_layout)

        # Statistics

        stats_layout = QHBoxLayout()

        self.activity_count_label = self.create_stat_card(
            stats_layout,
            "تعداد فعالیت‌ها",
            "0"
        )

        self.total_duration_label = self.create_stat_card(
            stats_layout,
            "مجموع زمان",
            "۰ ساعت و ۰ دقیقه"
        )

        content_layout.addLayout(stats_layout)

        # Search

        content_layout.addWidget(
            QLabel("جستجو و فیلتر فعالیت‌ها")
        )

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText(
            "جستجو بر اساس نام فعالیت..."
        )

        self.search_input.textChanged.connect(
            self.refresh_activities
        )

        content_layout.addWidget(self.search_input)

        content_layout.addWidget(QLabel("فیلتر بر اساس برچسب‌ها"))

        self.tag_filter_list = QListWidget()
        self.tag_filter_list.setMaximumHeight(90)

        self.tag_filter_list.setFlow(
            QListWidget.Flow.LeftToRight
        )

        self.tag_filter_list.setWrapping(True)
        self.tag_filter_list.setResizeMode(
            QListWidget.ResizeMode.Adjust
        )

        self.tag_filter_list.itemChanged.connect(
            self.refresh_activities
        )

        content_layout.addWidget(self.tag_filter_list)

        self.match_all_checkbox = QCheckBox(
            "فعالیت باید تمام برچسب‌های انتخاب‌شده را داشته باشد"
        )

        self.match_all_checkbox.stateChanged.connect(
            self.refresh_activities
        )

        content_layout.addWidget(self.match_all_checkbox)

        # Table

        table_header = QHBoxLayout()

        table_title = QLabel("لیست فعالیت‌ها")
        table_title.setObjectName("SectionTitle")

        table_header.addWidget(table_title)
        table_header.addStretch()

        content_layout.addLayout(table_header)

        self.table = QTableView()

        self.table_model = ActivityTableModel()
        self.table.setModel(self.table_model)

        self.table.setSelectionBehavior(
            QAbstractItemView.SelectionBehavior.SelectRows
        )

        self.table.setSelectionMode(
            QAbstractItemView.SelectionMode.SingleSelection
        )

        self.table.setAlternatingRowColors(True)
        self.table.verticalHeader().setVisible(False)

        self.table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )

        self.table.setEditTriggers(
            QAbstractItemView.EditTrigger.NoEditTriggers
        )

        self.table.doubleClicked.connect(
            self.edit_activity
        )

        content_layout.addWidget(self.table)

        # Action buttons

        actions_layout = QHBoxLayout()

        edit_button = QPushButton("ویرایش فعالیت")
        edit_button.clicked.connect(self.edit_activity)

        delete_button = QPushButton("حذف فعالیت")
        delete_button.setObjectName("DangerButton")
        delete_button.clicked.connect(self.delete_activity)

        actions_layout.addWidget(edit_button)
        actions_layout.addWidget(delete_button)
        actions_layout.addStretch()

        content_layout.addLayout(actions_layout)

        main_layout.addWidget(sidebar)
        main_layout.addWidget(content)

    def create_stat_card(self, parent_layout, caption, value):

        card = QFrame()
        card.setStyleSheet("""
            QFrame {
                background-color: #222B39;
                border-radius: 10px;
            }
        """)

        layout = QVBoxLayout(card)

        caption_label = QLabel(caption)
        caption_label.setObjectName("StatCaption")

        value_label = QLabel(value)
        value_label.setObjectName("StatValue")

        layout.addWidget(caption_label)
        layout.addWidget(value_label)

        parent_layout.addWidget(card)

        return value_label

    def load_filter_tags(self):

        self.tag_filter_list.blockSignals(True)
        self.tag_filter_list.clear()

        with SessionLocal() as db:

            tags = TagService.get_all_tags(db)

            for tag in tags:

                item = QListWidgetItem(tag.name)

                item.setData(
                    Qt.ItemDataRole.UserRole,
                    tag.id
                )

                item.setFlags(
                    item.flags() |
                    Qt.ItemFlag.ItemIsUserCheckable
                )

                item.setCheckState(
                    Qt.CheckState.Unchecked
                )

                self.tag_filter_list.addItem(item)

        self.tag_filter_list.blockSignals(False)

    def get_selected_tag_ids(self):

        selected_ids = []

        for index in range(self.tag_filter_list.count()):

            item = self.tag_filter_list.item(index)

            if item.checkState() == Qt.CheckState.Checked:
                selected_ids.append(
                    item.data(Qt.ItemDataRole.UserRole)
                )

        return selected_ids

    def refresh_activities(self, *args):

        with SessionLocal() as db:

            tag_ids = self.get_selected_tag_ids()

            if tag_ids:

                activities = ActivityService.filter_by_tags(
                    db,
                    tag_ids,
                    match_all=self.match_all_checkbox.isChecked()
                )

            else:

                activities = ActivityService.get_all_activities(db)

            keyword = self.search_input.text().strip().casefold()

            if keyword:

                activities = [
                    activity
                    for activity in activities
                    if keyword in activity.name.casefold()
                ]

            activities = list(activities)

            # Calculate statistics based on filtered activities

            activity_count = len(activities)

            total_minutes = sum(
                activity.duration_minutes
                for activity in activities
            )

            hours, remaining_minutes = divmod(
                total_minutes,
                60
            )

            self.table_model.set_activities(activities)

            self.activity_count_label.setText(
                str(activity_count)
            )

            self.total_duration_label.setText(
                f"{hours} ساعت و {remaining_minutes} دقیقه"
            )

    def add_activity(self):

        with SessionLocal() as db:

            dialog = ActivityDialog(db, parent=self)

            if dialog.exec():

                data = dialog.get_data()

                try:

                    ActivityService.create_activity(
                        db=db,
                        **data
                    )

                except Exception as error:

                    db.rollback()

                    QMessageBox.warning(
                        self,
                        "خطا",
                        str(error)
                    )

                    return

        self.refresh_activities()

    def add_tag(self):

        dialog = TagDialog(self)

        if dialog.exec():

            name = dialog.get_name()

            try:

                with SessionLocal() as db:

                    TagService.create_tag(db, name)

            except Exception as error:

                QMessageBox.warning(
                    self,
                    "خطا",
                    str(error)
                )

                return

            self.load_filter_tags()
            self.refresh_activities()

    # Tag management

    def manage_tags(self):

        dialog = QDialog(self)
        dialog.setWindowTitle("مدیریت برچسب‌ها")
        dialog.setMinimumSize(380, 420)

        layout = QVBoxLayout(dialog)

        layout.addWidget(
            QLabel("برای حذف، یک برچسب را انتخاب کنید:")
        )

        tag_list = QListWidget()
        layout.addWidget(tag_list)

        def load_tags():

            tag_list.clear()

            with SessionLocal() as db:

                tags = TagService.get_all_tags(db)

                for tag in tags:

                    item = QListWidgetItem(tag.name)

                    item.setData(
                        Qt.ItemDataRole.UserRole,
                        tag.id
                    )

                    tag_list.addItem(item)

        def delete_selected_tag():

            item = tag_list.currentItem()

            if item is None:

                QMessageBox.information(
                    dialog,
                    "انتخاب برچسب",
                    "ابتدا یک برچسب را انتخاب کنید."
                )

                return

            tag_id = item.data(Qt.ItemDataRole.UserRole)
            tag_name = item.text()

            result = QMessageBox.question(
                dialog,
                "تأیید حذف برچسب",
                f"آیا از حذف برچسب «{tag_name}» مطمئن هستید؟\n"
                "فعالیت‌ها حذف نمی‌شوند و فقط این برچسب از آن‌ها جدا می‌شود.",
                QMessageBox.StandardButton.Yes |
                QMessageBox.StandardButton.No
            )

            if result != QMessageBox.StandardButton.Yes:
                return

            try:

                with SessionLocal() as db:

                    TagService.delete_tag(db, tag_id)

            except Exception as error:

                QMessageBox.warning(
                    dialog,
                    "خطا",
                    str(error)
                )

                return

            load_tags()
            self.load_filter_tags()
            self.refresh_activities()

        buttons_layout = QHBoxLayout()

        delete_button = QPushButton(
            "حذف برچسب انتخاب‌شده"
        )

        delete_button.setObjectName("DangerButton")
        delete_button.clicked.connect(delete_selected_tag)

        close_button = QPushButton("بستن")
        close_button.clicked.connect(dialog.accept)

        buttons_layout.addWidget(delete_button)
        buttons_layout.addWidget(close_button)

        layout.addLayout(buttons_layout)

        load_tags()
        dialog.exec()

    def get_selected_activity(self):

        selected_indexes = (
            self.table.selectionModel().selectedRows()
        )

        if not selected_indexes:
            return None

        row = selected_indexes[0].row()

        return self.table_model.get_activity(row)

    def edit_activity(self):

        selected = self.get_selected_activity()

        if selected is None:

            QMessageBox.information(
                self,
                "انتخاب فعالیت",
                "ابتدا یک فعالیت را از جدول انتخاب کنید."
            )

            return

        activity_id = selected.id

        with SessionLocal() as db:

            activity = ActivityService.get_activity(
                db,
                activity_id
            )

            if activity is None:
                return

            dialog = ActivityDialog(
                db,
                activity=activity,
                parent=self
            )

            if dialog.exec():

                data = dialog.get_data()

                try:

                    ActivityService.update_activity(
                        db,
                        activity_id,
                        **data
                    )

                except Exception as error:

                    db.rollback()

                    QMessageBox.warning(
                        self,
                        "خطا",
                        str(error)
                    )

                    return

        self.refresh_activities()

    def delete_activity(self):

        selected = self.get_selected_activity()

        if selected is None:

            QMessageBox.information(
                self,
                "انتخاب فعالیت",
                "ابتدا یک فعالیت را انتخاب کنید."
            )

            return

        result = QMessageBox.question(
            self,
            "حذف فعالیت",
            f"آیا از حذف فعالیت «{selected.name}» مطمئن هستید؟",
            QMessageBox.StandardButton.Yes |
            QMessageBox.StandardButton.No
        )

        if result != QMessageBox.StandardButton.Yes:
            return

        try:

            with SessionLocal() as db:

                ActivityService.delete_activity(
                    db,
                    selected.id
                )

        except Exception as error:

            QMessageBox.warning(
                self,
                "خطا",
                str(error)
            )

            return

        self.refresh_activities()

    def show_daily_report(self):

        with SessionLocal() as db:

            report = ReportService.daily_report(db)

        minutes = report["total_minutes"]

        hours, remaining = divmod(minutes, 60)

        QMessageBox.information(
            self,
            "گزارش روزانه",
            f"""
تاریخ: {report['date']}

تعداد فعالیت‌ها: {report['activity_count']}

مجموع زمان: {minutes} دقیقه

معادل: {hours} ساعت و {remaining} دقیقه
"""
        )

    def show_weekly_report(self):

        with SessionLocal() as db:

            report = ReportService.weekly_report(db)

        minutes = report["total_minutes"]

        hours, remaining = divmod(minutes, 60)

        QMessageBox.information(
            self,
            "گزارش هفتگی",
            f"""
شروع هفته: {report['week_start']}

تعداد فعالیت‌ها: {report['activity_count']}

مجموع زمان: {minutes} دقیقه

معادل: {hours} ساعت و {remaining} دقیقه
"""
        )

    def export_excel(self):

        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "ذخیره فایل Excel",
            "activities.xlsx",
            "Excel Files (*.xlsx)"
        )

        if not file_path:
            return

        if not file_path.lower().endswith(".xlsx"):
            file_path += ".xlsx"

        try:

            with SessionLocal() as db:

                ExcelService.export_activities(
                    db,
                    file_path
                )

            QMessageBox.information(
                self,
                "موفق",
                "فایل Excel با موفقیت ذخیره شد."
            )

        except Exception as error:

            QMessageBox.critical(
                self,
                "خطا",
                str(error)
            )
