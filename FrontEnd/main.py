import sys
from PyQt5.QtWidgets import (QApplication, QStyleFactory)
from ActivityClass.ALD import ConfigGallery

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle(QStyleFactory.create('Fusion'))
    ex = ConfigGallery()
    ex.show()
    sys.exit(app.exec_())
