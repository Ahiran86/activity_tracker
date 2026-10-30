from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel,
    QLineEdit, QPushButton, QHBoxLayout
)


class TagDialog(QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("افزودن برچسب")
        self.setMinimumWidth(350)

        layout = QVBoxLayout(self)

        layout.addWidget(QLabel("نام برچسب"))

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText(
            "مثلاً Python، دانشگاه، مطالعه"
        )

        layout.addWidget(self.name_input)

        buttons = QHBoxLayout()

        save_button = QPushButton("ذخیره")
        save_button.setObjectName("PrimaryButton")
        save_button.clicked.connect(self.accept)

        cancel_button = QPushButton("انصراف")
        cancel_button.clicked.connect(self.reject)

        buttons.addWidget(save_button)
        buttons.addWidget(cancel_button)

        layout.addLayout(buttons)

    def get_name(self):

        return self.name_input.text().strip()