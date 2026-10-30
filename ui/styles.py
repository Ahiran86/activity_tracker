DARK_STYLE = """
QWidget {
    background-color: #151923;
    color: #E6EAF0;
    font-family: "Ray";
    font-size: 10pt;
}

QMainWindow {
    background-color: #151923;
}

QFrame#Sidebar {
    background-color: #1C2330;
    border: none;
}

QLabel#Title {
    font-size: 20pt;
    font-weight: bold;
    color: #FFFFFF;
}

QLabel#SectionTitle {
    font-size: 13pt;
    font-weight: bold;
    color: #FFFFFF;
}

QLabel#StatValue {
    font-size: 22pt;
    font-weight: bold;
    color: #70B7FF;
}

QLabel#StatCaption {
    color: #AAB4C5;
    font-size: 9pt;
}

QPushButton {
    background-color: #29364A;
    color: #FFFFFF;
    border: none;
    border-radius: 7px;
    padding: 10px 14px;
}

QPushButton:hover {
    background-color: #364A66;
}

QPushButton#PrimaryButton {
    background-color: #2878C8;
    font-weight: bold;
}

QPushButton#PrimaryButton:hover {
    background-color: #358DE3;
}

QPushButton#DangerButton {
    background-color: #8C3540;
}

QPushButton#DangerButton:hover {
    background-color: #AA414D;
}

QLineEdit, QSpinBox, QTextEdit, QComboBox {
    background-color: #222B39;
    color: #FFFFFF;
    border: 1px solid #354255;
    border-radius: 6px;
    padding: 8px;
}

QTableView {
    background-color: #1C2330;
    alternate-background-color: #222B39;
    color: #E6EAF0;
    border: 1px solid #354255;
    border-radius: 8px;
    gridline-color: #354255;
    selection-background-color: #294D73;
    selection-color: #FFFFFF;
}

QHeaderView::section {
    background-color: #29364A;
    color: #FFFFFF;
    padding: 10px;
    border: none;
    font-weight: bold;
}

QCheckBox {
    spacing: 8px;
}

QCheckBox::indicator {
    width: 17px;
    height: 17px;
}

QCheckBox::indicator:unchecked {
    background-color: #222B39;
    border: 1px solid #52627A;
    border-radius: 4px;
}

QCheckBox::indicator:checked {
    background-color: #2878C8;
    border: 1px solid #2878C8;
    border-radius: 4px;
}

QDialog {
    background-color: #1C2330;
}

QScrollBar:vertical {
    background: #1C2330;
    width: 10px;
}

QScrollBar::handle:vertical {
    background: #46566D;
    border-radius: 4px;
}
"""