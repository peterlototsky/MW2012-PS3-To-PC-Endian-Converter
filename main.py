import sys
import os

from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog
from PyQt5.QtGui import QColor, QBrush
from UI.MainWindow import Ui_MainWindow

import Tools.fileManager as fileManager
from UI.signals import guiSignals
from Tools.conversionRunner import conversionRunner


class MainWindow(QMainWindow):
   
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.gui_signals = guiSignals()
        self.conversionRunner = conversionRunner(self.gui_signals)
        self.setSignals()

        self.files = []


    def openFolder(self, param1):
        folder = QFileDialog.getExistingDirectory(self, "Select Folder")
        if folder:
            print(f"Selected folder: {folder}")
            self.listDatFiles(folder)


    def listDatFiles(self, folder_path):
        self.ui.listWidget.clear()
        self.files = []

        self.files = fileManager.openFolder(folder_path)
        
        for file_name in self.files:
            self.ui.listWidget.addItem(os.path.basename(file_name))


    def startConversion(self, param1):
        self.ui.progressBar.setMaximum(len(self.files))
        if self.files:
            self.conversionRunner.startConversion(self.files)
        else:
            self.ui.textEdit.append("No Files to Convert\n")


    def setSignals(self):
        self.gui_signals.increment_progress_bar.connect(self.incrementProgressBar)
        self.gui_signals.update_row_color.connect(self.colorRow)
        self.gui_signals.output_to_console.connect(self.outputText)

        self.ui.actionOpen.triggered.connect(self.openFolder)
        self.ui.actionConvert.triggered.connect(self.startConversion)


    def colorRow(self, index : int, color : str):
        item = self.ui.listWidget.item(index)
        item.setBackground(QBrush(QColor(color)))


    def outputText(self, message : str):
        self.ui.textEdit.append(message)


    def incrementProgressBar(self, progress : int):
        self.ui.progressBar.setValue(progress)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
