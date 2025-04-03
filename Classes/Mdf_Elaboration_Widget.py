import os.path

from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QFrame, QGridLayout, \
    QFileDialog, QCheckBox, QSpinBox, QLineEdit
from Classes.Mdf_Elaboration_Handler import Mdf_Elaboration_Handler
from Classes.Configuration_Data import Configuration_Data
from icons.resources import resource_path


class Mdf_Elaboration_Widget(QWidget):

    def tc_substitution_exec_elaboration(self):
        df, start_time = self.mdf_elaboration.load_from_mdf(self.cfg_data.mdf_elaboration_input_file_path)

        if self.adding_read_checkbox.isChecked():
            self.mdf_elaboration.insert_read(df,
                                             read_start_time=self.read_delay_spin_box.value(),
                                             read_waiting_time=self.read_waiting_time_spin_box.value(),
                                             read_high_time=self.read_high_time_spin_box.value(),
                                             read_numbers=self.read_repetitions_spin_box.value())

        if self.adding_read_threshold_checkbox.isChecked():
            self.mdf_elaboration.insert_read_by_threshold(df,
                                                          signal_name=self.read_by_threshold_signal_name.text(),
                                                          threshold=self.read_by_threshold_value_label_spin_box.value())

        self.mdf_elaboration.save_to_mdf(df, self.cfg_data.mdf_elaboration_output_file_path)

    def openInputFileDialog(self):
        file_dialog = QFileDialog()

        possible_filters = ["MDF Files (*.mf4)", "All Files (*)"]
        selected_filter = possible_filters[0]  # .m4f

        filename, _ = file_dialog.getOpenFileName(self, caption="Select input MDF file",
                                                  dir=os.path.dirname(self.cfg_data.mdf_conversion_input_file_path),
                                                  filter=";;".join(possible_filters),
                                                  selectedFilter=selected_filter)

        if filename:
            self.cfg_data.mdf_elaboration_input_file_path = filename
            self.input_file_path_label.setText(self.cfg_data.mdf_elaboration_input_file_path)
            self.cfg_data.save_cfg_data_to_file()

    def saveFileDialog(self):
        fileName, _ = QFileDialog.getSaveFileName(self, "Select output file", "",
                                                  "MDF file (*.mf4)")  # , options=options)
        if fileName:
            print(fileName)
            self.cfg_data.mdf_elaboration_output_file_path = fileName
            self.output_file_path_label.setText(self.cfg_data.mdf_elaboration_output_file_path)
            self.save_ui_to_cfg_data()

    def save_ui_to_cfg_data(self):
        self.cfg_data.mdf_elaboration_input_file_path = self.input_file_path_label.text()
        self.cfg_data.mdf_elaboration_output_file_path = self.output_file_path_label.text()
        self.cfg_data.mdf_elaboration_insert_read_by_value_delay = 2
        self.cfg_data.mdf_elaboration_insert_read_by_value_waiting = 15
        self.cfg_data.mdf_elaboration_insert_read_by_value_time = 15
        self.cfg_data.mdf_elaboration_insert_read_by_value_repetitions = 15
        self.cfg_data.mdf_elaboration_insert_read_by_threshold_signal_name = "hello"
        self.cfg_data.mdf_elaboration_insert_read_by_threshold_value = 1
        self.cfg_data.save_cfg_data_to_file()

    def __init__(self, cfg_data):
        super().__init__()

        if not isinstance(cfg_data, Configuration_Data):
            print("cfg_data not Configuration_Data");
            exit()

        widget_main_layout = QVBoxLayout()
        ############### TITLE LABEL ###############
        title_label = QLabel(self)
        title_label.setFrameStyle(QFrame.Sunken)
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setText("MDF_Elaboration_Widget")
        title_label.setStyleSheet('background-color: rgb(255,140,0)')

        widget_main_layout.addWidget(title_label)

        ############### INPUT FILE [.TXT] ###############
        input_file_layout = QGridLayout()
        #
        input_file_description_label = QLabel(self)
        input_file_description_label.setText("Input MDF file :")
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
        btn_input_file_selector.pressed.connect(self.openInputFileDialog)
        input_file_layout.addWidget(btn_input_file_selector, 1, 8, 1, 1)
        ##
        widget_main_layout.addLayout(input_file_layout)
        widget_main_layout.addStretch()
        ######### INSERT READ BY VALUE #############################
        insert_read_by_value_layout = QHBoxLayout()

        # Create a checkbox
        self.adding_read_checkbox = QCheckBox("Insert read by value", self)
        # self.checkbox.stateChanged.connect(self.on_checkbox_changed)

        # Create a label to display checkbox state
        self.read_delay_label = QLabel("Delay from start [s]", self)
        self.read_delay_spin_box = QSpinBox(self)
        self.read_delay_spin_box.setRange(0, 1000)  # Set the range of values (min, max)
        self.read_delay_spin_box.setValue(0)
        #self.read_delay_spin_box.valueChanged.connect()

        self.read_waiting_time_label = QLabel("Waiting Time [s]", self)
        self.read_waiting_time_spin_box = QSpinBox(self)
        self.read_waiting_time_spin_box.setRange(0, 600)  # Set the range of values (min, max)
        self.read_waiting_time_spin_box.setValue(30)

        self.read_high_time_label = QLabel("Read Time[s]", self)
        self.read_high_time_spin_box = QSpinBox(self)
        self.read_high_time_spin_box.setRange(0, 60)  # Set the range of values (min, max)
        self.read_high_time_spin_box.setValue(5)

        self.read_repetitions_label = QLabel("Read Repetitions[num]", self)
        self.read_repetitions_spin_box = QSpinBox(self)
        self.read_repetitions_spin_box.setRange(0, 60)  # Set the range of values (min, max)
        self.read_repetitions_spin_box.setValue(10)

        # Add widgets to layout
        insert_read_by_value_layout.addWidget(self.adding_read_checkbox)

        insert_read_by_value_layout.addWidget(self.read_delay_label)
        insert_read_by_value_layout.addWidget(self.read_delay_spin_box)
        insert_read_by_value_layout.addWidget(self.read_waiting_time_label)
        insert_read_by_value_layout.addWidget(self.read_waiting_time_spin_box)
        insert_read_by_value_layout.addWidget(self.read_high_time_label)
        insert_read_by_value_layout.addWidget(self.read_high_time_spin_box)
        insert_read_by_value_layout.addWidget(self.read_repetitions_label)
        insert_read_by_value_layout.addWidget(self.read_repetitions_spin_box)

        widget_main_layout.addLayout(insert_read_by_value_layout)
        widget_main_layout.addStretch()

        ######### INSERT READ BY THRESHOLD #############################
        insert_read_by_threshold_layout = QHBoxLayout()

        # Create a checkbox
        self.adding_read_threshold_checkbox = QCheckBox("Insert read by threshold", self)
        # self.checkbox.stateChanged.connect(self.on_checkbox_changed)

        # Create a label to display checkbox state
        self.read_by_threshold_label = QLabel("Name of the reference signal", self)
        self.read_by_threshold_signal_name = QLineEdit()
        self.read_by_threshold_signal_name.setText("Time[s]")  # Set the range of values (min, max)

        self.read_by_threshold_value_label = QLabel("Threshold value", self)
        self.read_by_threshold_value_label_spin_box = QSpinBox(self)
        self.read_by_threshold_value_label_spin_box.setRange(0, 10000)  # Set the range of values (min, max)
        self.read_by_threshold_value_label_spin_box.setValue(5)

        # Add widgets to layout
        insert_read_by_threshold_layout.addWidget(self.adding_read_threshold_checkbox)
        insert_read_by_threshold_layout.addWidget(self.read_by_threshold_label)
        insert_read_by_threshold_layout.addWidget(self.read_by_threshold_signal_name)
        insert_read_by_threshold_layout.addWidget(self.read_by_threshold_value_label)
        insert_read_by_threshold_layout.addWidget(self.read_by_threshold_value_label_spin_box)

        widget_main_layout.addLayout(insert_read_by_threshold_layout)
        widget_main_layout.addStretch()

        ############### OUTPUT FILE  ###############
        output_file_layout = QGridLayout()
        #
        output_file_description_label = QLabel(self)
        output_file_description_label.setText("Output file :")

        output_file_description_label.setAlignment(Qt.AlignLeft)
        output_file_layout.addWidget(output_file_description_label, 0, 0)

        #
        self.output_file_path_label = QLabel(self)
        self.output_file_path_label.setFrameStyle(QFrame.Panel | QFrame.Sunken)
        self.output_file_path_label.setText("-")
        self.output_file_path_label.setAlignment(Qt.AlignLeft)
        output_file_layout.addWidget(self.output_file_path_label, 1, 0, 1, 8)
        #
        btn_output_file_selector = QPushButton("Add ")
        btn_output_file_selector.setIcon(QIcon(resource_path('folder-icon.jpg')))
        btn_output_file_selector.pressed.connect(self.saveFileDialog)
        output_file_layout.addWidget(btn_output_file_selector, 1, 8, 1, 1)
        ##
        widget_main_layout.addLayout(output_file_layout)
        widget_main_layout.addStretch()

        ############### START SUBSTITUTION ###############
        exec_row_layout = QHBoxLayout()
        # exec_row_layout.addStretch()
        btn_exec_tc_substitution = QPushButton("Execute Processing")
        btn_exec_tc_substitution.setIcon(QIcon(resource_path('execute-icon.jpg')))
        btn_exec_tc_substitution.pressed.connect(self.tc_substitution_exec_elaboration)
        exec_row_layout.addWidget(btn_exec_tc_substitution)

        exec_row_layout.addStretch()
        widget_main_layout.addLayout(exec_row_layout)

        ############### SET MAIN LAYOUT
        self.setLayout(widget_main_layout)
        ############### GUI END

        ############### LOAD DATA ######################
        self.cfg_data = cfg_data
        self.cfg_data.load_cfg_data_from_file()

        self.input_file_path_label.setText(self.cfg_data.mdf_elaboration_input_file_path)
        self.output_file_path_label.setText(self.cfg_data.mdf_elaboration_output_file_path)

        self.mdf_elaboration = Mdf_Elaboration_Handler()
