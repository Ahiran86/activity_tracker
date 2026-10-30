
import sys
from pathlib import Path

from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QFontDatabase, QFont

from database.connection import Base, engine
from models.activity import Activity
from models.tag import Tag
from ui.main_window import MainWindow
from ui.styles import DARK_STYLE


def resource_path(relative_path):
    if getattr(sys, "frozen", False):
        base_path = Path(sys._MEIPASS)
    else:
        base_path = Path(__file__).resolve().parent

    return base_path / relative_path


def main():
    Base.metadata.create_all(bind=engine)

    app = QApplication(sys.argv)

    font_path = resource_path("fonts/RAY.TTF")

    font_id = QFontDatabase.addApplicationFont(str(font_path))

    if font_id == -1:
        print("Font RAY.TTF could not be loaded!")
    else:
        font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
        app.setFont(QFont(font_family, 10))

    app.setStyle("Fusion")
    app.setStyleSheet(DARK_STYLE)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        print(f"Application error: {error}")
        raise
