import json
import datafed.CommandLib as datafed
from PyQt5.QtWidgets import (QPushButton, QDialog, QTreeWidget,
                             QTreeWidgetItem, QVBoxLayout,
                             QHBoxLayout, QFrame, QLabel,
                             QApplication, QStyleFactory,
                             QMainWindow, QAction, QToolBar,
                             QWidget, QStackedWidget, QRadioButton,
                             QLineEdit, QLayout, QToolButton,
                             QScrollArea, QSizePolicy, QDockWidget,
                             QComboBox, QSplitter, QGroupBox,
                             QFormLayout, QSpinBox, QButtonGroup,
                             QMessageBox, QGridLayout, QTabWidget,
                             QMenu, QCheckBox, )
from PyQt5.QtGui import (QIcon, QColor, QDrag, QPixmap, QPainter, QCursor, )
from PyQt5.QtCore import (pyqtSlot, Qt, QParallelAnimationGroup, QMimeData,
                          QPropertyAnimation, QAbstractAnimation, )


#----> Level 3
class PageWidget_Analysis(QWidget):
    """
    This constructor creates the layout for Stacked Pages.
    """
    def __init__(self):
        super(PageWidget_Analysis, self).__init__()
        self.main_layout = QVBoxLayout(self)

        # Widget 1: Stacked Pages
        self.stackpages = QStackedWidget()
        # self.stackpages.setStyleSheet("background-color: white;")
        page1 = PageWidget_Analysis.StackWidget_ActView(self)
        page2 = PageWidget_Analysis.StackWidget_ActMod(self)   # this is a blank widget that will take on a QWidget
                            # object called by clicking on an activity node
        self.stackpages.addWidget(page1)
        self.stackpages.addWidget(page2)

        self.main_layout.addWidget(self.stackpages)
        self.setLayout(self.main_layout)


#------> Level 4
    class StackWidget_ActView(QWidget):
        def __init__(self, outer):
            super(PageWidget_Analysis.StackWidget_ActView, self).__init__()

            self.layout = QHBoxLayout()
            self.outer = outer

            test_button = QPushButton("test button")
            test_button.clicked.connect(self.testpage)

            self.layout.addWidget(test_button)
            self.setLayout(self.layout)

        def testpage(self):
            # Accessing outer class from inner class
            # read more here: https://stackoverflow.com/questions/2024566/access-outer-class-from-inner-class-in-python
            self.outer.stackpages.setCurrentIndex(1)


    #------> Level 4
    class StackWidget_ActMod(QWidget):
        def __init__(self, outer):
            super(PageWidget_Analysis.StackWidget_ActMod, self).__init__()

            self.outer = outer


            #TODO: Creating the object to take care of the node that was clicked
            # (1) Clicking a node = list samples. Later: grouped by identical setting/experiment run
            # (2) Clicking the specific sample = switch page & signal to generate service object
            # (3) Service object generated & register on the page
            # (3.1) Service object sends data back to datafed
            # (3.2) Service object closes & object destroy object.__del__(self)
            # (3.3) Service object under __del__ returns page to browser


            # DataFed: 1 collection = 1 experiment, each collection contains a number of samples in that experiment.
            # each data file contains metadata and associated raw data from N number of instruments
            # Users should be able to:
            # (1) create & delete data
            # (2) create & delete collection
            # (3) link data to collection
            # (4) modify data
            #

            self.main_layout = QVBoxLayout()
            return_button = QPushButton("return")
            return_button.clicked.connect(self.returnpage)




            self.main_layout.addWidget(return_button)
            self.setLayout(self.main_layout)

        def returnpage(self):
            self.outer.stackpages.setCurrentIndex(0)
