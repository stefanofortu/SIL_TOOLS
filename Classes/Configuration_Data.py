import json
import sys

from PySide6.QtWidgets import QWidget, QFileDialog

FILE_NAME_DEFAULT = "SIL_config_data.json"

class Configuration_Data: #CHANGE NAME TO FILE
    def __init__(self):
        self.configuration_file_name = FILE_NAME_DEFAULT
        print("sistema le variabili in questo file di configurazione")
        self.mdf_conversion_input_file_path = ""
        self.mdf_conversion_output_file_path = ""
        self.mdf_elaboration_input_file_path = ""
        self.mdf_elaboration_output_file_path = ""
        self.load_cfg_data_from_file()

    def load_cfg_data_from_file(self):
        try:
            with open(self.configuration_file_name, 'r') as json_file:
                json_file_no_comment = ''.join(line for line in json_file if not line.startswith('#'))
                file_dict = json.loads(json_file_no_comment)

                try:
                    cfg_data_dict = file_dict['root']['SIL_CFG_DATA']
                except KeyError:
                    print("Field 'SIL_CFG_DATA' in file " , self.configuration_file_name, "does not exist")
                    sys.exit()

                if isinstance(cfg_data_dict, dict):
                    try:
                        input_file = cfg_data_dict['mdf_conversion_input_file']
                        self.mdf_conversion_input_file_path = input_file['path']

                        output_file = cfg_data_dict['mdf_conversion_output_file']
                        self.mdf_conversion_output_file_path = output_file['path']

                        mdf_elaboration_input_file = cfg_data_dict['mdf_elaboration_input_file']
                        self.mdf_elaboration_input_file_path = mdf_elaboration_input_file['path']

                        mdf_elaboration_output_file = cfg_data_dict['mdf_elaboration_output_file']
                        self.mdf_elaboration_output_file_path = mdf_elaboration_output_file['path']
                    except KeyError:
                        print('Field in Conversion_to_MDF wrongly formatted')
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
                "SIL_CFG_DATA": {},
            }
        }
        configuration_file_data['root']['SIL_CFG_DATA'] = dict({
            "mdf_conversion_input_file": {
                "path": self.mdf_conversion_input_file_path,
            },
            "mdf_conversion_output_file": {
                "path": self.mdf_conversion_output_file_path
            },
            "mdf_elaboration_input_file": {
                "path": self.mdf_elaboration_input_file_path,
            },
            "mdf_elaboration_output_file": {
                "path": self.mdf_elaboration_output_file_path
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