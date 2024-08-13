from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QMessageBox, QLabel, QFrame, QGridLayout, \
    QLineEdit, QFileDialog
from Classes.CSV_to_MDF_Handler import CSV_to_MDF_Handler
from Classes.Configuration_Data import CSV_to_MDF_Configuration_Data
from icons.resources import resource_path


class CSV_to_MDF_Widget(QWidget):
    def __init__(self, csv_to_mdf_cfg_data):

        super().__init__()
        widget_main_layout = QVBoxLayout()
        ############### TITLE LABEL ###############
        title_label = QLabel(self)
        title_label.setFrameStyle(QFrame.Sunken)
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setText("CSV to MDF conversion")
        title_label.setStyleSheet('background-color: rgb(255,140,0)')

        widget_main_layout.addWidget(title_label)
        ############### INPUT FILE [.TXT] ###############
        input_file_layout = QGridLayout()
        #
        input_file_description_label = QLabel(self)
        input_file_description_label.setText("Input file :")
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
        #btn_input_file_selector.setToolTip("<b>HTML</b> <i>can</i> be shown too..")
        btn_input_file_selector.pressed.connect(self.openInputFileDialog)
        input_file_layout.addWidget(btn_input_file_selector, 1, 8, 1, 1)
        ##
        widget_main_layout.addLayout(input_file_layout)
        ############### INPUT SHEET  ###############
        input_file_sheet_layout = QGridLayout()
        #
        input_file_sheet_label = QLabel(self)
        input_file_sheet_label.setText("Input sheet :")
        input_file_sheet_label.setAlignment(Qt.AlignLeft)
        input_file_sheet_layout.addWidget(input_file_sheet_label, 0, 0)
        self.input_sheet_line_edit = QLineEdit()
        input_file_sheet_layout.addWidget(self.input_sheet_line_edit, 1, 0, 1, 8)
        #
        widget_main_layout.addLayout(input_file_sheet_layout)
        ############### FIND & REPLACE FILE PATH  ###############
        fr_file_layout = QGridLayout()
        #
        fr_file_label = QLabel(self)
        fr_file_label.setText("Find & Replace file :")
        fr_file_label.setAlignment(Qt.AlignLeft)
        fr_file_layout.addWidget(fr_file_label, 0, 0)
        #
        self.fr_file_path_label = QLabel(self)
        self.fr_file_path_label.setFrameStyle(QFrame.Panel | QFrame.Sunken)
        self.fr_file_path_label.setText("-")
        self.fr_file_path_label.setAlignment(Qt.AlignLeft)
        fr_file_layout.addWidget(self.fr_file_path_label, 1, 0, 1, 8)
        #
        btn_fr_file_selector = QPushButton("Add ")
        btn_fr_file_selector.setIcon(QIcon(resource_path("folder-icon.jpg")))
        btn_fr_file_selector.pressed.connect(self.openFindReplaceFileDialog)
        fr_file_layout.addWidget(btn_fr_file_selector, 1, 8, 1, 1)
        ##
        widget_main_layout.addLayout(fr_file_layout)
        ############### FIND & REPLACE FILE SHEET  ###############
        fr_file_sheet_layout = QGridLayout()
        #
        fr_file_sheet_label = QLabel(self)
        fr_file_sheet_label.setText("Find & Replace sheet :")
        fr_file_sheet_label.setAlignment(Qt.AlignLeft)
        fr_file_sheet_layout.addWidget(fr_file_sheet_label, 0, 0)
        self.fr_sheet_line_edit = QLineEdit()
        fr_file_sheet_layout.addWidget(self.fr_sheet_line_edit, 1, 0, 1, 8)
        #
        widget_main_layout.addLayout(fr_file_sheet_layout)
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
        ############### START SUBSTITUTION ###############
        exec_row_layout = QHBoxLayout()
        exec_row_layout.addStretch()
        btn_exec_tc_substitution = QPushButton("Execute substitution")
        btn_exec_tc_substitution.setIcon(QIcon(resource_path('execute-icon.jpg')))
        btn_exec_tc_substitution.pressed.connect(self.tc_substitution_exec_conversion)
        exec_row_layout.addWidget(btn_exec_tc_substitution)

        ############### START CLEANING EMPTY_ROW ###############
        btn_exec_tc_cleanup = QPushButton("Execute Cleanup")
        btn_exec_tc_cleanup.setIcon(QIcon(resource_path('cleanup-icon-small.jpg')))
        btn_exec_tc_cleanup.pressed.connect(self.tc_substitution_exec_cleanup)
        exec_row_layout.addWidget(btn_exec_tc_cleanup)

        ############### START CLEANING EMPTY_ROW ###############
        btn_exec_tc_bullet_fix = QPushButton("Execute Bullet Fix")
        btn_exec_tc_bullet_fix.setIcon(QIcon(resource_path('bullet_list.png')))
        btn_exec_tc_bullet_fix.pressed.connect(self.tc_substitution_fix_bullet_list)
        exec_row_layout.addWidget(btn_exec_tc_bullet_fix)

        ############### START POLARION TO EXCEL ###############
        btn_exec_pol_to_xls = QPushButton("Polarion to Excel")
        btn_exec_pol_to_xls.setIcon(QIcon(resource_path('excel.png')))
        btn_exec_pol_to_xls.pressed.connect(self.tc_conversion_polarion_to_excel)
        exec_row_layout.addWidget(btn_exec_pol_to_xls)

        ############### START EXCEL TO POLARION ###############
        btn_exec_pol_to_xls = QPushButton("Excel to Polarion")
        btn_exec_pol_to_xls.setIcon(QIcon(resource_path('polarion.png')))
        btn_exec_pol_to_xls.pressed.connect(self.tc_conversion_excel_to_polarion)
        exec_row_layout.addWidget(btn_exec_pol_to_xls)

        exec_row_layout.addStretch()

        widget_main_layout.addLayout(exec_row_layout)
        ############### SET MAIN LAYOUT
        self.setLayout(widget_main_layout)
        ############### GUI END

        if not isinstance(csv_to_mdf_cfg_data, CSV_to_MDF_Configuration_Data):
            print("CSV_to_MDF_Widget::init() - wrong input type")
            exit()
        else:
            self.csv_to_mdf_handler = CSV_to_MDF_Handler(csv_to_mdf_cfg_data)
            self.update_cfg_data_gui()

    def update_handler(self, csv_to_mdf_data):
        #self.csv_to_mdf_handler = CSV_to_MDF_Handler()
        self.update_cfg_data_gui()

    def update_cfg_data_gui(self):
        #in_file_path, in_file_sheet, fr_file_path, fr_file_sheet, out_file_path = \
        #    csv_to_mdf_handler.parse_json_path_file(json_data)

        #self.csv_to_mdf_handler.input_file_path = in_file_path
        self.input_file_path_label.setText(self.csv_to_mdf_handler.cfg_data.input_file_path)

        #self.csv_to_mdf_handler.input_file_sheet = in_file_sheet
        self.input_sheet_line_edit.setText(self.csv_to_mdf_handler.cfg_data.input_file_sheet)

        #self.csv_to_mdf_handler.find_replace_file_path = fr_file_path
        self.fr_file_path_label.setText(self.csv_to_mdf_handler.cfg_data.find_replace_file_path)

        #self.csv_to_mdf_handler.find_replace_file_sheet = fr_file_sheet
        self.fr_sheet_line_edit.setText(self.csv_to_mdf_handler.cfg_data.find_replace_file_sheet)

        #self.csv_to_mdf_handler.output_file_path = out_file_path
        self.output_file_path_label.setText(self.csv_to_mdf_handler.cfg_data.output_file_path)

    def tc_substitution_exec_conversion(self):
        self.csv_to_mdf_handler.cfg_data.set_in_file_sheet(self.input_sheet_line_edit.text())
        self.csv_to_mdf_handler.cfg_data.set_fr_file_sheet(self.fr_sheet_line_edit.text())

        self.csv_to_mdf_handler.exec_substitution()

    def tc_substitution_exec_cleanup(self):
        self.csv_to_mdf_handler.cfg_data.set_in_file_sheet(self.input_sheet_line_edit.text())

        self.csv_to_mdf_handler.exec_cleanup()

    def tc_substitution_fix_bullet_list(self):
        self.csv_to_mdf_handler.cfg_data.set_in_file_sheet(self.input_sheet_line_edit.text())

        self.csv_to_mdf_handler.exec_bullet_lists_fix()

    def tc_conversion_polarion_to_excel(self):
        self.csv_to_mdf_handler.cfg_data.set_in_file_sheet(self.input_sheet_line_edit.text())

        self.csv_to_mdf_handler.exec_polarion_to_excel_converter()


    def tc_conversion_excel_to_polarion(self):
        self.csv_to_mdf_handler.cfg_data.set_in_file_sheet(self.input_sheet_line_edit.text())

        self.csv_to_mdf_handler.exec_excel_to_polarion_converter()

    def openInputFileDialog(self):
        fileName, _ = QFileDialog.getOpenFileName(self, "Select input CSV file", "",
                                                  "Excel Files (*.txt)")  # , options=options)
        if fileName:
            # print(fileName)
            self.csv_to_mdf_handler.cfg_data.set_in_file_path(fileName)
            self.update_cfg_data_gui()

    def openFindReplaceFileDialog(self):
        # options = QFileDialog.Options()
        # options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self, "Select Find & Replace xlsx file", "",
                                                  "Excel Files (*.xlsx)")  # , options=options)
        if fileName:
            # print(fileName)
            self.csv_to_mdf_handler.cfg_data.set_fr_file_path(fileName)
            self.update_cfg_data_gui()

    def saveFileDialog(self):
        fileName, _ = QFileDialog.getSaveFileName(self, "Select output file", "",
                                                  "Excel Files (*.xlsx)")  # , options=options)
        if fileName:
            # print(fileName)
            self.csv_to_mdf_handler.cfg_data.set_out_file_path(fileName)
            self.update_cfg_data_gui()