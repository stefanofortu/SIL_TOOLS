import os.path

from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QFrame, QGridLayout, \
    QFileDialog, QComboBox
from pandas import to_timedelta

from Converters.Dewesoft_to_CSV import Dewesoft_to_CSV
from Converters.PumpLogger_to_MDF import PumpLogger_to_MDF
from Classes.Configuration_Data import Configuration_Data
from Converters.Vector_to_MDF import Vector_to_MDF
from icons.resources import resource_path

import Classes.GUI_Configuration as GUI_Configuration
from libraries.DW_to_Py_Converter import Dewesoft_Converter


class CSV_Creator_Widget(QWidget):

    def __init__(self, cfg_data):
        super().__init__()

        self.file_name_list = None
        if not isinstance(cfg_data, Configuration_Data):
            print("cfg_data not Configuration_Data")
            exit()

        widget_main_layout = QVBoxLayout()
        # ############### TITLE LABEL ###############
        # conversion_title_label = QLabel(self)
        # conversion_title_label.setFrameStyle(QFrame.Sunken)
        # conversion_title_label.setAlignment(Qt.AlignCenter)
        # conversion_title_label.setText("Conversion to MDF")
        # conversion_title_label.setStyleSheet('background-color: rgb(255,140,0)')
        #
        # widget_main_layout.addWidget(conversion_title_label)
        #
        # ############### SELECTION BOX FILE  ###############
        # # Create a Vertical Layout
        # comboBox_VLayout = QVBoxLayout()
        #
        # # Introduction label
        # self.selection_label = QLabel("Select an option:")
        #
        # # Create a ComboBox
        # self.selection_comboBox = QComboBox()
        # self.selection_comboBox.addItems(GUI_Configuration.GUI_mdf_converstion_selection)
        #
        # # Layout and main widget
        # comboBox_VLayout.addWidget(self.selection_label)
        # comboBox_VLayout.addWidget(self.selection_comboBox)
        # widget_main_layout.addLayout(comboBox_VLayout)
        #
        # ############### INPUT FILE ###############
        # input_file_layout = QGridLayout()
        # #
        # input_file_description_label = QLabel(self)
        # input_file_description_label.setText("Input CSV file :")
        # input_file_description_label.setAlignment(Qt.AlignLeft)
        # input_file_layout.addWidget(input_file_description_label, 0, 0)
        # #
        # self.input_file_path_label = QLabel(self)
        # self.input_file_path_label.setFrameStyle(QFrame.Panel | QFrame.Sunken)
        # self.input_file_path_label.setText("-")
        # self.input_file_path_label.setAlignment(Qt.AlignLeft)
        # input_file_layout.addWidget(self.input_file_path_label, 1, 0, 1, 8)
        # #
        # btn_input_file_selector = QPushButton("Add ")
        # btn_input_file_selector.setIcon(QIcon(resource_path("folder-icon.jpg")))
        # # btn_input_file_selector.setToolTip("<b>HTML</b> <i>can</i> be shown too..")
        # btn_input_file_selector.pressed.connect(self.open_input_file_dialog)
        # input_file_layout.addWidget(btn_input_file_selector, 1, 8, 1, 1)
        # ##
        # widget_main_layout.addLayout(input_file_layout)

        # self.same_out_file_radio_button = QRadioButton("Output file: same as input file")
        # self.same_out_file_radio_button.setChecked(True)
        # self.new_out_file_radio_button = QRadioButton("Output file: select file")
        # self.same_out_file_radio_button.setChecked(False)
        #
        # self.radio_button_group = QButtonGroup()
        #
        # self.radio_button_group.addButton(self.same_out_file_radio_button)
        # self.radio_button_group.addButton(self.new_out_file_radio_button)
        #
        # layout_RadioButton = QVBoxLayout()
        #
        # layout_RadioButton.addWidget(self.same_out_file_radio_button)
        # layout_RadioButton.addWidget(self.new_out_file_radio_button)
        #
        # widget_main_layout.addLayout(layout_RadioButton)

        # ############### OUTPUT FILE  ###############
        # output_file_layout = QGridLayout()
        # #
        # output_file_description_label = QLabel(self)
        # output_file_description_label.setText("Output file :")
        #
        # output_file_description_label.setAlignment(Qt.AlignLeft)
        # output_file_layout.addWidget(output_file_description_label, 0, 0)
        #
        # #
        # self.output_file_path_label = QLabel(self)
        # self.output_file_path_label.hide()
        # self.output_file_path_label.setFrameStyle(QFrame.Panel | QFrame.Sunken)
        # self.output_file_path_label.setText("-")
        # self.output_file_path_label.setAlignment(Qt.AlignLeft)
        # output_file_layout.addWidget(self.output_file_path_label, 1, 0, 1, 8)
        # #
        # btn_output_file_selector = QPushButton("Add ")
        # btn_output_file_selector.setIcon(QIcon(resource_path('folder-icon.jpg')))
        # btn_output_file_selector.pressed.connect(self.saveFileDialog)
        # output_file_layout.addWidget(btn_output_file_selector, 1, 8, 1, 1)
        # ##
        # widget_main_layout.addLayout(output_file_layout)

        ############### START CONVERSION ###############
        # exec_row_layout = QHBoxLayout()
        # # exec_row_layout.addStretch()
        # btn_exec_convertion_to_mdf = QPushButton("Execute convertion")
        # btn_exec_convertion_to_mdf.setIcon(QIcon(resource_path('execute-icon.jpg')))
        # btn_exec_convertion_to_mdf.pressed.connect(self.btn_exec_convertion_to_mdf)
        # exec_row_layout.addWidget(btn_exec_convertion_to_mdf)
        #
        # exec_row_layout.addStretch()
        # widget_main_layout.addLayout(exec_row_layout)

        ############### EXPORT LABEL ###############
        # export_title_label = QLabel(self)
        # export_title_label.setFrameStyle(QFrame.Sunken)
        # export_title_label.setAlignment(Qt.AlignCenter)
        # export_title_label.setText("Export from MDF")
        # export_title_label.setStyleSheet('background-color: rgb(255,140,0)')
        #
        # widget_main_layout.addWidget(export_title_label)


        ############### SELECTION BOX FILE  ###############
        # Create a Vertical Layout
        comboBox_VLayout = QVBoxLayout()

        # Introduction label
        self.selection_label = QLabel("Select the input file:")

        # Create a ComboBox
        self.input_file_combobox = QComboBox()
        self.input_file_combobox.addItems(GUI_Configuration.CSV_conversion_GUI_selection_list)

        # Layout and main widget
        comboBox_VLayout.addWidget(self.selection_label)
        comboBox_VLayout.addWidget(self.input_file_combobox)
        widget_main_layout.addLayout(comboBox_VLayout)

        ############### INPUT FILE ###############
        input_file_layout = QGridLayout()
        #
        input_file_description_label = QLabel(self)
        input_file_description_label.setText("Input File :")
        input_file_description_label.setAlignment(Qt.AlignLeft)
        input_file_layout.addWidget(input_file_description_label, 0, 0)
        #
        self.input_file_path_label = QLabel(self)
        self.input_file_path_label.setFrameStyle(QFrame.Panel | QFrame.Sunken)
        self.input_file_path_label.setText("-")
        self.input_file_path_label.setAlignment(Qt.AlignLeft)
        input_file_layout.addWidget(self.input_file_path_label, 1, 0, 1, 8)
        #
        btn_input_file_selector = QPushButton("Add ")
        btn_input_file_selector.setIcon(QIcon(resource_path("excel.png")))
        # btn_input_file_selector.setToolTip("<b>HTML</b> <i>can</i> be shown too..")
        btn_input_file_selector.pressed.connect(self.open_input_file_dialog)
        input_file_layout.addWidget(btn_input_file_selector, 1, 8, 1, 1)
        ##
        widget_main_layout.addLayout(input_file_layout)

        ############### START CONVERSION ###############
        export_btn_layout = QHBoxLayout()
        # exec_row_layout.addStretch()
        export_to_csv_button = QPushButton("Convert to .CSV")
        export_to_csv_button.setIcon(QIcon(resource_path('execute-icon.jpg')))
        export_to_csv_button.pressed.connect(self.btn_exec_export_to_csv)
        export_btn_layout.addWidget(export_to_csv_button)
        export_btn_layout.addStretch()
        widget_main_layout.addLayout(export_btn_layout)
        widget_main_layout.addStretch()

        ############### SET MAIN LAYOUT
        self.setLayout(widget_main_layout)
        ############### GUI END

        ############### LOAD DATA ######################
        self.cfg_data = cfg_data
        self.cfg_data.load_cfg_data_from_file()

        self.input_file_combobox.setCurrentText(self.cfg_data.csv_conversion_input_file_combobox)
        self.input_file_path_label.setText('<br>'.join(self.cfg_data.csv_conversion_input_file_list))

        self.dewesoft_converter = Dewesoft_to_CSV()

        #self.csv_to_mdf_handler = CSV_to_MDF_Handler()
        #self.bertrandt_to_mdf_handler = Bertrandt_to_MDF_Handler()
        #self.pumplogger_to_mdf = PumpLogger_to_MDF()
        #self.dielectrik_to_mdf = DielectriK_to_MDF()
        #self.vector_to_mdf = Vector_to_MDF()

    def btn_exec_export_to_csv(self):
        print("btn_exec_export_to_csv")

        Dewesoft_to_CSV.exec_conversion(input_file_list=self.cfg_data.csv_conversion_input_file_list,
                                        use_same_input_file_name=True,
                                        output_file_name="")

    def open_input_file_dialog(self):
        file_dialog = QFileDialog()
        possible_filters, selected_filter = GUI_Configuration.CSV_conversion_select_filter_for_file(
            self.input_file_combobox.currentText())
        # print(possible_filters, selected_filter)

        if len(self.cfg_data.csv_conversion_input_file_list) == 0:
            base_filename = ""
        else:
            base_filename = self.cfg_data.csv_conversion_input_file_list[0]
        fileNameList, _ = file_dialog.getOpenFileNames(self, caption="Select input file",
                                                       dir=os.path.dirname(base_filename),
                                                       filter=";;".join(possible_filters),
                                                       selectedFilter=selected_filter)

        if len(fileNameList) == 0:
            print(f"fileNameList empty : {fileNameList}")
        else:
            self.cfg_data.csv_conversion_input_file_combobox = self.input_file_combobox.currentText()
            self.cfg_data.csv_conversion_input_file_list = fileNameList
            self.input_file_path_label.setText("<br>".join(self.cfg_data.csv_conversion_input_file_list))
            self.cfg_data.save_cfg_data_to_file()

    def save_file_dialog(self):
        fileName, _ = QFileDialog.getSaveFileName(self, "Select output file", "",
                                                  "MDF file (*.mf4)")  # , options=options)
        if fileName:
            # print(fileName)
            self.cfg_data.mdf_conversion_output_file_path = fileName
            self.output_file_path_label.setText(self.cfg_data.mdf_conversion_output_file_path)
            self.cfg_data.save_cfg_data_to_file()
