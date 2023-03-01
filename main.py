import version
import sys
from PyQt5 import QtCore, QtGui, QtWidgets, uic, QtSvg
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
import cv2


class MainWindow(QtWidgets.QMainWindow):
        
    def __init__(self):
        super(MainWindow, self).__init__()
        uic.loadUi('gui.ui', self)

        self.show()
        self.setWindowTitle(version.__name__ + " (" + version.__version__ + ")")


    def resize_images(self, urls):
        max_dimension = self.spin_size.value()
        self.progress.setMaximum(len(urls)-1)
        self.progress.setValue(0)

        for i in range(len(urls)):
            #print(urls[i])

            image = cv2.imread(urls[i], cv2.IMREAD_COLOR)
            h,w,d = image.shape
            #min_dimension = 50
            ratio = 1
            if h > w:
                ratio = max_dimension / h
            else:
                ratio = max_dimension / w
            image = cv2.resize(image, None, fx=ratio, fy=ratio, interpolation=cv2.INTER_AREA)
            cv2.imwrite(urls[i], image)
            
            
            self.progress.setValue(i)
            QApplication.processEvents()
            #self.label_file.setText(urls[i].split(os.sep)[-1]) # does not work?
            self.label_file.setText(urls[i].split("/")[-1])

        self.progress.setValue(0)
        self.label_file.setText("")


    def dragEnterEvent(self, e):
        if e.mimeData().hasUrls():
            print("has urls")
            e.accept()
        else:
            e.ignore()            


    def dropEvent(self, event):
        if event.mimeData().hasUrls():
            event.setDropAction(QtCore.Qt.CopyAction)
            event.accept()

            urls = []
            for url in event.mimeData().urls():
                urls.append(str(url.toLocalFile()))
            
            self.resize_images(urls)
        else:
            event.ignore() 


def main():
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle('Fusion')
    myWindow = MainWindow()
    sys.exit(app.exec_())
    

if __name__ == '__main__':
    if sys.platform == 'win32':
        QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
    main()
