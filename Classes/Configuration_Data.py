import json
import sys

from PySide6.QtWidgets import QWidget, QFileDialog

FILE_NAME_DEFAULT = "SIL_config_data.json"

class Configuration_Data: #CHANGE NAME TO FILE
    def __init__(self):
        self.configuration_file_name = FILE_NAME_DEFAULT
        self.input_file_path = ""
        self.output_file_path = ""
        self.load_cfg_data_from_file()

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

                if isinstance(CSV_to_MDF_cfg_data_dict, dict):
                    try:
                        input_file = CSV_to_MDF_cfg_data_dict['input_file']
                        self.input_file_path = input_file['path']

                        output_file = CSV_to_MDF_cfg_data_dict['output_file']
                        self.output_file_path = output_file['path']
                        # print('filePath for output file :', output_file_path)
                    except KeyError:
                        print('Field in CSV_to_MDF_Configuration_Data wrongly formatted')
                        sys.exit()
                else:
                    print('create_data_from_json_dict(): error in input data')
                    sys.exit()

        except FileNotFoundError:
            print('File self.configuration_file_name does not exist')
            self.save_cfg_data_to_file(filename_default=True, select_new_file=False)



    def save_cfg_data_to_file(self, filename_default=False, select_new_file=False):
        configuration_file_data = {
            "root": {
                "CSV_to_MDF": {},
                "CAN_highlighting": {},
                "find_replace_multiple_row": {}
            }
        }
        configuration_file_data['root']['CSV_to_MDF'] = dict({
            "input_file": {
                "path": self.input_file_path,
            },
            "output_file": {
                "path": self.output_file_path
            }
        })

        # Serializing json
        json_object = json.dumps(configuration_file_data, indent=4)

        print("about to write")
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

        if self.configuration_file_name:
            try:
                with open(self.configuration_file_name, "w") as outfile:
                    outfile.write(json_object)
            except IOError:
                print("Error in writing files - self.configuration_file_name")

# class CSV_to_MDF_Configuration_Data:
#     def __init__(self, csv_to_mdf_dictionary=None):
#         if csv_to_mdf_dictionary == None:
#             pass
#         else:
#             self.create_data_from_json_dict(csv_to_mdf_dictionary)
#
#     def create_json_dict_from_data(self):
#         csv_to_mdf_dict = {
#             "input_file": {
#                 "path": self.input_file_path,
#             },
#             "output_file": {
#                 "path": self.output_file_path
#             }
#         }
#
#         return csv_to_mdf_dict

# class Configuration_File(QWidget):
#     def __init__(self):
#         super().__init__()
#
#     def open(self):
#         # options = QFileDialog.Options()
#         # options |= QFileDialog.DontUseNativeDialog
#         fileName, _ = QFileDialog.getOpenFileName(self, 'Select configuration file', "", 'JSON file (*.json)')
#         if fileName:
#             print(fileName)
#         else:
#             raise ValueError
#
#     def save(self, select_new_file=False):
#
#         self.configuration_file_data['root']['CSV_to_MDF'] = CSV_to_MDF_data
#         # self.configuration_file_data['root']['CAN_highlighting'] = tc_highlight_data
#         # self.configuration_file_data['root']['find_replace_multiple_row'] = tc_substitution_data
#
#         print(self.configuration_file_data)
#
#         # Serializing json
#         json_object = json.dumps(self.configuration_file_data, indent=4)
#
#         if not select_new_file:
#             fileName = self.configuration_file_name
#         else:
#             fileName, _ = QFileDialog.getSaveFileName(self, "Save configuration as ", "",
#                                                       'JSON file (*.json)')  # , options=options)
#         if self.configuration_file_name:
#             # Writing to sample.json
#             try:
#                 with open(fileName, "w") as outfile:
#                     outfile.write(json_object)
#             except IOError:
#                 print("Error in writing files")
#
#             self.configuration_file_name = fileName
