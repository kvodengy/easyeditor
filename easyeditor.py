from PyQt5 import QtCore, QtGui, QtWidgets
from ui import Ui_MainWindow
import os

class ImageEditor(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.workdir = ""
        self.ui.btn_dir.clicked.connect(self.showfiles)

    def choose_dir(self):
        self.workdir = QtWidgets.QFileDialog.getExistingDirectory()

    def filter(self, files, extentions):
        result = []
        for file in files:
            for ex in extentions:
                if file.endswith(ex):
                    result.append(file)
        return result

    def showfiles(self):
        extensions = [".jpg", ".png", ".jpeg", "gif", ".bmp"]
        self.choose_dir()
        try:
            files = os.listdir(self.workdir)
            files = self.filter(files, extensions)
            self.ui.listWidget.clear()
            for file in files:
                self.ui.listWidget.addItem(file)
        except:
            win = QtWidgets.QMessageBox()
            win.setText("Шлях до файлів обрано не вірно!")
            win.exec()
        


    

app = QtWidgets.QApplication([])
win = ImageEditor()
win.show()
app.exec()