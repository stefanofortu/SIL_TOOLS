import json
import sys

from PySide6.QtWidgets import QWidget, QFileDialog

FILE_NAME_DEFAULT = "SIL_config_data.json"
class Configuration_Data: #CHANGE NAME TO FILE
    def __init__(self):
        self.configuration_file_name = FILE_NAME_DEFAULT
        csv_to_mdf_cfg_data = CSV_to_MDF_Configuration_Data()
        #self.hil_function_file_data = CSV_to_MDF_Configuration_Data()
        #self.tc_highlight_data = CSV_to_MDF_Configuration_Data()

    def load_cfg_data_from_file(self):
        try:
            with open(self.configuration_file_name, 'r') as json_file:
                json_file_no_comment = ''.join(line for line in json_file if not line.startswith('#'))
                file_dict = json.loads(json_file_no_comment)

                try:
                    CSV_to_MDF_cfg_data_dict = file_dict['root']['CSV_to_MDF']
                except KeyError:
                    print("Field 'CSV_to_MDF' in file " , self.configuration_file_name, "does not exist")
                    sys.exit()
                #try:
                #    CAN_highlighting_dict = file_dict['root']['CAN_highlighting']
                #except KeyError:
                #    print('Field CAN_highlighting in file %s does not exist', self.configuration_file_name)
                #    sys.exit()
                #try:
                #    CSV_to_MDF_cfg_data_dict = file_dict['root']['find_replace_multiple_row']
                #except KeyError:
                #    print('Field find_replace_multiple_row in file %s does not exist', self.configuration_file_name)
                #    sys.exit()


                csv_to_mdf_cfg_data = CSV_to_MDF_Configuration_Data(CSV_to_MDF_cfg_data_dict)
                hil_function_file_data = None  # HIL_Function_Configuration_Data(HIL_substitution_dict)
                tc_highlight_data = None  # TC_Highlight_Configuration_Data(CAN_highlighting_dict)

        except FileNotFoundError:
            print('File self.configuration_file_name does not exist')
            csv_to_mdf_cfg_data = CSV_to_MDF_Configuration_Data()
            hil_function_cfg_data = None
            tc_highlight_to_mdf_cfg_data = None
            self.save_cfg_data_to_file(csv_to_mdf_cfg_data, None, None,
                                       filename_default=True)

        return csv_to_mdf_cfg_data,hil_function_file_data, tc_highlight_data


    def save_cfg_data_to_file(self, csv_to_mdf_cfg_data,hil_function_file_data, tc_highlight_data,
                                filename_default=False, select_new_file=False):
        configuration_file_data = {
            "root": {
                "CSV_to_MDF": {},
                "CAN_highlighting": {},
                "find_replace_multiple_row": {}
            }
        }
        configuration_file_data['root']['CSV_to_MDF'] = csv_to_mdf_cfg_data.create_json_dict_from_data()
        # self.configuration_file_data['root']['CAN_highlighting'] = tc_highlight_data
        # self.configuration_file_data['root']['find_replace_multiple_row'] = tc_substitution_data

        # Serializing json
        json_object = json.dumps(configuration_file_data, indent=4)

        filename = None
        if filename_default:
            filename = FILE_NAME_DEFAULT
        else:
            if not select_new_file:
                filename = self.configuration_file_name
            else:
                filename, _ = QFileDialog.getSaveFileName(self, "Save configuration as ", "",
                                                          'JSON file (*.json)')  # , options=options)
                if filename is None:
                    print("Error in filename")
                else:
                    self.configuration_file_name = filename

        if filename:
            try:
                with open(filename, "w") as outfile:
                    outfile.write(json_object)
            except IOError:
                print("Error in writing files")




class HIL_Function_Configuration_Data:
    def __init__(self):
        self.function_verify_filename = ""
        self.function_verify_sheetName = ""
        self.build_filename = ""
        self.source_sheet = []
        self.run_file_path = ""

    def return_json_dict(self):
        dict = {}
        return dict


class TC_Highlight_Configuration_Data:
    def __init__(self):
        self.input_TC_file_path = ""
        self.input_TC_file_sheet_name = ""
        self.output_TC_file_path = ""

    def return_json_dict(self):
        dict = {}
        return dict


class CSV_to_MDF_Configuration_Data:
    def __init__(self, csv_to_mdf_dictionary=None):
        if csv_to_mdf_dictionary == None:
            self.input_file_path = ""
            self.input_file_sheet = ""
            self.find_replace_file_path = ""
            self.find_replace_file_sheet = ""
            self.output_file_path = ""
        else:
            self.create_data_from_json_dict(csv_to_mdf_dictionary)

    def create_json_dict_from_data(self):
        csv_to_mdf_dict = {
            "input_file": {
                "path": self.input_file_path,
                "sheet_name": self.input_file_sheet
            },
            "find_replace_file": {
                "path": self.find_replace_file_path,
                "sheet_name": self.find_replace_file_sheet
            },
            "output_file": {
                "path": self.output_file_path
            }
        }

        return csv_to_mdf_dict

    def create_data_from_json_dict(self, json_dict):
        if isinstance(json_dict, dict):
            try:
                input_file = json_dict['input_file']
                self.input_file_path = input_file['path']
                # print('filePath for input file :', input_file_path)
                self.input_file_sheet = input_file['sheet_name']
                # print('sheets in input file :', input_file_sheet)

                find_replace_file = json_dict['find_replace_file']
                self.find_replace_file_path = find_replace_file['path']
                # print('filePath for find&Replace file :', find_replace_file_path)
                self.find_replace_file_sheet = find_replace_file['sheet_name']
                # print('sheets in find&Replace file :', find_replace_file_sheet)

                output_file = json_dict['output_file']
                self.output_file_path = output_file['path']
                # print('filePath for output file :', output_file_path)
            except KeyError:
                print('Field in CSV_to_MDF_Configuration_Data wrongly formatted')
                sys.exit()
        else:
            print('create_data_from_json_dict(): error in input data')
            sys.exit()

class Configuration_File(QWidget):
    def __init__(self):
        super().__init__()

    def open(self):
        # options = QFileDialog.Options()
        # options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self, 'Select configuration file', "", 'JSON file (*.json)')
        if fileName:
            print(fileName)
        else:
            raise ValueError

    def save(self, select_new_file=False):

        self.configuration_file_data['root']['CSV_to_MDF'] = CSV_to_MDF_data
        # self.configuration_file_data['root']['CAN_highlighting'] = tc_highlight_data
        # self.configuration_file_data['root']['find_replace_multiple_row'] = tc_substitution_data

        print(self.configuration_file_data)

        # Serializing json
        json_object = json.dumps(self.configuration_file_data, indent=4)

        if not select_new_file:
            fileName = self.configuration_file_name
        else:
            fileName, _ = QFileDialog.getSaveFileName(self, "Save configuration as ", "",
                                                      'JSON file (*.json)')  # , options=options)
        if self.configuration_file_name:
            # Writing to sample.json
            try:
                with open(fileName, "w") as outfile:
                    outfile.write(json_object)
            except IOError:
                print("Error in writing files")

            self.configuration_file_name = fileName
