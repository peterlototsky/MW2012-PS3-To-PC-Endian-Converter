import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog
from MainWindow import Ui_MainWindow

import fileManager
import conversionRunner

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.actionOpen.triggered.connect(self.openFolder)
        self.ui.actionConvert.triggered.connect(self.start_conversion)

        self.files = []

    def openFolder(self, param1):
        folder = QFileDialog.getExistingDirectory(self, "Select Folder")
        if folder:
            print(f"Selected folder: {folder}")
            self.list_dat_files(folder)

    def list_dat_files(self, folder_path):
        # Clear the existing items in the QListWidget
        self.ui.listWidget.clear()
        self.files = []

        self.files = fileManager.openFolder(folder_path)
        
        # Add each .dat file to the QListWidget
        for file_name in self.files:
            self.ui.listWidget.addItem(os.path.basename(file_name))


    def start_conversion(self, param1):
        self.ui.progressBar.setMaximum(len(self.files))
        files_coverted = 0
        if self.files:
            for file in self.files:
                output = conversionRunner.convert(file)
                if output[0]:
                    self.ui.textEdit.append(f'{output[1]}\n')
                else:
                    self.ui.textEdit.append(f'Wrote File {output[1]}\n')
                files_coverted = files_coverted + 1
                self.ui.progressBar.setValue(files_coverted)
        else:
            self.ui.textEdit.append("No Files to Convert\n")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
