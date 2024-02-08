from PyQt5 import QtCore, QtGui, QtWidgets
from ui import Ui_MainWindow
from PIL import Image, ImageFilter, ImageEnhance
import os

class ImageEditor(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.workdir = ""
        self.ui.btn_bw.clicked.connect(self.do_bw)
        self.ui.btn_left.clicked.connect(self.do_left)
        self.ui.btn_right.clicked.connect(self.do_right)
        self.ui.btn_mirror.clicked.connect(self.do_mirror)
        self.ui.btn_sharp.clicked.connect(self.do_sharp)
        self.ui.btn_flip.clicked.connect(self.do_flip)
        self.ui.btn_blur.clicked.connect(self.do_blur)
        self.ui.btn_crop.clicked.connect(self.do_crop)
        self.ui.btn_dir.clicked.connect(self.showfiles)
        self.ui.listWidget.itemClicked.connect(self.showimage)

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
            win.setText("боже...")
            win.exec()

    def loadImage(self, name):
        self.filename = name
        self.path = os.path.join(self.workdir, self.filename)
        self.image = Image.open(self.path)

    def showimage(self):
        if self.ui.listWidget.selectedItems():
            name = self.ui.listWidget.selectedItems()[0].text()
            self.loadImage(name)
            pix = QtGui.QPixmap(self.path)
            w, h = self.ui.image.width(), self.ui.image.height()
            pix = pix.scaled(w, h, QtCore.Qt.KeepAspectRatio)
            self.ui.image.setPixmap(pix)

    def show_changed(self):
        self.loadImage("changed.jpg")
        pix = QtGui.QPixmap(self.path)
        w, h = self.ui.image.width(), self.ui.image.height()
        pix = pix.scaled(w, h, QtCore.Qt.KeepAspectRatio)
        self.ui.image.setPixmap(pix)

    def do_bw(self):
        self.image = self.image.convert("L")
        self.saveimage()
        self.show_changed()

    def do_blur(self):
        self.image = self.image.filter(ImageFilter.BLUR)
        self.saveimage()
        self.show_changed()

    def do_left(self):
        self.image = self.image.transpose(Image.ROTATE_90)
        self.saveimage()
        self.show_changed()

    def do_right(self):
        self.image = self.image.transpose(Image.ROTATE_270)
        self.saveimage()
        self.show_changed()

    def do_flip(self):
        self.image = self.image.transpose(Image.ROTATE_180)
        self.saveimage()
        self.show_changed()


    def do_mirror(self):
        self.image = self.image.transpose(Image.FLIP_LEFT_RIGHT)
        self.saveimage()
        self.show_changed()

    def do_sharp(self):
        self.image = ImageEnhance.Contrast(self.image)
        self.image = self.image.enhance(1.5)
        self.saveimage()
        self.show_changed()

    def do_crop(self):
        box = (100, 100, 400, 450)
        self.image = self.image.crop(box)
        self.saveimage()
        self.show_changed()


    def saveimage(self):
        path = os.path.join(self.workdir, "changed.jpg")
        self.image.save(path)



    

app = QtWidgets.QApplication([])
win = ImageEditor()
win.show()
app.exec()
