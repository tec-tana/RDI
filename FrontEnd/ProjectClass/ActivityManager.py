import sys
from PyQt5 import QtWidgets, QtCore


class Window(QtWidgets.QMainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)

        self.stacked_widget = QtWidgets.QStackedWidget()
        self.button = QtWidgets.QPushButton("Next")

        self.button.clicked.connect(self.__next_page)

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.stacked_widget)
        layout.addWidget(self.button)

        widget = QtWidgets.QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        self.stacked_widget.addWidget(QtWidgets.QLabel("Page 1"))
        self.stacked_widget.addWidget(QtWidgets.QLabel("Page 2"))
        self.stacked_widget.addWidget(QtWidgets.QLabel("Page 3"))

    def __next_page(self):
        idx = self.stacked_widget.currentIndex()
        if idx < self.stacked_widget.count() - 1:
            self.stacked_widget.setCurrentIndex(idx + 1)
        else:
            self.stacked_widget.setCurrentIndex(0)

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    w = Window()
    w.show()
    sys.exit(app.exec_())