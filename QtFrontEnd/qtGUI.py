import sys
from PyQt5.QtCore import QDateTime, Qt, QTimer
from PyQt5.QtWidgets import (QApplication, QCheckBox, QComboBox, QDateTimeEdit,
        QDial, QDialog, QGridLayout, QGroupBox, QHBoxLayout, QLabel, QLineEdit,
        QProgressBar, QPushButton, QRadioButton, QScrollBar, QSizePolicy,
        QSlider, QSpinBox, QStyleFactory, QTableWidget, QTabWidget, QTextEdit,
        QVBoxLayout, QWidget, QStyleFactory)
import pyqtgraph


class WidgetGallery(QDialog):
    def __init__(self, parent=None):
        super(WidgetGallery, self).__init__(parent)
        self.setMinimumSize(1500, 1000)

        # Create widgets
        self.create_topLayout()
        self.create_widget_browser()
        self.create_widget_metadata()
        self.create_widget_plot()

        # Create Grid Layout object
        mainLayout = QGridLayout()
        # addWidget :: QWidget, row, column, rowSpan, columnSpan, alignment = 0
        mainLayout.addLayout(self.topLayout, 0, 0, 1, 2)
        mainLayout.addWidget(self.browser_box, 1, 0)
        mainLayout.addWidget(self.metadata_box, 1, 1)
        mainLayout.addWidget(self.plot_box, 2, 0, 2, 2)
        mainLayout.setRowStretch(1, 2)  # set row 1 stretch factor
        mainLayout.setRowStretch(2, 3)  # set row 2 stretch factor
        mainLayout.setColumnStretch(0, 1)  # set column 0 stretch factor
        mainLayout.setColumnStretch(1, 1)  # set column 1 stretch factor
        self.setLayout(mainLayout)

        self.setWindowTitle("ALD Sample Manager")

    def create_topLayout(self):
        self.styleComboBox = QComboBox()
        self.styleComboBox.addItems(['ALD', 'Ellipsometry', 'QCM'])
        self.styleLabel = QLabel("&Equipment:")
        self.styleLabel.setBuddy(self.styleComboBox)

        self.topLayout = QHBoxLayout()
        self.topLayout.addWidget(self.styleLabel)
        self.topLayout.addWidget(self.styleComboBox)
        self.topLayout.addStretch(1)

    def create_widget_browser(self):
        self.browser_box = QGroupBox("File Browser")

        checkBox = QCheckBox("Tri-state check box")
        checkBox.setTristate(True)
        checkBox.setCheckState(Qt.PartiallyChecked)

        layout = QVBoxLayout()
        layout.addWidget(checkBox)
        layout.addStretch(1)
        self.browser_box.setLayout(layout)

    def create_widget_metadata(self):
        self.metadata_box = QTabWidget()
        self.metadata_box.setSizePolicy(QSizePolicy.Preferred,
                                        QSizePolicy.Ignored)

        tab1 = QWidget()
        tableWidget = QTableWidget(10, 10)

        tab1hbox = QHBoxLayout()
        tab1hbox.setContentsMargins(5, 5, 5, 5)
        tab1hbox.addWidget(tableWidget)
        tab1.setLayout(tab1hbox)

        tab2 = QWidget()
        textEdit = QTextEdit()

        textEdit.setPlainText("Twinkle, twinkle, little star,\n"
                              "How I wonder what you are.\n"
                              "Up above the world so high,\n"
                              "Like a diamond in the sky.\n"
                              "Twinkle, twinkle, little star,\n"
                              "How I wonder what you are!\n")

        tab2hbox = QHBoxLayout()
        tab2hbox.setContentsMargins(5, 5, 5, 5)  # all-around 5 pixels
        tab2hbox.addWidget(textEdit)
        tab2.setLayout(tab2hbox)

        self.metadata_box.addTab(tab1, "&Table")  # keyboard shortcut Alt+T
        self.metadata_box.addTab(tab2, "Text &Edit")  # keyboard shortcut Alt+E

    def create_widget_plot(self):
        self.plot_box = QGroupBox("Plot: " + self.styleComboBox.currentText())
        self.styleComboBox.activated.connect(self.update_group_title)

        # Create one-line text widget
        lineEdit = QLineEdit('s3cRe7')
        lineEdit.setEchoMode(QLineEdit.Normal)  # display characters as entered, no masking

        # Create slider widget
        slider = QSlider(Qt.Horizontal, self.plot_box)
        slider.setValue(40)

        # Create Grid Layout object
        layout = QGridLayout()
        layout.addWidget(lineEdit, 4, 0, 1, 2)
        layout.addWidget(slider, 5, 0, 1, 2)
        layout.setRowStretch(0, 1)
        self.plot_box.setLayout(layout)

    def update_group_title(self):
        self.plot_box.setTitle("Plot: " + self.styleComboBox.currentText())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle(QStyleFactory.create('Fusion'))
    ex = WidgetGallery()
    ex.show()
    sys.exit(app.exec_())
