from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QIcon, QAction
from PySide6.QtWidgets import QMainWindow, QWidget, QTabWidget, QToolBar, QStatusBar, QVBoxLayout

from Classes.Configuration_Data import Configuration_Data
from Classes.MDF_Elaboration_Widget import MDF_Elaboration_Widget
from Classes.Pwm_Reader_Widget import Pwm_Reader_Widget
from Classes.QTextEditLogger import QTextEditLogger

from Classes.MDF_Creator_Widget import MDF_Creator_Widget
from Classes.MDF_Elaboration_Widget import MDF_Elaboration_Widget
from Classes.CSV_Creator_Widget import CSV_Creator_Widget

from icons.resources import resource_path
import logging


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SIL tools")
        self.left = 100
        self.top = 100
        self.width = 320
        self.height = 240
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.configuration_data = Configuration_Data()
        self.mdf_creator_widget = MDF_Creator_Widget(self.configuration_data)
        self.mdf_elaboration_widget = MDF_Elaboration_Widget(self.configuration_data)
        self.csv_creator_widget = CSV_Creator_Widget(self.configuration_data)
        self.csv_to_mdf_widget = CSV_Creator_Widget(self.configuration_data)
        self.mdf_elaboration_widget = MDF_Elaboration_Widget(self.configuration_data)
        self.pwm_reader_widget = Pwm_Reader_Widget()
        #self.setStyleSheet("background-color: rgb(255, 255, 255)")

        toolbar_action_new = QAction(QIcon(resource_path("new_configuration.png")), "New", self)
        toolbar_action_new.setStatusTip("Create new configuration")
        #toolbar_action_new.triggered.connect(self.configuration_file.new)

        toolbar_action_open = QAction(QIcon(resource_path("open.jpg")), "Open", self)
        toolbar_action_open.setStatusTip("Open existing configuration")
        #toolbar_action_open.triggered.connect(self.open_configuration_file)

        toolbar_action_save = QAction(QIcon(resource_path("save.ico")), "Save", self)
        toolbar_action_save.setStatusTip("Save current configuration")
        #toolbar_action_save.triggered.connect(self.save_configuration_file)

        toolbar_action_save_as = QAction(QIcon(resource_path("save_as.jpeg")), "Save as", self)
        toolbar_action_save_as.setStatusTip("Save new configuration")
        #toolbar_action_save_as.triggered.connect(self.save_configuration_file_as)

        # ####################
        toolbar = QToolBar("My main toolbar")
        toolbar.setIconSize(QSize(24, 24))
        toolbar.addAction(toolbar_action_new)
        toolbar.addAction(toolbar_action_open)
        toolbar.addAction(toolbar_action_save)
        toolbar.addAction(toolbar_action_save_as)
        self.addToolBar(toolbar)
        #
        menu = self.menuBar()
        #
        file_menu = menu.addMenu("File")
        file_menu.addAction(toolbar_action_new)
        file_menu.addAction(toolbar_action_open)
        file_menu.addAction(toolbar_action_save)
        file_menu.addAction(toolbar_action_save_as)

        self.setStatusBar(QStatusBar(self))

        # definisci il widget delle tab
        tab_widget = QTabWidget()
        tab_widget.setDocumentMode(True)
        tab_widget.setTabPosition(QTabWidget.North)
        tab_widget.setMovable(False)

        tab_widget.insertTab(0, self.mdf_creator_widget, "MDF Creator")
        tab_widget.insertTab(1, self.mdf_elaboration_widget, "MDF Elaboration")
        tab_widget.insertTab(2, self.csv_creator_widget, "CSV Creator")
        tab_widget.insertTab(3, self.pwm_reader_widget, "Arduino set Conversions")

        #logTextBox = QTextEditLogger(self)
        #logging.getLogger().addHandler(logTextBox)

        # Set main layout
        main_layout = QVBoxLayout()
        main_layout.addWidget(tab_widget)
        #main_layout.addWidget(logTextBox.widget)

        # Serve un layout a cui assegnare il layout
        main_widget = QWidget()
        main_widget.setLayout(main_layout)

        # Set main_widget as the central layout of the main window
        self.setCentralWidget(main_widget)
        self.setWindowIcon(QIcon(resource_path("test_new.png")))

    def open_configuration_file(self):
        try:
            print("to be replaced")
            #hil_function_file_data, tc_highlight_data, tc_substitution_data = self.configuration_file.open()
            #self.tc_substitution_widget.update_handler(tc_substitution_data)
        except ValueError:
            logging.warning("No file selected")
            self.statusBar().showMessage("No file selected", 2500)

    def save_configuration_file(self):
        print("to be replaced")
        #hil_function_file_data = HIL_Function_Configuration_Data()
        #tc_highlight_data = TC_Highlight_Configuration_Data()
        #tc_substitution_data = self.tc_substitution_widget.tc_substitution_handler.cfg_data
        #self.configuration_file.save(hil_function_file_data=hil_function_file_data.return_json_dict(),
        #                             tc_highlight_data=tc_highlight_data.return_json_dict(),
        #                             tc_substitution_data=tc_substitution_data.return_json_dict(),
        #                             select_new_file=False)

    def save_configuration_file_as(self):
        print("to be replaced")
        #hil_function_file_data = HIL_Function_Configuration_Data()
        #tc_highlight_data = TC_Highlight_Configuration_Data()
        #tc_substitution_data = self.tc_substitution_widget.tc_substitution_handler.cfg_data
        #self.configuration_file.save(hil_function_file_data=hil_function_file_data.return_json_dict(),
        #                             tc_highlight_data=tc_highlight_data.return_json_dict(),
        #                             tc_substitution_data=tc_substitution_data.return_json_dict(),
        #                             select_new_file=True)
