import json
import numpy as np
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
from config import cfg

r"""TODO:
Working on this file today gave an error of:
    Exception ignored in: <function Connection.__del__ at 0x00000156B7AC48B8>
    Traceback (most recent call last):
    File "C:\Users\Tanat\PycharmProjects\NHI_DataCollection_Strandwitz\venv\lib\site-packages\datafed\Connection.py", line 102, in __del__
    [...]
    File "C:\Users\Tanat\PycharmProjects\NHI_DataCollection_Strandwitz\venv\lib\site-packages\zmq\sugar\context.py", line 153, in _rm_socket
    TypeError: 'NoneType' object is not callable
    Exception ignored in: <function Socket.__del__ at 0x0000020DD4F5A5E8>
This looks like ZeroMQ library that is used to parallelize concurrent tasks, datafed looks like it's being affected.
"""

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
        tab1 = TabWidget_RecipeView()  # showing current recipe recorded in DataFed
        tab2 = TabWidget_ApplyTemplate()  # blank template to build on for new samples, overrides original DataFed record
        self.tab.addTab(tab1, "Recipe View")
        self.tab.addTab(tab2, "Apply Template")

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
        self.applyTemp = applyTemplateDialog(self)
        button_apply.clicked.connect(self.apply_template)

        self.main_layout.addWidget(region1, 0, 0, 1, 5)
        self.main_layout.addWidget(region2, 1, 0, 3, 5)
        self.main_layout.addWidget(button_apply, 4, 4, 1, 1)
        self.main_layout.setRowStretch(1, 1)
        self.main_layout.setRowMinimumHeight(0, 180)

        self.setLayout(self.main_layout)

    def apply_template(self):
        self.applyTemp.show()

#------> Level 5
class region_RecipeChain(QWidget):
    """
    This constructor creates the region_RecipeChain object for TabWidget_ApplyTemplate.
    """
    initRecord = 10  # the preset initial number of blank records in the chain

    def __init__(self):
        super(region_RecipeChain, self).__init__()
        self.main_layout = QHBoxLayout()

        # Scrolled chained area
        main_scroll = QScrollArea()
        main_widget = QWidget()
        self.layout = QHBoxLayout(main_widget)
        self.layout.setAlignment(Qt.AlignLeft)
        self.ChainedRecord = []  # container for chained records
        self.add_RecordToChain(self.initRecord)  # initialize with fixed # of blank records
        main_scroll.setWidget(main_widget)
        main_scroll.setWidgetResizable(True)
        main_scroll.setFixedHeight(180)

        # Button to add blank record
        addBlank = QPushButton("+")
        addBlank.setFixedSize(100, 100)
        addBlank.clicked.connect(lambda: self.add_RecordToChain(1))

        self.main_layout.addWidget(main_scroll)
        self.main_layout.addWidget(addBlank)
        self.setLayout(self.main_layout)

    def add_RecordToChain(self, N:int=1):
        for index in range(N):
            node = DropBin("")
            node.setFixedSize(100, 100)
            node.setStyleSheet("background-color:white;")
            self.layout.addWidget(node)
            self.ChainedRecord.append(node)
        self.setLayout(self.main_layout)

#------> Level 5
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

        # Load activity module config
        with open("config/activity_modules.json", "r") as f:
            activities = json.load(f)

        # generate color gradient
        colors = list()
        for i in range(len(activities['category'])):
            colors.append((np.random.choice(range(255)),
                           np.random.choice(range(255)),
                           np.random.choice(range(255))))

        # Nested loop to create sets of Label + QScrollArea(modules)
        for topic in activities['category']:  # Read the number of subgroups from config file
            klr = colors.pop()
            #print(klr)  # print rgb combination (255,255,255)
            self.subgroup = QWidget()
            local_layout = QVBoxLayout(self.subgroup)

            # create group label
            label = QLabel(topic["name"])

            # create module box
            module_box = QScrollArea()
            module_box_widget = QWidget()
            module_box_layout = QVBoxLayout(module_box_widget)

            # This is the main location that assign and create new modules as draggable labels
            self.module_item = list()  # this contains objects of DraggableLabel
            for k,module in enumerate(topic["module"]):
                self.module_item.append(DragModule(module["name"]))
                self.module_item[k].name = module["name"]
                self.module_item[k].config = module["config"]
                #self.module_item[k].setMinimumWidth(150)
                self.module_item[k].setStyleSheet("background-color: rgb{0}; color: {1}"
                                                  .format(str(klr), (r'white' if sum(klr)<280 else r'black')))
                module_box_layout.addWidget(self.module_item[k])


            module_box_widget.setLayout(module_box_layout)
            module_box.setWidget(module_box_widget)

            local_layout.addWidget(label)
            local_layout.addWidget(module_box)

            self.subgroup.setLayout(local_layout)
            layout.addWidget(self.subgroup)

        self.setWidget(MainWidget)
        self.setWidgetResizable(True)

#~ Draggable Container
class DragModule(QPushButton):
    """
    containers that represent black modules to be dragged to recipe chain
    these containers cannot do much more, but the have identifier to pass onto droppable containers
    """
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

#~ Droppable Containers
class DropBin(QPushButton):
    """
    containers that represent the recipe chain
    these containers take in identifier of which modules were dragged into
    """
    def __init__(self, *args, **kwargs):
        QPushButton.__init__(self, *args, **kwargs)
        self.setAcceptDrops(True)
        self.configure_module = Configure_Module(self)
        self.clicked.connect(self.on_pushButton_clicked)

    def on_pushButton_clicked(self):
        if len(self.text()) > 1:
            self.configure_module.show()

    def dragEnterEvent(self, event):
        if event.mimeData().hasText():
            event.acceptProposedAction()

    def dropEvent(self, event):
        """
        This is a section where the container is updated.
        """
        pos = event.pos()
        text = event.mimeData().text()
        self.setText(text)  # set the label shown
        # self.setStyleSheet('')  # set the stylesheet
        #TODO: set module identifier from draggable label (event.mimeData().___)

        event.acceptProposedAction()

    def contextMenuEvent(self, event):
        menu = QMenu(self)
        menu.setStyleSheet("background-color: gray;")
        quitAction = menu.addAction("Delete node")
        action = menu.exec_(self.mapToGlobal(event.pos()))
        if action == quitAction:
            self.close()

#~ Configuration Dialog
class Configure_Module(QDialog):
    """
    the template of configuration dialog is based on the key each module holds.
    TODO: Right now, below is just the draft, customization was not implemented.
    """
    def __init__(self, parent=None):
        super(Configure_Module, self).__init__(parent)  # have to attach to parent as a child
                                                        # to make sure the dialog closes  upon main window closes
        # Check if the


        # Load activity module config
        with open("config/activity_modules.json", "r") as f:
            activities = json.load(f)

        self.setMinimumSize(500, 400)
        self.setWindowTitle('Configure Module')
        lay = QVBoxLayout()
        wid2 = QWidget()
        lay2 = QFormLayout()

        #TODO: config for each instrument should be recorded under `activities` object
        lay2.addRow(QLabel("Input 1:"), QLineEdit())  # data to record
        lay2.addRow(QLabel("Input 2:"), QLineEdit())  # data to record
        lay2.addRow(QLabel("Input 3:"), QLineEdit())  # data to record

        savebutton = QPushButton("Save")
        savebutton.clicked.connect(self.save_setting)
        closebutton = QPushButton("Cancel")
        closebutton.clicked.connect(self.dialog_close)

        wid2.setLayout(lay2)
        lay.addWidget(wid2)
        lay.addWidget(savebutton)
        lay.addWidget(closebutton)
        self.setLayout(lay)

    def dialog_close(self):
        self.close()

    def save_setting(self):
        """
        This saves setting to cfg object that handles DOI
        """
        #TODO: identify the format of coll to be added
        #cfg.doi.save_setting()


#~ Apply to Samples Dialog
class applyTemplateDialog(QDialog):
    def __init__(self, parent=None):
        super(applyTemplateDialog, self).__init__(parent)  # have to attach to parent as a child
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

        #TODO: replace with the real number of sameples in that collection
        # Each data file in a collection represent the entire knowledge about one specific sample.
        for i in range(50):
            sample_box = QCheckBox("Sample number 000.00." + str(i))
            self.checkboxes.append(sample_box)
            scroll_box_layout.addWidget(sample_box)
        scroll_box_widget.setLayout(scroll_box_layout)
        scroll_box.setWidget(scroll_box_widget)
        lay.addWidget(scroll_box)

        closebutton = QPushButton("Apply Templates")
        closebutton.clicked.connect(self.apply_template)
        closebutton = QPushButton("Cancel")
        closebutton.clicked.connect(self.dialog_close)
        lay.addWidget(closebutton)
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

    def apply_template(self):
        """
        apply template to selected samples
        :return:
        """
        #TODO: identify the format of coll to be added
        cfg.doi.apply_template()


#------> Level 4
class TabWidget_RecipeView(QWidget):
    """
    This constructor creates the layout for PageWidget_RcpMngr >> TabWidget_RecipeView.
    """
    def __init__(self):
        super(TabWidget_RecipeView, self).__init__()

        # setting scroll area
        self.layout = QVBoxLayout()
        scroll_box = QScrollArea()
        # setting layout within scroll area
        main_layout = QGridLayout()
        box = QWidget()
        box.setLayout(main_layout)

        # setting containers for recipe records
        self.RecipeRecord = []
        # Adding all the sample recipes
        #TODO: replace with the real number of samples in that collection
        # Each data file in a collection represent the entire knowledge about one specific sample.
        for i in range(15):
            self.RecipeRecord.append(RecipeView(i))
            main_layout.addWidget(QLabel("Sample "+str(i)), i, 0)
            main_layout.addWidget(self.RecipeRecord[i], i, 1)

        box.setLayout(main_layout)
        scroll_box.setWidget(box)
        self.layout.addWidget(scroll_box)
        self.setLayout(self.layout)

    def update(self):
        '''
        updating the records for view
        '''
        pass


#~ Indv Recipe Container (now copied from region_RecipeChain)
class RecipeView(QWidget):
    """
        This constructor creates the region_RecipeChain object for TabWidget_ApplyTemplate.
    """
    initRecord = 50
    def __init__(self, *arg):
        super(RecipeView, self).__init__()
        self.main_layout = QHBoxLayout()

        #main_scroll = QScrollArea()    # Scrolled chained area
                                        #  This current scrolla area setup is for each and every
                                        #  samples. However, the scroll area somehow fails to
                                        #  stretch over the remaining width of the window and
                                        #  only cap at ~8 samples visible.

                                        #  The other way to do this is to section the layout
                                        #  horizontally. In that case, the sample label will
                                        #  always be visible on the left.
        main_widget = QWidget()
        self.layout = QHBoxLayout(main_widget)
        self.layout.setAlignment(Qt.AlignLeft)
        self.ChainedRecord = []  # container for chained records
        self.add_RecordToChain(self.initRecord)  # initialize with fixed # of blank records
        #main_scroll.setWidget(main_widget)
        #main_scroll.setWidgetResizable(True)
        #main_scroll.setFixedHeight(180)

        self.main_layout.addWidget(main_widget)
        self.setLayout(self.main_layout)

    def add_RecordToChain(self, N:int=1):
        for index in range(N):
            node = DropBin("")
            node.setFixedSize(100, 100)
            node.setStyleSheet("background-color:white;")
            self.layout.addWidget(node)
            self.ChainedRecord.append(node)
        self.setLayout(self.main_layout)
