import sys
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


# Level 1
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


#--> Level 2
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
        self.sidebarwidget = SidebarWidget()

        # Widget 2: Stacked Pages
        self.stackpages = QStackedWidget()
        self.stackpages.setStyleSheet("background-color: white;")
        page1 = PageWidget_Login()
        page2 = PageWidget_RcpMngr()
        page3 = PageWidget_Analysis()
        page4 = PageWidget_ML()
        self.stackpages.addWidget(page1)
        self.stackpages.addWidget(page2)
        self.stackpages.addWidget(page3)
        self.stackpages.addWidget(page4)

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
        super(SidebarWidget, self).__init__()

        self.main_layout = QVBoxLayout(self)

        # Widget 1: File Browser
        self.filebrowser = QGroupBox("File Browser")
        filebrowserwidget = FileBrowserWidget()
        layout = QVBoxLayout()
        layout.addWidget(filebrowserwidget)
        self.filebrowser.setLayout(layout)

        # Widget 2: Page Toggle
        self.pagetoggle = QGroupBox("Page Toggle")
        pagetogglerwidget = PageTogglerWidget()
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
        super(FileBrowserWidget, self).__init__()

        self.main_layout = QFormLayout(self)

        # Widget 1: File Browser
        self.main_layout.addRow(QLabel("User:"), QLabel("Username"))  # pull the data from log-in info
        self.main_layout.addRow(QLabel("Project:"), QComboBox())  # pull the data from log-in info
        self.main_layout.addRow(QLabel("DOI:"), QComboBox())  # pull the data from log-in info

        self.setLayout(self.main_layout)


#------> Level 4
class PageTogglerWidget(QWidget):
    """
    This constructor creates the layout for Side Bar>>PageToggler.
    """
    def __init__(self):
        super(PageTogglerWidget, self).__init__()

        layout_toggle = QVBoxLayout()

        # Widget 1: Page Toggle
        self.button_Login = QPushButton('Log-in', self)
        self.button_Login.setFixedSize(350, 100)
        self.button_RcpMngr = QPushButton('Recipe Manager', self)
        self.button_RcpMngr.setFixedSize(350, 100)
        self.button_Analysis = QPushButton('Data Viewer', self)
        self.button_Analysis.setFixedSize(350, 100)
        self.button_ML = QPushButton('ML Study', self)
        self.button_ML.setFixedSize(350, 100)

        # Group button to manage states
        self.btn_grp = QButtonGroup()
        self.btn_grp.setExclusive(True)
        self.btn_grp.addButton(self.button_Login)
        self.btn_grp.addButton(self.button_RcpMngr)
        self.btn_grp.addButton(self.button_Analysis)
        self.btn_grp.addButton(self.button_ML)
        self.btn_grp.buttonClicked.connect(self.toggle)

        # Adding buttons to layout
        layout_toggle.addWidget(self.button_Login)
        layout_toggle.addWidget(self.button_RcpMngr)
        layout_toggle.addWidget(self.button_Analysis)
        layout_toggle.addWidget(self.button_ML)
        layout_toggle.addStretch(1)
        self.setLayout(layout_toggle)

    def toggle(self, btn):
        # Insert a clause here if the user has not logged-in
        buttonList = {"Log-in":0, "Recipe Manager":1, "Data Viewer":2, "ML Study":3}
        buttonNum = buttonList.get(btn.text())  # Return assigned number
        self.clear_color()
        btn.setStyleSheet("background-color: Green;")

        # Have to fix the dependency here. This may become difficult to deal with later.
        main_widget.stackpages.setCurrentIndex(buttonNum)
        pass

    def clear_color(self):
        self.button_Login.setStyleSheet("background-color: white;")
        self.button_RcpMngr.setStyleSheet("background-color: white;")
        self.button_Analysis.setStyleSheet("background-color: white;")
        self.button_ML.setStyleSheet("background-color: white;")


#----> Level 3
class PageWidget_Login(QWidget):
    """
    This constructor creates the layout for Stacked Pages.
    """
    def __init__(self):
        super(PageWidget_Login, self).__init__()

        self.main_layout = QHBoxLayout(self)
        self.inner_layout = QVBoxLayout(self)

        # Widget 1: Login Prompt
        self.textName = QLineEdit(self)
        self.textPass = QLineEdit(self)
        self.buttonLogin = QPushButton('Login', self)
        #self.buttonLogin.clicked.connect(self.handleLogin)
        self.inner_layout.addStretch(1)  # adding top spacer
        self.inner_layout.addWidget(self.textName)
        self.inner_layout.addWidget(self.textPass)
        self.inner_layout.addWidget(self.buttonLogin)
        self.inner_layout.addStretch(1)  # adding bottom spacer

        self.main_layout.addStretch(1)  # adding left spacer
        self.main_layout.addLayout(self.inner_layout)
        self.main_layout.addStretch(1)  # adding right spacer
        self.setLayout(self.main_layout)

    def handleLogin(self):
        # TODO: Replace with with the list of username from database
        if self.textName.text() == 'foo' and self.textPass.text() == 'bar':
            # TODO: a clause to update log-in status
            self.close()
            # TODO: a clause to transfer to project page
        else:
            QMessageBox.warning(self, 'Error', 'Bad username or password')


#----> Level 3
class PageWidget_RcpMngr(QWidget):
    """
    This constructor creates the layout for PageWidget_RcpMngr.
    """
    def __init__(self):
        super(PageWidget_RcpMngr, self).__init__()
        self.main_layout = QVBoxLayout(self)

        # Widget 1: Tab widgets
        self.tab = QTabWidget()
        self.tab.setStyleSheet("background-color: none;")
        tab1 = TabWidget_ApplyTemplate()
        tab2 = TabWidget_RecipeView()
        self.tab.addTab(tab1, "Apply Template")
        self.tab.addTab(tab2, "Recipe View")

        self.main_layout.addWidget(self.tab)
        self.setLayout(self.main_layout)


#------> Level 4
class TabWidget_ApplyTemplate(QWidget):
    """
    This constructor creates the layout for PageWidget_RcpMngr >> TabWidget_ApplyTemplate.
    """
    def __init__(self):
        super(TabWidget_ApplyTemplate, self).__init__()

        self.main_layout = QGridLayout(self)

        # Widget 1: Tab widgets
        self.tab = QTabWidget()
        region1 = region_RecipeChain()
        region2 = region_Modules()
        button_apply = QPushButton("Apply")
        self.applyTemp = Template_Dialog(self)
        button_apply.clicked.connect(self.apply_template)

        self.main_layout.addWidget(region1, 0, 0, 1, 5)
        self.main_layout.addWidget(region2, 1, 0, 3, 5)
        self.main_layout.addWidget(button_apply, 4, 4, 1, 1)
        self.main_layout.setRowStretch(1, 1)
        self.main_layout.setRowMinimumHeight(0, 180)

        self.setLayout(self.main_layout)

    def apply_template(self):
        self.applyTemp.show()


#------> Level 4
class region_RecipeChain(QScrollArea):
    """
    This constructor creates the region_RecipeChain object for TabWidget_ApplyTemplate.
    """
    def __init__(self):
        super(region_RecipeChain, self).__init__()
        main_widget = QWidget()
        layout = QHBoxLayout(main_widget)
        layout.setAlignment(Qt.AlignLeft)
        self.ChainedRecord = []
        for index in range(100):
            node = DropLabel(' ')
            node.setFixedSize(100, 100)
            node.setStyleSheet("background-color:white;")
            layout.addWidget(node)
            self.ChainedRecord.append(node)
        self.setWidget(main_widget)
        # self.setWidgetResizable(True)


#------> Level 4
class region_Modules(QScrollArea):
    """
    This constructor creates the region_Modules object for TabWidget_ApplyTemplate.
    """
    def __init__(self):
        super(region_Modules, self).__init__()

        # Contains horizontal sets of Label + QScrollArea(modules)
        MainWidget = QWidget()
        layout = QHBoxLayout(MainWidget)
        layout.setAlignment(Qt.AlignLeft)

        # Nested loop to create sets of Label + QScrollArea(modules)
        for topic in ['Label a', 'Label b', 'Label c', 'Label d', 'Label e', 'Label f', 'Label g']:  # Read the number of subgroups from config file
            self.subgroup = QWidget()
            local_layout = QVBoxLayout(self.subgroup)

            # create label
            label = QLabel(topic)

            # create module box
            module_box = QScrollArea()
            module_box_widget = QWidget()
            module_box_layout = QVBoxLayout(module_box_widget)
            for key in range(15):
                test_label = DraggableLabel("Module "+str(key))
                test_label.setMinimumWidth(150)
                module_box_layout.addWidget(test_label)
            module_box_widget.setLayout(module_box_layout)
            module_box.setWidget(module_box_widget)

            local_layout.addWidget(label)
            local_layout.addWidget(module_box)

            self.subgroup.setLayout(local_layout)
            layout.addWidget(self.subgroup)

        self.setWidget(MainWidget)
        self.setWidgetResizable(True)

#~ Draggable Container
class DraggableLabel(QPushButton):
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_start_position = event.pos()

    def mouseMoveEvent(self, event):
        if not (event.buttons() & Qt.LeftButton):
            return
        if (event.pos() - self.drag_start_position).manhattanLength() < QApplication.startDragDistance():
            return
        drag = QDrag(self)
        mimedata = QMimeData()
        mimedata.setText(self.text())
        drag.setMimeData(mimedata)
        pixmap = QPixmap(self.size())
        painter = QPainter(pixmap)
        painter.drawPixmap(self.rect(), self.grab())
        painter.end()
        drag.setPixmap(pixmap)
        drag.setHotSpot(event.pos())
        drag.exec_(Qt.CopyAction | Qt.MoveAction)

#~ Droppable Container
class DropLabel(QPushButton):
    def __init__(self, *args, **kwargs):
        QPushButton.__init__(self, *args, **kwargs)
        self.setAcceptDrops(True)
        self.test_dialog = Test_Dialog(self)
        self.clicked.connect(self.on_pushButton_clicked)

    def on_pushButton_clicked(self):
        self.test_dialog.show()

    def dragEnterEvent(self, event):
        if event.mimeData().hasText():
            event.acceptProposedAction()

    def dropEvent(self, event):
        ''' This is a section where the container is updated. '''
        pos = event.pos()
        text = event.mimeData().text()
        self.setText(text)
        event.acceptProposedAction()

    def contextMenuEvent(self, event):
        menu = QMenu(self)
        menu.setStyleSheet("background-color: gray;")
        quitAction = menu.addAction("Delete node")
        action = menu.exec_(self.mapToGlobal(event.pos()))
        if action == quitAction:
            self.close()

#~ Configuration Dialog
class Test_Dialog(QDialog):
    def __init__(self, parent=None):
        super(Test_Dialog, self).__init__(parent)  # have to attach to parent as a child
                                                   # to make sure the dialog closes  upon main window closes
        self.setMinimumSize(500, 400)
        self.setWindowTitle('Test Dialog')
        lay = QVBoxLayout()
        wid2 = QWidget()
        lay2 = QFormLayout()

        lay2.addRow(QLabel("Input 1:"), QLineEdit())  # data to record
        lay2.addRow(QLabel("Input 2:"), QLineEdit())  # data to record
        lay2.addRow(QLabel("Input 3:"), QLineEdit())  # data to record

        closebutton = QPushButton("Close")
        closebutton.clicked.connect(self.dialog_close)

        wid2.setLayout(lay2)
        lay.addWidget(wid2)
        lay.addWidget(closebutton)
        self.setLayout(lay)

    def dialog_close(self):
        self.close()

#~ Apply to Samples Dialog
class Template_Dialog(QDialog):
    def __init__(self, parent=None):
        super(Template_Dialog, self).__init__(parent)  # have to attach to parent as a child
                                                       # to make sure the dialog closes  upon main window closes
        self.setMinimumSize(500, 400)
        self.setMinimumSize(500, 1000)
        self.setWindowTitle('Apply template')
        lay = QVBoxLayout()
        label = QLabel("Choose samples below:")
        lay.addWidget(label)

        scroll_box = QScrollArea()
        scroll_box_widget = QWidget()
        scroll_box_layout = QVBoxLayout()
        self.checkboxes = []
        checkBoxAll = QCheckBox("Select All / None")
        checkBoxAll.setChecked(False)
        checkBoxAll.stateChanged.connect(self.onStateChangePrincipal)
        scroll_box_layout.addWidget(checkBoxAll)
        for i in range(50):
            sample_box = QCheckBox("Sample number 000.00." + str(i))
            self.checkboxes.append(sample_box)
            scroll_box_layout.addWidget(sample_box)
        scroll_box_widget.setLayout(scroll_box_layout)
        scroll_box.setWidget(scroll_box_widget)
        lay.addWidget(scroll_box)

        closebutton = QPushButton("Apply Templates")
        closebutton.clicked.connect(self.dialog_close)
        lay.addWidget(closebutton)
        self.setLayout(lay)

    @pyqtSlot(int)
    def onStateChangePrincipal(self, state):
        if state == Qt.Checked:
            for checkbox in self.checkboxes:
                checkbox.blockSignals(True)
                checkbox.setCheckState(state)
                checkbox.blockSignals(False)
        else:
            for checkbox in self.checkboxes:
                checkbox.blockSignals(False)
                checkbox.setCheckState(state)
                checkbox.blockSignals(True)

    def dialog_close(self):
        self.close()


#------> Level 4
class TabWidget_RecipeView(QWidget):
    """
    This constructor creates the layout for PageWidget_RcpMngr >> TabWidget_RecipeView.
    """
    def __init__(self):
        super(TabWidget_RecipeView, self).__init__()

        self.layout = QVBoxLayout()
        scroll_box = QScrollArea()
        main_widget = QWidget()
        main_layout = QFormLayout()

        # Adding all the sample recipes
        for i in range(15):
            main_layout.addRow(QLabel("Sample "+str(i)), RecipeView(i))  # pull the data from log-in info
        main_widget.setLayout(main_layout)
        scroll_box.setWidget(main_widget)

        self.layout.addWidget(scroll_box)
        self.setLayout(self.layout)


#~ Indv Recipe Container (now copied from region_RecipeChain)
class RecipeView(QScrollArea):
    """
        This constructor creates the region_RecipeChain object for TabWidget_ApplyTemplate.
        """
    def __init__(self, *arg):
        super(RecipeView, self).__init__()
        main_widget = QWidget()
        layout = QHBoxLayout(main_widget)
        layout.setAlignment(Qt.AlignLeft)
        self.ChainedRecord = []
        for index in range(10):
            node = DropLabel(' ')
            node.setFixedSize(100, 100)
            node.setStyleSheet("background-color:white;")
            layout.addWidget(node)
            self.ChainedRecord.append(node)
        self.setWidget(main_widget)
        # self.setWidgetResizable(True)


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
    class StackWidget_ActView(TabWidget_RecipeView):
        def __init__(self, outer):
            super(PageWidget_Analysis.StackWidget_ActView, self).__init__()

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

            self.main_layout = QVBoxLayout()
            return_button = QPushButton("return")
            return_button.clicked.connect(self.returnpage)




            self.main_layout.addWidget(return_button)
            self.setLayout(self.main_layout)

        def returnpage(self):
            self.outer.stackpages.setCurrentIndex(0)


#----> Level 3
class PageWidget_ML(QWidget):
    """
    This constructor creates the layout for Stacked Pages.
    """
    def __init__(self):
        super(PageWidget_ML, self).__init__()


"""
-------------------------------------------------------------
-------------------------------------------------------------
-------------------------------------------------------------
--------------------- MAIN APPLICATION ----------------------
-------------------------------------------------------------
-------------------------------------------------------------
-------------------------------------------------------------
"""


if __name__ == "__main__":
    # Starting Application
    app = QApplication(sys.argv)
    app.setApplicationName("ML-ALD Data Interface")
    app.setStyle(QStyleFactory.create('Fusion'))

    ''' Initiate Main Window '''
    window = MainWindow()
    # Attaching CentralWidget
    main_widget = CentralWidget()
    window.setCentralWidget(main_widget)


    window.show()
    sys.exit(app.exec_())
