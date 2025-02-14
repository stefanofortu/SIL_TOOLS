import os.path

from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QMessageBox, QLabel, QFrame, QGridLayout, \
    QLineEdit, QFileDialog, QComboBox, QRadioButton, QButtonGroup
from pandas import to_timedelta

from Classes.CSV_to_MDF_Handler import CSV_to_MDF_Handler
from Classes.Bertrandt_to_MDF import Bertrandt_to_MDF_Handler
from Classes.Dataframe_to_MDF import Dataframe_to_MDF
from Classes.DielectriK_to_MDF import DielectriK_to_MDF
from Classes.PumpLogger_to_MDF import PumpLogger_to_MDF
from Classes.Configuration_Data import Configuration_Data
from icons.resources import resource_path


class Main_Widget(QWidget):

    def __init__(self, cfg_data):
        super().__init__()

        if not isinstance(cfg_data, Configuration_Data):
            print("cfg_data not Configuration_Data");
            exit()

        widget_main_layout = QVBoxLayout()
        ############### TITLE LABEL ###############
        conversion_title_label = QLabel(self)
        conversion_title_label.setFrameStyle(QFrame.Sunken)
        conversion_title_label.setAlignment(Qt.AlignCenter)
        conversion_title_label.setText("Conversion to MDF")
        conversion_title_label.setStyleSheet('background-color: rgb(255,140,0)')

        widget_main_layout.addWidget(conversion_title_label)

        ############### SELECTION BOX FILE  ###############
        # Create a Vertical Layout
        comboBox_VLayout = QVBoxLayout()

        # Introduction label
        self.selection_label = QLabel("Select an option:")

        # Create a ComboBox
        self.selection_comboBox = QComboBox()
        self.selection_comboBox.addItems(["EDAG", "Bertrandt", "PumpLogger", "Dielectrik"])

        # Layout and main widget
        comboBox_VLayout.addWidget(self.selection_label)
        comboBox_VLayout.addWidget(self.selection_comboBox)
        widget_main_layout.addLayout(comboBox_VLayout)

        ############### INPUT FILE ###############
        input_file_layout = QGridLayout()
        #
        input_file_description_label = QLabel(self)
        input_file_description_label.setText("Input CSV file :")
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
        btn_input_file_selector.setIcon(QIcon(resource_path("folder-icon.jpg")))
        # btn_input_file_selector.setToolTip("<b>HTML</b> <i>can</i> be shown too..")
        btn_input_file_selector.pressed.connect(self.open_input_file_dialog)
        input_file_layout.addWidget(btn_input_file_selector, 1, 8, 1, 1)
        ##
        widget_main_layout.addLayout(input_file_layout)

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
        self.output_file_path_label = QLabel(self)
        self.output_file_path_label.hide()
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
        exec_row_layout = QHBoxLayout()
        # exec_row_layout.addStretch()
        btn_exec_convertion_to_mdf = QPushButton("Execute convertion")
        btn_exec_convertion_to_mdf.setIcon(QIcon(resource_path('execute-icon.jpg')))
        btn_exec_convertion_to_mdf.pressed.connect(self.btn_exec_convertion_to_mdf)
        exec_row_layout.addWidget(btn_exec_convertion_to_mdf)

        exec_row_layout.addStretch()
        widget_main_layout.addLayout(exec_row_layout)

        ############### EXPORT LABEL ###############
        export_title_label = QLabel(self)
        export_title_label.setFrameStyle(QFrame.Sunken)
        export_title_label.setAlignment(Qt.AlignCenter)
        export_title_label.setText("Export from MDF")
        export_title_label.setStyleSheet('background-color: rgb(255,140,0)')

        widget_main_layout.addWidget(export_title_label)

        ############### MDF INPUT FILE ###############
        input_mdf_file_layout = QGridLayout()
        #
        input_mdf_file_description_label = QLabel(self)
        input_mdf_file_description_label.setText("Input MDF file :")
        input_mdf_file_description_label.setAlignment(Qt.AlignLeft)
        input_mdf_file_layout.addWidget(input_mdf_file_description_label, 0, 0)
        #
        self.input_mdf_file_path_label = QLabel(self)
        self.input_mdf_file_path_label.setFrameStyle(QFrame.Panel | QFrame.Sunken)
        self.input_mdf_file_path_label.setText("-")
        self.input_mdf_file_path_label.setAlignment(Qt.AlignLeft)
        input_mdf_file_layout.addWidget(self.input_mdf_file_path_label, 1, 0, 1, 8)
        #
        btn_input_mdf_file_selector = QPushButton("Add ")
        btn_input_mdf_file_selector.setIcon(QIcon(resource_path("folder-icon.jpg")))
        # btn_input_file_selector.setToolTip("<b>HTML</b> <i>can</i> be shown too..")
        btn_input_mdf_file_selector.pressed.connect(self.open_mdf_input_file_dialog)
        input_mdf_file_layout.addWidget(btn_input_mdf_file_selector, 1, 8, 1, 1)
        ##
        widget_main_layout.addLayout(input_mdf_file_layout)

        ############### START CONVERSION ###############
        export_btn_layout = QHBoxLayout()
        # exec_row_layout.addStretch()
        export_to_mdf_button = QPushButton("EXPORT")
        export_to_mdf_button.setIcon(QIcon(resource_path('execute-icon.jpg')))
        export_to_mdf_button.pressed.connect(self.btn_exec_export_to_csv)
        export_btn_layout.addWidget(export_to_mdf_button)
        export_btn_layout.addStretch()
        widget_main_layout.addLayout(export_btn_layout)

        ############### SET MAIN LAYOUT
        self.setLayout(widget_main_layout)
        ############### GUI END

        ############### LOAD DATA ######################
        self.cfg_data = cfg_data
        self.cfg_data.load_cfg_data_from_file()

        self.input_file_path_label.setText(self.cfg_data.mdf_conversion_input_file_path)
        #self.output_file_path_label.setText(self.cfg_data.mdf_conversion_output_file_path)
        self.input_mdf_file_path_label.setText(self.cfg_data.mdf_export_input_file_path)

        self.csv_to_mdf_handler = CSV_to_MDF_Handler()
        self.bertrandt_to_mdf_handler = Bertrandt_to_MDF_Handler()
        self.pumplogger_to_mdf = PumpLogger_to_MDF()
        self.dielectrik_to_mdf = DielectriK_to_MDF()

    def btn_exec_export_to_csv(self):
        df, start_time = Dataframe_to_MDF.load_from_mdf(self.cfg_data.mdf_export_input_file_path)
        # Create a new column by adding the relative seconds as a timedelta to the base time
        df.insert(0, "Time", start_time + to_timedelta(df['Time[s]'], unit='s'))
        print(df.columns)
        df.drop(columns=["Press_In(bar)", "Press_Out.(bar)", "LV_Ipump (A)", "EV_glicole(%)",
                         "Press_In(bar) .1", "Press_Out(bar)"], inplace=True)
        df.rename(columns={"Delta P(bar)": "DeltaP", "Flow(l/min)": "Q",
                           "LV_Vpump (V)": "Tcoolant", "HV_Vpump(V)": "Vpump", "HV_Ipump(A)": "Ipump"}, inplace=True)
        df['Time'] = (df['Time'].dt.strftime('%d/%m/%Y %H:%M:%S.%f'))
        output_file_name = ""
        parts = self.cfg_data.mdf_export_input_file_path.split(".")
        if len(parts) > 1:
            output_file_name = (".".join(parts[:-1])) + ".csv"
            print("output_file_name: ", output_file_name)
        else:
            print("input_file_path has no extension")
            exit()

        df.to_csv(output_file_name, index=False)
        print("csv salvato")

    def btn_exec_convertion_to_mdf(self):
        use_same_name = True
        # if self.same_out_file_radio_button.isChecked() ^ self.new_out_file_radio_button.isChecked():
        #     if self.same_out_file_radio_button.isChecked() == True:
        #         use_same_name = True
        #     if self.new_out_file_radio_button.isChecked() == True:
        #         use_same_name = False
        # else:
        #     print("Radio Button Error")
        #     exit()

        if self.selection_comboBox.currentText() == "EDAG":
            self.csv_to_mdf_handler.exec_substitution(self.cfg_data.mdf_conversion_input_file_path,
                                                      use_same_name,
                                                      self.cfg_data.mdf_conversion_output_file_path)
        elif self.selection_comboBox.currentText() == "Bertrandt":
            self.bertrandt_to_mdf_handler.exec_conversion(self.cfg_data.mdf_conversion_input_file_path,
                                                          use_same_name,
                                                          self.cfg_data.mdf_conversion_output_file_path)
        elif self.selection_comboBox.currentText() == "PumpLogger":
            self.pumplogger_to_mdf.exec_conversion(self.cfg_data.mdf_conversion_input_file_path,
                                                   use_same_name,
                                                   self.cfg_data.mdf_conversion_output_file_path)
        elif self.selection_comboBox.currentText() == "Dielectrik":
            self.dielectrik_to_mdf.exec_conversion(self.cfg_data.mdf_conversion_input_file_path,
                                                   use_same_name,
                                                   self.cfg_data.mdf_conversion_output_file_path)
        else:
            print("Wrong selection in selection_comboBox")

    def open_input_file_dialog(self):
        file_dialog = QFileDialog()
        # file_dialog.setDirectory(os.path.dirname(self.cfg_data.input_file_path))
        possible_filters = ["Text Files (*.txt)", "CSV Files (*.csv)", "Python Files (*.py)",
                            "PumpLogger_data (*.data)", "All Files (*)"]

        if self.selection_comboBox.currentText() == "EDAG":
            selected_filter = possible_filters[0]  # .csv
        elif self.selection_comboBox.currentText() == "Bertrandt":
            selected_filter = possible_filters[1]
        elif self.selection_comboBox.currentText() == "PumpLogger":
            selected_filter = possible_filters[3]  # .csv
        elif self.selection_comboBox.currentText() == "Dielectrik":
            selected_filter = possible_filters[0]  # .txt
        else:
            print("Wrong selection in selection_comboBox")

        fileName, _ = file_dialog.getOpenFileName(self, caption="Select input CSV file",
                                                  dir=os.path.dirname(self.cfg_data.mdf_conversion_input_file_path),
                                                  filter=";;".join(possible_filters),
                                                  selectedFilter=selected_filter)

        if fileName:
            self.cfg_data.mdf_conversion_input_file_path = fileName
            self.input_file_path_label.setText(self.cfg_data.mdf_conversion_input_file_path)
            self.cfg_data.save_cfg_data_to_file()

    def open_mdf_input_file_dialog(self):
        file_dialog = QFileDialog()

        possible_filters = ["MDF Files (*.mf4)", "All Files (*)"]
        selected_filter = possible_filters[0]  # .m4f

        filename, _ = file_dialog.getOpenFileName(self, caption="Select input MDF file",
                                                  dir=os.path.dirname(self.cfg_data.mdf_conversion_input_file_path),
                                                  filter=";;".join(possible_filters),
                                                  selectedFilter=selected_filter)

        if filename:
            self.cfg_data.mdf_export_input_file_path = filename
            self.input_mdf_file_path_label.setText(self.cfg_data.mdf_export_input_file_path)
            self.cfg_data.save_cfg_data_to_file()

    def save_file_dialog(self):
        fileName, _ = QFileDialog.getSaveFileName(self, "Select output file", "",
                                                  "MDF file (*.mf4)")  # , options=options)
        if fileName:
            # print(fileName)
            self.cfg_data.mdf_conversion_output_file_path = fileName
            self.output_file_path_label.setText(self.cfg_data.mdf_conversion_output_file_path)
            self.cfg_data.save_cfg_data_to_file()
