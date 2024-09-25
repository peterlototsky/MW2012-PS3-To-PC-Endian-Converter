from PyQt5.QtCore import pyqtSignal, QObject


class guiSignals(QObject):

    increment_progress_bar = pyqtSignal(int)
    update_row_color = pyqtSignal(int, str)
    output_to_console = pyqtSignal(str)
