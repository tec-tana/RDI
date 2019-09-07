import sys
from PyQt5.QtWidgets import (QPushButton, QDialog, QTreeWidget,
                             QTreeWidgetItem, QVBoxLayout,
                             QHBoxLayout, QFrame, QLabel,
                             QApplication, QStyleFactory,
                             QMainWindow, QAction)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot


class Application(QApplication):

    def __init__(self):
        super().__init__(sys.argv)
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


class SectionExpandButton(QPushButton):
    """a QPushbutton that can expand or collapse its section
    """

    def __init__(self, item, text = "", parent = None):
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

    def add_button(self, title):
        """creates a QTreeWidgetItem containing a button
        to expand or collapse its section
        """
        item = QTreeWidgetItem()
        self.tree.addTopLevelItem(item)
        self.tree.setItemWidget(item, 0, SectionExpandButton(item, text = title))
        return item

    def add_widget(self, button, widget):
        """creates a QWidgetItem containing the widget,
        as child of the button-QWidgetItem
        """
        section = QTreeWidgetItem(button)
        section.setDisabled(True)
        self.tree.setItemWidget(section, 0, widget)
        return section


if __name__ == "__main__":
    app = Application()
    app.setApplicationName("ML-ALD Data Interface -- Lehigh University")
    app.setStyle(QStyleFactory.create('Fusion'))

    window = CollapsibleDialog()
    window.show()

    ex1 = GUI()
    ex2 = ConfigGallery()
    sys.exit(app.exec_())





