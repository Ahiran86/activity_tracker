from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QSpinBox,
    QTextEdit,
    QPushButton,
    QCheckBox,
    QScrollArea,
    QWidget,
    QMessageBox
)

from services.tag_service import TagService


class ActivityDialog(QDialog):

    def __init__(self, db, activity=None, parent=None):
        super().__init__(parent)

        self.db = db
        self.activity = activity
        self.tag_checkboxes = {}

        self.setWindowTitle(
            "ویرایش فعالیت" if activity else "افزودن فعالیت"
        )

        self.setMinimumWidth(420)

        self.setup_ui()

    def setup_ui(self):

        layout = QVBoxLayout(self)
        layout.setSpacing(12)

        title = QLabel(
            "ویرایش فعالیت" if self.activity else "فعالیت جدید"
        )

        layout.addWidget(title)

        layout.addWidget(QLabel("نام فعالیت"))

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("مثلاً یادگیری Python")

        layout.addWidget(self.name_input)

        layout.addWidget(QLabel("زمان صرف‌شده (دقیقه)"))

        self.duration_input = QSpinBox()
        self.duration_input.setRange(1, 100000)
        self.duration_input.setValue(30)

        layout.addWidget(self.duration_input)

        layout.addWidget(QLabel("دستاورد (اختیاری)"))

        self.achievement_input = QTextEdit()
        self.achievement_input.setPlaceholderText(
            "امروز چه چیزی یاد گرفتی یا انجام دادی؟"
        )

        self.achievement_input.setMaximumHeight(90)

        layout.addWidget(self.achievement_input)

        layout.addWidget(QLabel("برچسب‌ها"))

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setMaximumHeight(150)

        tag_container = QWidget()

        self.tags_layout = QVBoxLayout(tag_container)

        self.load_tags()

        scroll.setWidget(tag_container)

        layout.addWidget(scroll)

        buttons = QHBoxLayout()

        save_button = QPushButton("ذخیره")
        save_button.setObjectName("PrimaryButton")
        save_button.clicked.connect(self.validate_and_accept)

        cancel_button = QPushButton("انصراف")
        cancel_button.clicked.connect(self.reject)

        buttons.addWidget(save_button)
        buttons.addWidget(cancel_button)

        layout.addLayout(buttons)

        if self.activity:
            self.load_activity()

    def load_tags(self):

        tags = TagService.get_all_tags(self.db)

        for tag in tags:

            checkbox = QCheckBox(tag.name)

            self.tag_checkboxes[tag.id] = checkbox

            self.tags_layout.addWidget(checkbox)

    def load_activity(self):

        self.name_input.setText(self.activity.name)

        self.duration_input.setValue(
            self.activity.duration_minutes
        )

        self.achievement_input.setPlainText(
            self.activity.achievement or ""
        )

        selected_ids = {
            tag.id for tag in self.activity.tags
        }

        for tag_id, checkbox in self.tag_checkboxes.items():

            checkbox.setChecked(tag_id in selected_ids)

    def validate_and_accept(self):

        if not self.name_input.text().strip():

            QMessageBox.warning(
                self,
                "خطا",
                "نام فعالیت را وارد کنید."
            )

            return

        self.accept()

    def get_data(self):

        selected_tag_ids = [
            tag_id
            for tag_id, checkbox in self.tag_checkboxes.items()
            if checkbox.isChecked()
        ]

        return {
            "name": self.name_input.text().strip(),
            "duration_minutes": self.duration_input.value(),
            "achievement": (
                self.achievement_input.toPlainText().strip() or None
            ),
            "tag_ids": selected_tag_ids
        }