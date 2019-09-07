import sys
from PyQt5.QtWidgets import (QApplication, QStyleFactory, QMainWindow, QAction)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot
from ActivityClass.ALD import ConfigGallery


class GUI(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # self.setWindowTitle(self.title)
        # self.setGeometry(self.left, self.top, self.width, self.height)

        mainMenu = self.menuBar()
        fileMenu = mainMenu.addMenu('File')
        editMenu = mainMenu.addMenu('Edit')
        viewMenu = mainMenu.addMenu('View')
        searchMenu = mainMenu.addMenu('Search')
        toolsMenu = mainMenu.addMenu('Tools')
        helpMenu = mainMenu.addMenu('Help')

        exitButton = QAction(QIcon('exit24.png'), 'Exit', self)
        exitButton.setShortcut('Ctrl+Q')
        exitButton.setStatusTip('Exit application')
        exitButton.triggered.connect(self.close)
        fileMenu.addAction(exitButton)

        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setApplicationName("ML-ALD Data Interface -- Lehigh University")
    app.setStyle(QStyleFactory.create('Fusion'))
    ex1 = GUI()
    ex2 = ConfigGallery()
    sys.exit(app.exec_())


