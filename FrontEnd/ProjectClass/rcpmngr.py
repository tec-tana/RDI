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

#------> Level 5
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

            # create label
            label = QLabel(topic["name"])

            # create module box
            module_box = QScrollArea()
            module_box_widget = QWidget()
            module_box_layout = QVBoxLayout(module_box_widget)
            for module in topic["module"]:
                test_label = DraggableLabel(module["name"])
                #test_label.setMinimumWidth(150)
                test_label.setStyleSheet("background-color: rgb{0}; color: {1}"
                                         .format(str(klr), (r'white' if sum(klr)<280 else r'black')))
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
