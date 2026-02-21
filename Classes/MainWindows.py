from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QIcon, QAction
from PySide6.QtWidgets import QMainWindow, QWidget, QTabWidget, QToolBar, QStatusBar, QVBoxLayout, QTextBrowser, \
    QHBoxLayout, QPushButton

from Classes.Configuration_Data import Configuration_Data
from Classes.MDF_Elaboration_Widget import MDF_Elaboration_Widget
from Arduino.PWM_Reader_Widget import Pwm_Reader_Widget
from Classes.QTextEditLogger import QTextEditLogger

from Classes.MDF_Creator_Widget import MDF_Creator_Widget
from Classes.MDF_Elaboration_Widget import MDF_Elaboration_Widget
from Classes.CSV_Creator_Widget import CSV_Creator_Widget
from Vector.VectorFileGenerator import VectorFileGenerator

from icons.resources import resource_path
import logging, os

from Classes.LoggingStream import df_logger
logger = logging.getLogger("SIL_TOOLS")

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
        self.vector_file_generator = VectorFileGenerator(self.configuration_data)

        #self.setStyleSheet("background-color: rgb(255, 255, 255)")

        toolbar_action_new = QAction(QIcon(resource_path("new_configuration.png")), "New", self)
        toolbar_action_new.setStatusTip("Create new configuration")
        #toolbar_action_new.triggered.connect(self.configuration_file.new)

        toolbar_action_open = QAction(QIcon(resource_path("open.jpg")), "Open", self)
        toolbar_action_open.setStatusTip("Open existing configuration")
        toolbar_action_open.triggered.connect(self.open_configuration_file)

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

        if self.configuration_data.tab_mdf_conversion:
            tab_widget.insertTab(0, self.mdf_creator_widget, "MDF Creator")
        if self.configuration_data.tab_mdf_elaboration:
            tab_widget.insertTab(1, self.mdf_elaboration_widget, "MDF Elaboration")
        if self.configuration_data.tab_csv_conversion:
            tab_widget.insertTab(2, self.csv_creator_widget, "CSV Creator")
        if self.configuration_data.tab_arduino:
            tab_widget.insertTab(3, self.pwm_reader_widget, "Arduino set Conversions")
        tab_widget.insertTab(4, self.vector_file_generator, "Vector File Generator")

        #logTextBox = QTextEditLogger(self)
        #logging.getLogger().addHandler(logTextBox)

        # Set main layout
        main_layout = QVBoxLayout()
        main_layout.addWidget(tab_widget)
        #main_layout.addWidget(logTextBox.widget)

        #logTextBox = QTextEditLogger(self)
        #logging.getLogger().addHandler(logTextBox)

        ############### LOGGING  ###############
        self.logging_text_browser = QTextBrowser(self)
        # LoggingStream.stdout().messageWritten.connect(self.logging_text_browser.insertPlainText)
        # LoggingStream.stderr().messageWritten.connect(self.logging_text_browser.insertPlainText)
        for handler in logger.handlers:
            if hasattr(handler, "name"):
                if handler.name == "qt_text_browser_logging":
                    handler.add_widget(self.logging_text_browser)
        #df_logger.log_signal.connect(self.append_log)
        main_layout.addWidget(self.logging_text_browser)
        ############### CLEAR BUTTON  ###############
        clear_row_layout = QHBoxLayout()
        clear_row_layout.addStretch()
        btn_clear_window = QPushButton("Clear window")
        btn_clear_window.setIcon(QIcon(resource_path('cleanup-icon-small.jpg')))
        btn_clear_window.pressed.connect(self.clear_window)
        clear_row_layout.addWidget(btn_clear_window)
        main_layout.addLayout(clear_row_layout)

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

    def clear_window(self):
        self.logging_text_browser.clear()

    def append_log(self, log_text: str):
        """Slot to update QTextBrowser."""
        self.logging_text_browser.append(f"{log_text}")