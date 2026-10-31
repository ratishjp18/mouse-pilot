"""
Style definitions for Mouse Pilot UI
Supports both light and dark themes with Windows 11 aesthetic
"""

LIGHT_THEME = """
QMainWindow {
    background-color: transparent;
}

QWidget {
    font-family: 'Segoe UI', Arial, sans-serif;
    font-size: 10pt;
    background-color: transparent;
}

QLabel {
    color: #1F1F1F;
    background-color: transparent;
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

/* Single Circle Design */
QPushButton#mainCircle {
    background-color: transparent;
    border: 5px solid #0078D4;
    border-radius: 90px;
}

QPushButton#mainCircle:hover {
    background-color: transparent;
    border: 6px solid #106EBE;
}

QPushButton#mainCircle:pressed {
    background-color: transparent;
}

QPushButton#mainCircle[status="running"] {
    background-color: transparent;
    border: 5px solid #4CAF50;
}

QPushButton#mainCircle[status="running"]:hover {
    background-color: transparent;
    border: 6px solid #45A049;
}

QPushButton#mainCircle[status="paused"] {
    background-color: transparent;
    border: 5px solid #FFB900;
}

#circleStatus {
    font-size: 10pt;
    font-weight: 600;
    color: #1F1F1F;
    background: transparent;
}

#timerDisplay {
    font-size: 24pt;
    font-weight: 700;
    color: #0078D4;
    background: transparent;
    font-family: 'Consolas', 'Courier New', monospace;
}

#sessionDisplay {
    font-size: 9pt;
    color: #605E5C;
    background: transparent;
    font-family: 'Consolas', 'Courier New', monospace;
}

#mouseIcon {
    background: transparent;
}

#circleStatus {
    font-size: 18pt;
    font-weight: 600;
    color: #1F1F1F;
    background: transparent;
}

#timerDisplay {
    font-size: 36pt;
    font-weight: 700;
    color: #0078D4;
    background: transparent;
    font-family: 'Consolas', 'Courier New', monospace;
}

#sessionDisplay {
    font-size: 14pt;
    color: #605E5C;
    background: transparent;
    font-family: 'Consolas', 'Courier New', monospace;
}

QPushButton#circleButton {
    background-color: #E8E8E8;
    color: #1F1F1F;
    border-radius: 20px;
    font-size: 16pt;
    font-weight: 600;
    border: 2px solid #CCCCCC;
}

QPushButton#circleButton:hover {
    background-color: #D0D0D0;
    border: 2px solid #0078D4;
}

QPushButton#sideCircleButton {
    background-color: white;
    color: #0078D4;
    border-radius: 45px;
    font-size: 16pt;
    font-weight: 600;
    border: 3px solid #0078D4;
}

QPushButton#sideCircleButton:hover {
    background-color: #F0F8FF;
    border: 3px solid #106EBE;
}

QPushButton#sideCircleButton:pressed {
    background-color: #E0E0E0;
}

QPushButton#circleControlButton {
    background-color: #0078D4;
    color: white;
    border-radius: 35px;
    font-size: 24pt;
    border: none;
}

QPushButton#circleControlButton:hover {
    background-color: #106EBE;
}

QPushButton#circleControlButton:pressed {
    background-color: #005A9E;
}

QPushButton#circleControlButton:disabled {
    background-color: #E0E0E0;
    color: #A0A0A0;
}

QPushButton#circleControlButtonStop {
    background-color: #D13438;
    color: white;
    border-radius: 35px;
    font-size: 24pt;
    border: none;
}

QPushButton#circleControlButtonStop:hover {
    background-color: #B22222;
}

QPushButton#circleControlButtonStop:pressed {
    background-color: #8B0000;
}

QPushButton#circleControlButtonStop:disabled {
    background-color: #E0E0E0;
    color: #A0A0A0;
}
"""

DARK_THEME = """
QMainWindow {
    background-color: transparent;
}

QWidget {
    font-family: 'Segoe UI', Arial, sans-serif;
    font-size: 10pt;
    background-color: transparent;
}

QLabel {
    color: #FFFFFF;
    background-color: transparent;
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

/* Single Circle Design - Dark */
QPushButton#mainCircle {
    background-color: transparent;
    border: 5px solid #60CDFF;
    border-radius: 90px;
}

QPushButton#mainCircle:hover {
    background-color: transparent;
    border: 6px solid #1A86D9;
}

QPushButton#mainCircle:pressed {
    background-color: transparent;
}

QPushButton#mainCircle[status="running"] {
    background-color: transparent;
    border: 5px solid #6CCB5F;
}

QPushButton#mainCircle[status="running"]:hover {
    background-color: transparent;
    border: 6px solid #5FBF52;
}

QPushButton#mainCircle[status="paused"] {
    background-color: transparent;
    border: 5px solid #FFB900;
}

#mouseIcon {
    background: transparent;
}

#circleStatus {
    font-size: 18pt;
    font-weight: 600;
    color: #FFFFFF;
    background: transparent;
}

#timerDisplay {
    font-size: 36pt;
    font-weight: 700;
    color: #60CDFF;
    background: transparent;
    font-family: 'Consolas', 'Courier New', monospace;
}

#sessionDisplay {
    font-size: 14pt;
    color: #C8C6C4;
    background: transparent;
    font-family: 'Consolas', 'Courier New', monospace;
}

QPushButton#circleButton {
    background-color: #3F3F3F;
    color: #FFFFFF;
    border-radius: 20px;
    font-size: 16pt;
    font-weight: 600;
    border: 2px solid #5A5A5A;
}

QPushButton#circleButton:hover {
    background-color: #505050;
    border: 2px solid #60CDFF;
}

QPushButton#sideCircleButton {
    background-color: #2D2D2D;
    color: #60CDFF;
    border-radius: 45px;
    font-size: 16pt;
    font-weight: 600;
    border: 3px solid #60CDFF;
}

QPushButton#sideCircleButton:hover {
    background-color: #3F3F3F;
    border: 3px solid #1A86D9;
}

QPushButton#sideCircleButton:pressed {
    background-color: #505050;
}

QPushButton#circleControlButton {
    background-color: #0078D4;
    color: white;
    border-radius: 35px;
    font-size: 24pt;
    border: none;
}

QPushButton#circleControlButton:hover {
    background-color: #1A86D9;
}

QPushButton#circleControlButton:pressed {
    background-color: #005A9E;
}

QPushButton#circleControlButton:disabled {
    background-color: #3F3F3F;
    color: #797775;
}

QPushButton#circleControlButtonStop {
    background-color: #E81123;
    color: white;
    border-radius: 35px;
    font-size: 24pt;
    border: none;
}

QPushButton#circleControlButtonStop:hover {
    background-color: #F1707A;
}

QPushButton#circleControlButtonStop:pressed {
    background-color: #C50F1F;
}

QPushButton#circleControlButtonStop:disabled {
    background-color: #3F3F3F;
    color: #797775;
}
"""


def get_theme_stylesheet(theme_name):
    """Get stylesheet for the specified theme"""
    return DARK_THEME if theme_name == "dark" else LIGHT_THEME
