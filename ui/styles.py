"""
Style definitions for Mouse Pilot UI
Supports both light and dark themes with Windows 11 aesthetic
"""

LIGHT_THEME = """
QMainWindow {
    background-color: #F3F3F3;
}

QWidget {
    font-family: 'Segoe UI', Arial, sans-serif;
    font-size: 10pt;
}

QLabel {
    color: #1F1F1F;
}

QLabel#title {
    font-size: 24pt;
    font-weight: 600;
    color: #0078D4;
    padding: 10px;
}

QLabel#subtitle {
    font-size: 11pt;
    color: #605E5C;
}

QLabel#status {
    font-size: 14pt;
    font-weight: 600;
    padding: 8px 16px;
    border-radius: 8px;
    background-color: #E8E8E8;
}

QLabel#status[status="running"] {
    color: #107C10;
    background-color: #DFF6DD;
}

QLabel#status[status="paused"] {
    color: #CA5010;
    background-color: #FFF4CE;
}

QLabel#status[status="stopped"] {
    color: #605E5C;
    background-color: #E8E8E8;
}

QFrame#card {
    background-color: white;
    border-radius: 12px;
    border: 1px solid #E0E0E0;
    padding: 20px;
}

QPushButton {
    background-color: #0078D4;
    color: white;
    border: none;
    border-radius: 8px;
    padding: 12px 24px;
    font-size: 11pt;
    font-weight: 600;
}

QPushButton:hover {
    background-color: #106EBE;
}

QPushButton:pressed {
    background-color: #005A9E;
}

QPushButton:disabled {
    background-color: #E0E0E0;
    color: #A0A0A0;
}

QPushButton#stopButton {
    background-color: #D13438;
}

QPushButton#stopButton:hover {
    background-color: #B22222;
}

QPushButton#stopButton:pressed {
    background-color: #8B0000;
}

QPushButton#secondaryButton {
    background-color: #F3F3F3;
    color: #1F1F1F;
    border: 1px solid #CCCCCC;
}

QPushButton#secondaryButton:hover {
    background-color: #E8E8E8;
}

QComboBox {
    background-color: white;
    border: 1px solid #CCCCCC;
    border-radius: 6px;
    padding: 8px 12px;
    min-width: 150px;
}

QComboBox:hover {
    border: 1px solid #0078D4;
}

QComboBox::drop-down {
    border: none;
    width: 30px;
}

QComboBox::down-arrow {
    image: none;
    border-left: 5px solid transparent;
    border-right: 5px solid transparent;
    border-top: 5px solid #605E5C;
    margin-right: 5px;
}

QComboBox QAbstractItemView {
    background-color: white;
    border: 1px solid #CCCCCC;
    selection-background-color: #0078D4;
    selection-color: white;
}

QCheckBox {
    color: #1F1F1F;
    spacing: 8px;
}

QCheckBox::indicator {
    width: 20px;
    height: 20px;
    border: 1px solid #CCCCCC;
    border-radius: 4px;
    background-color: white;
}

QCheckBox::indicator:hover {
    border: 1px solid #0078D4;
}

QCheckBox::indicator:checked {
    background-color: #0078D4;
    border: 1px solid #0078D4;
    image: none;
}

QSpinBox {
    background-color: white;
    border: 1px solid #CCCCCC;
    border-radius: 6px;
    padding: 8px 12px;
    min-width: 100px;
}

QSpinBox:hover {
    border: 1px solid #0078D4;
}

QGroupBox {
    font-weight: 600;
    border: 1px solid #E0E0E0;
    border-radius: 8px;
    margin-top: 12px;
    padding-top: 12px;
}

QGroupBox::title {
    subcontrol-origin: margin;
    subcontrol-position: top left;
    padding: 0 8px;
    color: #0078D4;
}
"""

DARK_THEME = """
QMainWindow {
    background-color: #1F1F1F;
}

QWidget {
    font-family: 'Segoe UI', Arial, sans-serif;
    font-size: 10pt;
}

QLabel {
    color: #FFFFFF;
}

QLabel#title {
    font-size: 24pt;
    font-weight: 600;
    color: #60CDFF;
    padding: 10px;
}

QLabel#subtitle {
    font-size: 11pt;
    color: #C8C6C4;
}

QLabel#status {
    font-size: 14pt;
    font-weight: 600;
    padding: 8px 16px;
    border-radius: 8px;
    background-color: #323130;
}

QLabel#status[status="running"] {
    color: #6CCB5F;
    background-color: #2D4A2B;
}

QLabel#status[status="paused"] {
    color: #FFB900;
    background-color: #443D1C;
}

QLabel#status[status="stopped"] {
    color: #C8C6C4;
    background-color: #323130;
}

QFrame#card {
    background-color: #2D2D2D;
    border-radius: 12px;
    border: 1px solid #3F3F3F;
    padding: 20px;
}

QPushButton {
    background-color: #0078D4;
    color: white;
    border: none;
    border-radius: 8px;
    padding: 12px 24px;
    font-size: 11pt;
    font-weight: 600;
}

QPushButton:hover {
    background-color: #1A86D9;
}

QPushButton:pressed {
    background-color: #005A9E;
}

QPushButton:disabled {
    background-color: #3F3F3F;
    color: #797775;
}

QPushButton#stopButton {
    background-color: #E81123;
}

QPushButton#stopButton:hover {
    background-color: #F1707A;
}

QPushButton#stopButton:pressed {
    background-color: #C50F1F;
}

QPushButton#secondaryButton {
    background-color: #3F3F3F;
    color: #FFFFFF;
    border: 1px solid #5A5A5A;
}

QPushButton#secondaryButton:hover {
    background-color: #505050;
}

QComboBox {
    background-color: #2D2D2D;
    border: 1px solid #5A5A5A;
    border-radius: 6px;
    padding: 8px 12px;
    min-width: 150px;
    color: #FFFFFF;
}

QComboBox:hover {
    border: 1px solid #60CDFF;
}

QComboBox::drop-down {
    border: none;
    width: 30px;
}

QComboBox::down-arrow {
    image: none;
    border-left: 5px solid transparent;
    border-right: 5px solid transparent;
    border-top: 5px solid #C8C6C4;
    margin-right: 5px;
}

QComboBox QAbstractItemView {
    background-color: #2D2D2D;
    border: 1px solid #5A5A5A;
    selection-background-color: #0078D4;
    selection-color: white;
    color: #FFFFFF;
}

QCheckBox {
    color: #FFFFFF;
    spacing: 8px;
}

QCheckBox::indicator {
    width: 20px;
    height: 20px;
    border: 1px solid #5A5A5A;
    border-radius: 4px;
    background-color: #2D2D2D;
}

QCheckBox::indicator:hover {
    border: 1px solid #60CDFF;
}

QCheckBox::indicator:checked {
    background-color: #0078D4;
    border: 1px solid #0078D4;
    image: none;
}

QSpinBox {
    background-color: #2D2D2D;
    border: 1px solid #5A5A5A;
    border-radius: 6px;
    padding: 8px 12px;
    min-width: 100px;
    color: #FFFFFF;
}

QSpinBox:hover {
    border: 1px solid #60CDFF;
}

QSpinBox::up-button, QSpinBox::down-button {
    background-color: #3F3F3F;
    border: none;
}

QGroupBox {
    font-weight: 600;
    border: 1px solid #3F3F3F;
    border-radius: 8px;
    margin-top: 12px;
    padding-top: 12px;
    color: #FFFFFF;
}

QGroupBox::title {
    subcontrol-origin: margin;
    subcontrol-position: top left;
    padding: 0 8px;
    color: #60CDFF;
}
"""


def get_theme_stylesheet(theme_name):
    """Get stylesheet for the specified theme"""
    return DARK_THEME if theme_name == "dark" else LIGHT_THEME
