import sys
from PyQt5.QtWidgets import (QPushButton, QDialog, QTreeWidget,
                             QTreeWidgetItem, QVBoxLayout,
                             QHBoxLayout, QFrame, QLabel,
                             QApplication, QStyleFactory,
                             QMainWindow, QAction, QToolBar,
                             QWidget, QStackedWidget, QRadioButton,
                             QLineEdit, QLayout, QToolButton, QScrollArea,
                             QSizePolicy, QDockWidget, QComboBox,)
from PyQt5.QtGui import (QIcon, QColor, )
from PyQt5.QtCore import (pyqtSlot, Qt, QParallelAnimationGroup,
                          QPropertyAnimation, QAbstractAnimation, )


class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        # self.setWindowTitle(self.title)
        self.left = 100
        self.top = 100
        self.width = 1500
        self.height = 1200
        self.initUI()

    def initUI(self):
        """ main program control menu is initiated here
        """
        self.setGeometry(self.left, self.top, self.width, self.height)
        # self.setWindowTitle("UI Testing")  # custom naming of current window
        self.init_mainMenu()

        self.main_widget = QWidget(self)
        self.form_widget = CollapsibleDialog()
        # self.form_widget2 = stackedExample(self)  # This is my UI widget

        self.main_layout = QVBoxLayout(self.main_widget)
        self.main_layout.sizeConstraint = QLayout.SetDefaultConstraint
        self.main_layout.addWidget(self.form_widget)  # form_widget has its own main_widget where
                                                                  # I put all other widgets onto
        # self.main_layout.addWidget(self.form_widget2)
        self.main_widget.setLayout(self.main_layout)
        self.setCentralWidget(self.main_widget)

        self.show()

    def init_mainMenu(self):
        mainMenu = self.menuBar()
        self.fileMenu = mainMenu.addMenu('File')
        self.editMenu = mainMenu.addMenu('Edit')
        self.viewMenu = mainMenu.addMenu('View')
        self.searchMenu = mainMenu.addMenu('Search')
        self.toolsMenu = mainMenu.addMenu('Tools')
        self.helpMenu = mainMenu.addMenu('Help')

        # add_to: fileMenu
        exitButton = QAction(QIcon('exit24.png'), 'Exit', self)
        exitButton.setShortcut('Ctrl+Q')
        exitButton.setStatusTip('Exit application')
        exitButton.triggered.connect(self.close)
        self.fileMenu.addAction(exitButton)

        # add_to: editMenu
        exitButton = QAction(QIcon('exit24.png'), 'Action', self)
        exitButton.setStatusTip('Exit application')
        # exitButton.triggered.connect(self.close)
        self.editMenu.addAction(exitButton)

        # add_to: viewMenu
        exitButton = QAction(QIcon('exit24.png'), 'Action', self)
        exitButton.setStatusTip('Exit application')
        # exitButton.triggered.connect(self.close)
        self.viewMenu.addAction(exitButton)

        # add_to: searchMenu
        exitButton = QAction(QIcon('exit24.png'), 'Action', self)
        exitButton.setStatusTip('Exit application')
        # exitButton.triggered.connect(self.close)
        self.searchMenu.addAction(exitButton)

        # add_to: toolsMenu
        self.toolButton = QAction(QIcon('exit24.png'), 'Display File Panel', self)
        self.toolButton.setStatusTip('Open Tool Dock')
        self.toolButton.triggered.connect(self.show)
        self.toolsMenu.addAction(self.toolButton)

        # add_to: helpMenu
        exitButton = QAction(QIcon('exit24.png'), 'Action', self)
        exitButton.setStatusTip('Exit application')
        # exitButton.triggered.connect(self.close)
        self.helpMenu.addAction(exitButton)

    def init_toolBar(self):
        toolbar = self.tool
        browser = stackedPages()
        toolbar.addWidget(browser)

""" 
EDIT THE WIDGET HERE
"""
class Page1(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent=parent)
        lay = QVBoxLayout(self)
        for i in range(4):
            lay.addWidget(QPushButton("{}".format(i)))


class Page2(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent=parent)
        lay = QVBoxLayout(self)
        for i in range(4):
            lay.addWidget(QLineEdit("{}".format(i)))


class Page3(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent=parent)
        lay = QVBoxLayout(self)
        for i in range(4):
            lay.addWidget(QRadioButton("{}".format(i)))


class stackedPages(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent=parent)
        lay = QVBoxLayout(self)
        self.Stack = QStackedWidget()
        self.Stack.addWidget(Page1())
        self.Stack.addWidget(Page2())
        self.Stack.addWidget(Page3())


        ''' Page turner button '''
        btnNext = QPushButton("Next")
        btnNext.clicked.connect(self.onNext)
        btnPrevious = QPushButton("Previous")
        btnPrevious.clicked.connect(self.onPrevious)
        btnLayout = QHBoxLayout()
        btnLayout.addWidget(btnPrevious)
        btnLayout.addWidget(btnNext)

        lay.addWidget(self.Stack)
        lay.addLayout(btnLayout)

    def onNext(self):
        self.Stack.setCurrentIndex((self.Stack.currentIndex()+1) % 3)

    def onPrevious(self):
        self.Stack.setCurrentIndex((self.Stack.currentIndex()-1) % 3)


class SectionExpandButton(QPushButton):
    """a QPushbutton that can expand or collapse its section
    """

    def __init__(self, item, text="", parent=None):
        super().__init__(text, parent)
        self.section = item
        self.clicked.connect(self.on_clicked)

    def on_clicked(self):
        """toggle expand/collapse of section by clicking
        """
        if self.section.isExpanded():
            self.section.setExpanded(False)
        else:
            self.section.setExpanded(True)


class CollapsibleDialog(QDialog):
    """a dialog to which collapsible sections can be added;
    subclass and reimplement define_sections() to define sections and
        add them as (title, widget) tuples to self.sections
    """
    def __init__(self):
        super().__init__()
        self.tree = QTreeWidget()
        self.tree.setHeaderHidden(True)
        layout = QVBoxLayout()
        layout.addWidget(self.tree)
        self.setLayout(layout)
        self.tree.setIndentation(0)

        self.sections = []
        self.define_sections()
        self.add_sections()

    def add_sections(self):
        """adds a collapsible sections for every
        (title, widget) tuple in self.sections
        """
        for (title, widget) in self.sections:
            button1 = self.add_button(title)
            section1 = self.add_widget(button1, widget)
            button1.addChild(section1)

    def define_sections(self):
        """reimplement this to define all your sections
        and add them as (title, widget) tuples to self.sections
        """
        widget = QFrame(self.tree)
        layout = QHBoxLayout(widget)
        layout.addWidget(QLabel("Bla"))
        layout.addWidget(QLabel("Blubb"))
        title = "Section 1"
        self.sections.append((title, widget))

        widget2 = stackedPages()
        title2 = "Section 2"
        self.sections.append((title2, widget2))

    def add_button(self, title):
        """creates a QTreeWidgetItem containing a button
        to expand or collapse its section
        """
        item = QTreeWidgetItem()
        self.tree.addTopLevelItem(item)
        self.tree.setItemWidget(item, 0, SectionExpandButton(item, text=title))
        return item

    def add_widget(self, button, widget):
        """creates a QWidgetItem containing the widget,
        as child of the button-QWidgetItem
        """
        section = QTreeWidgetItem(button)
        section.setDisabled(True)
        self.tree.setItemWidget(section, 0, widget)
        return section


class CollapsibleBox(QWidget):
    def __init__(self, title="", parent=None):
        super(CollapsibleBox, self).__init__(parent)

        self.toggle_button = QToolButton(text=title, checkable=True, checked=False)
        self.toggle_button.setStyleSheet("QToolButton { border: none; }")
        self.toggle_button.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.toggle_button.setArrowType(Qt.RightArrow)
        self.toggle_button.pressed.connect(self.on_pressed)


        self.toggle_animation = QParallelAnimationGroup(self)

        self.content_area = QScrollArea(maximumHeight=0, minimumHeight=0)
        self.content_area.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.content_area.setFrameShape(QFrame.NoFrame)

        lay = QVBoxLayout(self)
        lay.setSpacing(0)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.addWidget(self.toggle_button)
        lay.addWidget(self.content_area)

        self.toggle_animation.addAnimation(QPropertyAnimation(self, b"minimumHeight"))
        self.toggle_animation.addAnimation(QPropertyAnimation(self, b"maximumHeight"))
        self.toggle_animation.addAnimation(QPropertyAnimation(self.content_area, b"maximumHeight"))


    @pyqtSlot()
    def on_pressed(self):
        checked = self.toggle_button.isChecked()
        self.toggle_button.setArrowType(Qt.DownArrow if not checked else Qt.RightArrow)
        self.toggle_animation.setDirection(
            QAbstractAnimation.Forward if not checked
            else QAbstractAnimation.Backward
        )
        self.toggle_animation.start()

    def setContentLayout(self, layout):
        lay = self.content_area.layout()
        del lay
        self.content_area.setLayout(layout)
        collapsed_height = (self.sizeHint().height() - self.content_area.maximumHeight())
        content_height = layout.sizeHint().height()
        for i in range(self.toggle_animation.animationCount()):
            animation = self.toggle_animation.animationAt(i)
            animation.setDuration(500)
            animation.setStartValue(collapsed_height)
            animation.setEndValue(collapsed_height + content_height)

        content_animation = self.toggle_animation.animationAt(self.toggle_animation.animationCount() - 1)
        content_animation.setDuration(500)
        content_animation.setStartValue(0)
        content_animation.setEndValue(content_height)


if __name__ == "__main__":
    import random

    # Starting Application
    app = QApplication(sys.argv)
    app.setApplicationName("ML-ALD Data Interface")
    app.setStyle(QStyleFactory.create('Fusion'))

    ''' Initiate Main Window '''
    window = MainWindow()

    # Attaching Central Widget
    browser = stackedPages()
    window.setCentralWidget(browser)  # blank widget for now

    # Setting up Dock & Attaching widget
    dock = QDockWidget("DOI Browser Menu")
    dock.setFeatures(QDockWidget.DockWidgetMovable)  # disable closing the dock or floatable
    scroll = QScrollArea()
    scroll.setStyleSheet("background-color: white;")
    content = QWidget()
    window.addDockWidget(Qt.LeftDockWidgetArea, dock)
    dock.setWidget(scroll)
    scroll.setWidget(content)
    scroll.setWidgetResizable(True)
    vlay = QVBoxLayout(content)

    # dirty fix for adding in the menuBar, a button to reopen dock
    window.toolButton.triggered.connect(dock.show)

    # Adding content to widget to dock layout
    # 1. Username Widget
    section1 = CollapsibleBox('Username')
    vlay.addWidget(section1)
    lay1 = QVBoxLayout()
    item1_1 = QLabel("User ID")
    item1_1.setStyleSheet("color : black;")
    item1_1.setAlignment(Qt.AlignCenter)
    item1_2 = QComboBox()
    item1_2.addItems(['a','b','c','d'])
    lay1.addWidget(item1_1)
    lay1.addWidget(item1_2)
    # 2. Project Widget
    section2 = CollapsibleBox('Project')
    vlay.addWidget(section2)
    lay2 = QVBoxLayout()
    item2_1 = QLabel("Project Name")
    item2_1.setStyleSheet("color : black;")
    item2_1.setAlignment(Qt.AlignCenter)
    item2_2 = QComboBox()
    item2_2.addItems(['A','B','C','D'])
    lay2.addWidget(item2_1)
    lay2.addWidget(item2_2)
    # 3. DOI Widget
    section3 = CollapsibleBox('DOI')
    vlay.addWidget(section3)
    lay3 = QVBoxLayout()
    item3_1 = QLabel("DOI number")
    item3_1.setStyleSheet("color : black;")
    item3_1.setAlignment(Qt.AlignCenter)
    item3_2 = QComboBox()
    item3_2.addItems(['a','b','c','d'])
    lay3.addWidget(item3_1)
    lay3.addWidget(item3_2)


    section1.setContentLayout(lay1)
    section2.setContentLayout(lay2)
    section3.setContentLayout(lay3)

    vlay.addStretch()

    window.show()
    sys.exit(app.exec_())
