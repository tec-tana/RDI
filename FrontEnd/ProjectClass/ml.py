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
class PageWidget_ML(QWidget):
    """
    This constructor creates the layout for Stacked Pages.
    """
    def __init__(self):
        super(PageWidget_ML, self).__init__()
