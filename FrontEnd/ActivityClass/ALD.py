import sys
from PyQt5.QtCore import QDateTime, Qt, QTimer
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (QApplication, QCheckBox, QComboBox, QDateTimeEdit,
        QDial, QDialog, QGridLayout, QGroupBox, QHBoxLayout, QLabel, QLineEdit,
        QProgressBar, QPushButton, QRadioButton, QScrollBar, QSizePolicy,
        QSlider, QSpinBox, QStyleFactory, QFileDialog, QTableWidget, QTabWidget, QTextEdit,
        QVBoxLayout, QWidget, QStyleFactory, QMainWindow)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt
import pandas as pd


class ConfigGallery(QMainWindow):
    def __init__(self, parent=None):
        super(ConfigGallery, self).__init__(parent)
        self.setMinimumSize(2000, 1500)
        # self.setGeometry(50, 50, 500, 300)
        # self.setWindowTitle("PyQT tuts!")
        self.setWindowIcon(QIcon('pythonlogo.png'))
        self.InitUI()
        self.show()

    def InitUI(self):
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

    def create_topLayout(self):
        self.equipment_type_combo = QComboBox()
        self.equipment_type_combo.addItems(['Savanah ALD', 'Stacy MLD', 'Apollo101 ALD'])
        self.equipment_type_label = QLabel("&Equipment:")
        self.equipment_type_label.setBuddy(self.equipment_type_combo)

        self.topLayout = QHBoxLayout()
        self.topLayout.addWidget(self.equipment_type_label)
        self.topLayout.addWidget(self.equipment_type_combo)
        self.topLayout.addStretch(1)

    def create_widget_browser(self):
        self.browser_box = QGroupBox("File Browser")

        self.open_file_label = QLineEdit()
        self.open_file_button = QPushButton("&Open file")
        self.open_file_button.clicked.connect(self.openfile)

        self.study_type_combo = QComboBox()
        self.study_type_combo.addItems(['Temperature - QCM', 'Pressure - QCM', 'All - QCM'])
        self.study_type_label = QLabel("&Type of Study:")
        self.study_type_label.setBuddy(self.study_type_combo)
        self.study_type_combo.activated.connect(self.update_group_title)

        self.checkBox = QCheckBox("Use Moving Averages")
        self.checkBox.setChecked(True)
        # self.checkBox.setTristate(True)
        # self.checkBox.setCheckState(Qt.PartiallyChecked)

        # Use for displaying warning messages
        self.warning_message = QLabel("")
        self.warning_message.setStyleSheet("font-weight: bold; color: red")
        self.warning_message.setAlignment(Qt.AlignCenter)

        # button connected to `timeseries_plot` method
        self.plot_button = QPushButton('Plot')
        self.plot_button.clicked.connect(self.timeseries_plot)

        layout = QGridLayout()
        layout.addWidget(self.open_file_label, 0, 0, 1, 5)
        layout.addWidget(self.open_file_button, 0, 5, 1, 1)
        layout.addWidget(self.study_type_label, 1, 0, 1, 1)
        layout.addWidget(self.study_type_combo, 1, 1, 1, 5)
        layout.addWidget(self.checkBox, 2, 0, 1, 3)
        layout.addWidget(self.plot_button, 3, 2, 1, 2)
        layout.addWidget(self.warning_message, 4, 0, 1, 6)
        layout.setAlignment(Qt.AlignTop)
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
        textEdit.setPlaceholderText("Put your description here")

        tab2hbox = QHBoxLayout()
        tab2hbox.setContentsMargins(5, 5, 5, 5)  # all-around 5 pixels
        tab2hbox.addWidget(textEdit)
        tab2.setLayout(tab2hbox)

        self.metadata_box.addTab(tab1, "Recipe &Table")  # keyboard shortcut Alt+T
        self.metadata_box.addTab(tab2, "&Description")  # keyboard shortcut Alt+D

    def create_widget_plot(self):
        self.plot_box = QGroupBox()
        self.update_group_title()
        self.equipment_type_combo.activated.connect(self.update_group_title)

        # embed timeseries_plot on the widget
        self.figure = plt.figure()

        # this is the Canvas Widget that displays the `figure`
        # it takes the `figure` instance as a parameter to __init__
        self.canvas = FigureCanvas(self.figure)

        # this is the Navigation widget
        # it takes the Canvas widget and a parent
        self.toolbar = NavigationToolbar(self.canvas, self)

        # Create one-line text widget
        self.lineEdit = QLineEdit()
        self.lineEdit.setPlaceholderText('Put comments here...')
        self.lineEdit.setEchoMode(QLineEdit.Normal)  # display characters as entered, no masking

        # Create x-axes slider widget
        self.slider = QSlider(Qt.Horizontal, self.plot_box)
        self.slider.setMaximum(150)
        self.slider.setMinimum(1)
        self.slider.setValue(100)
        self.slider.valueChanged.connect(self.setPlotZoom)

        # Create y-axes slider widget
        self.Vslider = QSlider(Qt.Vertical, self.plot_box)
        self.Vslider.setMaximum(400)
        self.Vslider.setMinimum(100)
        self.Vslider.setValue(250)
        self.Vslider.valueChanged.connect(self.setPlotZoom)

        # Create scroll bar
        self.scrollBar = QScrollBar(Qt.Horizontal, self.plot_box)
        self.scrollBar.setValue(0)
        self.scrollBar.valueChanged.connect(self.setPlotZoom)

        # Create Grid Layout object
        layout = QGridLayout()
        layout.addWidget(self.toolbar, 0, 0, 1, 2)
        layout.addWidget(self.canvas, 1, 1, 3, 2)
        layout.addWidget(self.lineEdit, 4, 1, 1, 2)
        layout.addWidget(self.Vslider, 1, 0, 3, 1)
        layout.addWidget(self.slider, 5, 1, 1, 2)
        layout.addWidget(self.scrollBar, 6, 1, 1, 2)
        layout.setRowStretch(0, 1)
        self.plot_box.setLayout(layout)

    def openfile(self):
        self.fname = QFileDialog.getOpenFileName(self, 'Open file',
                                            r'C:\Users\Tanat\PycharmProjects\nhi-datacollection-ald\venv\Scripts\Results\pickle', "Pickle files (*.pkl)")
        self.open_file_label.setText(self.fname[0])

    def update_group_title(self):
        self.plot_box.setTitle("Plot: " + self.equipment_type_combo.currentText() +
                               ", " + self.study_type_combo.currentText())

    def timeseries_plot(self):
        """
        timeseries_plot ALD data

        :return:
        """
        try:
            filename = self.fname[0]
            self.warning_message.setText('')
            # load pickle dataframe
            self.data = pd.read_pickle(filename)
            self.data['Pressure'] = pd.to_numeric(self.data['Pressure'], errors='coerce')  # convert to number
            # calculate moving averages
            # This could be replaced by more sophisticated modules

            if self.checkBox.isChecked():
                # use moving averages columns
                ''' Calculate moving averages for heater temperature and pressure '''
                heater_header = list()
                num_heater = sum(1 for word in self.data.columns.tolist() if 'Heater' in word)
                for i in range(1, num_heater + 1):
                    header = 'Heater ' + str(i)
                    new_header = header + ' MA'
                    self.data[new_header] = self.data[header].rolling(window=1).mean()
                    heater_header.append(new_header)
                self.data['Pressure MA'] = self.data['Pressure'].rolling(window=1).mean()
                pressure_header = ['Pressure MA']
            else:
                ''' set header for heater temperature and pressure '''
                heater_header = [header for header in self.data.columns.tolist() if 'Heater' in header]
                pressure_header = ['Pressure']
            # Prepare for plotting
            self.figure.clear()  # discards the old graph
            self.axes_heater = self.figure.add_subplot(111)  # create an axis
            # plot timeseries data
            ''' Plotting the combined Pressure / Heater Data '''
            # plt.clf()  # Clear an entire figure, use when trying to plot new info on the same plot
            self.axes_heater.plot(self.data['Time'], self.data[heater_header])
            # plt.legend(prop={'size': 20}, bbox_to_anchor=(1.2, 0.9))
            self.axes_heater.set_xlabel('Time (mins)', size=20)
            self.axes_heater.set_ylabel('Temperature (°C)', size=20)

            self.axes_pressure = self.axes_heater.twinx()
            #self.axes_pressure.spines['right'].set_position(('axes', 1.0))
            self.axes_pressure.plot(self.data['Time'], self.data[pressure_header])
            #self.axes_pressure.legend(prop={'size': 20}, bbox_to_anchor=(1.2, 1))
            self.axes_pressure.set_ylabel('Pressure (Torr)', size=20)

            self.scrollBar.setRange(0, self.data['Time'].iloc[-1])
            self.axes_heater.set_title('Time Series: Pressure & Heater Data', size=20)
            self.axes_heater.set_xlim(xmin=self.scrollBar.value(),
                                      xmax=self.scrollBar.value() + self.data['Time'].iloc[-1]*self.slider.value()/100)
            self.axes_heater.set_ylim(ymin=100, ymax=self.Vslider.value())  # set hard limit to heater temp range

            # refresh canvas
            self.canvas.draw()
        except AttributeError:
            self.warning_message.setText("You have not selected file.")

        except Exception as ex:
            print(ex)

    def setPlotZoom(self):
        try:
            # zoom plot by set x/y-limits
            self.axes_heater.set_xlim(xmin=self.scrollBar.value(),
                                      xmax=self.scrollBar.value() + self.data['Time'].iloc[-1]*self.slider.value()/100)
            self.axes_heater.set_ylim(ymin=100, ymax=self.Vslider.value())  # set hard limit to heater temp range
            self.canvas.draw()  # refresh canvas
        except AttributeError:  # if the slider is moved before plot is generated
            pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle(QStyleFactory.create('Fusion'))
    ex = ConfigGallery()
    ex.show()
    sys.exit(app.exec_())
