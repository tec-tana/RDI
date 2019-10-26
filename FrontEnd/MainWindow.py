# import standard libraries
import sys
from PyQt5.QtGui import (QIcon,)
from PyQt5.QtWidgets import (QPushButton, QVBoxLayout, QHBoxLayout, QLabel, QApplication, QStyleFactory, QMainWindow, QAction,
                             QWidget, QStackedWidget, QComboBox, QGroupBox, QFormLayout, QButtonGroup,)
# import local constructs
from ProjectClass.rcpmngr import PageWidget_RcpMngr
from ProjectClass.analysis import PageWidget_Analysis
from ProjectClass.ml import PageWidget_ML
from config import cfg


"""---- class definition ----"""

# main window construct
class MainWindow(QMainWindow):
    """
    This constructor will create the main window under the application.
    This is where the UI container and the Menubar is configured.
    """
    def __init__(self):
        super(MainWindow, self).__init__()
        # self.title = "UI Testing"
        self.left = 100
        self.top = 100
        self.width = 1500
        self.height = 1200
        self.initUI()

    def initUI(self):
        self.setGeometry(self.left, self.top, self.width, self.height)
        # self.setWindowTitle(self.title)  # custom naming of current window
        self.init_menuBar()
        self.show()

    def init_menuBar(self):
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
        exitButton.setStatusTip('')
        self.editMenu.addAction(exitButton)

        # add_to: viewMenu
        exitButton = QAction(QIcon('exit24.png'), 'Action', self)
        exitButton.setStatusTip('')
        self.viewMenu.addAction(exitButton)

        # add_to: searchMenu
        exitButton = QAction(QIcon('exit24.png'), 'Action', self)
        exitButton.setStatusTip('')
        self.searchMenu.addAction(exitButton)

        # add_to: toolsMenu
        self.toolButton = QAction(QIcon('exit24.png'), 'Action', self)
        self.toolButton.setStatusTip('')
        self.toolsMenu.addAction(self.toolButton)

        # add_to: helpMenu
        exitButton = QAction(QIcon('exit24.png'), 'Action', self)
        exitButton.setStatusTip('')
        self.helpMenu.addAction(exitButton)


# central widget to host all page widgets
class CentralWidget(QWidget):
    """
    This constructor creates the central layout splitting Side Bar & Stacked Pages.
    """
    def __init__(self):
        super(CentralWidget, self).__init__()

        self.main_layout = QHBoxLayout(self)
        # self.main_layout.sizeConstraint = QLayout.SetDefaultConstraint
        ''' The main widget's minimum size is set to minimumSize(), 
            unless the widget already has a minimum size.
            https://doc.qt.io/qt-5/qlayout.html
        '''
        # self.splitter = QSplitter(Qt.Horizontal)  # if want to set as adjustable UI
        # self.splitter.setChildrenCollapsible(False)

        # Widget 1: Side Bar
        self.sidebarwidget = CentralWidget.SidebarWidget()

        # Widget 2: Stacked Pages
        self.stackpages = QStackedWidget()
        self.stackpages.setStyleSheet("background-color: white;")
        page1 = PageWidget_RcpMngr()
        page2 = PageWidget_Analysis()
        page3 = PageWidget_ML()
        self.stackpages.addWidget(page1)
        self.stackpages.addWidget(page2)
        self.stackpages.addWidget(page3)

        cfg.mainpagestack = self.stackpages

        # self.splitter.addWidget(self.sidebarwidget)
        # self.splitter.addWidget(self.stackpages)
        # self.splitter.setMinimumWidth(50)
        # self.splitter.setSizes([100, 1000])
        self.main_layout.addWidget(self.sidebarwidget)
        self.main_layout.addWidget(self.stackpages)
        # self.main_layout.addWidget(self.splitter)
        self.setLayout(self.main_layout)


    #----> Level 3
    class SidebarWidget(QWidget):
        """
        This constructor creates the layout for Side Bar.
        """
        def __init__(self):
            super(CentralWidget.SidebarWidget, self).__init__()

            self.main_layout = QVBoxLayout(self)

            # Widget 1: File Browser
            self.filebrowser = QGroupBox("File Browser")
            filebrowserwidget = CentralWidget.FileBrowserWidget()
            layout = QVBoxLayout()
            layout.addWidget(filebrowserwidget)
            self.filebrowser.setLayout(layout)

            # Widget 2: Page Toggle
            self.pagetoggle = QGroupBox("Page Toggle")
            pagetogglerwidget = CentralWidget.PageTogglerWidget()
            layout_toggle = QVBoxLayout()
            layout_toggle.addWidget(pagetogglerwidget)
            self.pagetoggle.setLayout(layout_toggle)

            self.main_layout.addWidget(self.filebrowser)
            self.main_layout.addWidget(self.pagetoggle)
            self.main_layout.addStretch(1)
            self.setLayout(self.main_layout)


    #------> Level 4
    class FileBrowserWidget(QWidget):
        """
        This constructor creates the layout for Side Bar>>File Browser.
        """
        def __init__(self):
            super(CentralWidget.FileBrowserWidget, self).__init__()

            self.main_layout = QFormLayout(self)

            # Creating widgets + connect actions
            self.user = QLabel()
            self.project = QComboBox()
            self.doi = QComboBox()
            self.project.activated.connect(self.updateBrowser)
            self.doi.activated.connect(self.updateDOI)

            # Widget 1: File Browser
            self.main_layout.addRow(QLabel("User:"), self.user)  # pull the data from log-in info
            self.main_layout.addRow(QLabel("Project:"), self.project)  # pull the data from log-in info
            self.main_layout.addRow(QLabel("DOI:"), self.doi)  # pull the data from log-in info

            self.setLayout(self.main_layout)

            self.updateBrowser()

        def updateBrowser(self, coll:str=''):
            import datafed.CommandLib as datafed
            from google.protobuf.json_format import MessageToDict
            self.user.setText(cfg.user._userinfo['name'])
            self.project.addItems([w['title'] for w in cfg.user._userinfo['ownership']['item'][:]])

            #TODO: Figure out how to extract files in each collection. coll view does not give info.
            #if self.project.currentText():
            #   coll = str(self.project.currentText())
            #   self.doi.addItems([w[] for w in MessageToDict(datafed.command('coll view'+coll)[0])])

        def updateDOI(self):
            cfg.currentDOI = self.doi.currentText()

    #------> Level 4
    class PageTogglerWidget(QWidget):
        """
        This constructor creates the layout for Side Bar>>PageToggler.
        """
        def __init__(self):
            super(CentralWidget.PageTogglerWidget, self).__init__()

            layout_toggle = QVBoxLayout()

            # Widget 1: Page Toggle
            self.button_RcpMngr = QPushButton('Recipe Manager', self)
            self.button_RcpMngr.setFixedSize(350, 100)
            self.button_Analysis = QPushButton('Data Viewer', self)
            self.button_Analysis.setFixedSize(350, 100)
            self.button_ML = QPushButton('ML Study', self)
            self.button_ML.setFixedSize(350, 100)

            # Group button to manage states
            self.btn_grp = QButtonGroup()
            self.btn_grp.setExclusive(True)
            self.btn_grp.addButton(self.button_RcpMngr)
            self.btn_grp.addButton(self.button_Analysis)
            self.btn_grp.addButton(self.button_ML)
            self.btn_grp.buttonClicked.connect(self.toggle)

            # Adding buttons to layout
            layout_toggle.addWidget(self.button_RcpMngr)
            layout_toggle.addWidget(self.button_Analysis)
            layout_toggle.addWidget(self.button_ML)
            layout_toggle.addStretch(1)
            self.setLayout(layout_toggle)

        def toggle(self, btn):
            # Insert a clause here if the user has not logged-in
            buttonList = {"Recipe Manager":0, "Data Viewer":1, "ML Study":2}
            buttonNum = buttonList.get(btn.text())  # Return assigned number
            self.clear_color()
            btn.setStyleSheet("background-color: Green;")

            # Right now, I'm assigning stackpages in the outer class to cfg
            #   but nested classes are not often practiced cuz they do not imply
            #   any particular relationship between inner and outer class.
            cfg.mainpagestack.setCurrentIndex(buttonNum)
            pass

        def clear_color(self):
            self.button_RcpMngr.setStyleSheet("background-color: white;")
            self.button_Analysis.setStyleSheet("background-color: white;")
            self.button_ML.setStyleSheet("background-color: white;")


class mainUI(QApplication):
    def __init__(self):
        import sys
        super(mainUI, self).__init__(sys.argv)
        self.setApplicationName("ML-ALD Data Interface")
        self.setStyle(QStyleFactory.create('Fusion'))
        # Initiate Main Window
        window = MainWindow()
        # Attach CentralWidget
        main_widget = CentralWidget()
        window.setCentralWidget(main_widget)
        # Show window
        window.show()
        self.exec_()



"""---- main program ----"""

if __name__ == "__main__":
    # Start Application
    app = QApplication(sys.argv)
    app.setApplicationName("ML-ALD Data Interface")
    app.setStyle(QStyleFactory.create('Fusion'))
    # Initiate Main Window
    window = MainWindow()
    # Attach CentralWidget
    main_widget = CentralWidget()
    window.setCentralWidget(main_widget)
    # Show window
    window.show()
    sys.exit(app.exec_())
