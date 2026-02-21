import json
import sys

from PySide6.QtWidgets import QWidget, QFileDialog

FILE_NAME_DEFAULT = "SIL_config_data.json"


class Configuration_Data:  # CHANGE NAME TO FILE
    def __init__(self):
        self.configuration_file_name = FILE_NAME_DEFAULT
        print("sistema le variabili in questo file di configurazione")
        ############# TAB CONFIGURATION ####################
        self.tab_mdf_conversion = True
        self.tab_mdf_elaboration = True
        self.tab_csv_conversion = True
        self.tab_arduino = False
        self.tab_curve = False
        ####################### CSV CONVERTION #######################
        self.mdf_conversion_input_file_list = []
        self.mdf_conversion_output_file_path = ""   ###########DA ELIMINARE
        ####################### CSV CONVERTION #######################
        self.mdf_elaboration_input_file_path = ""
        self.mdf_elaboration_insert_read_by_value_delay = 0
        self.mdf_elaboration_insert_read_by_value_waiting = 0
        self.mdf_elaboration_insert_read_by_value_time = 0
        self.mdf_elaboration_insert_read_by_value_repetitions = 0
        self.mdf_elaboration_insert_read_by_threshold_signal_name = 0
        self.mdf_elaboration_insert_read_by_threshold_value = 0
        self.mdf_elaboration_output_file_path = ""
        ####################### CSV CONVERTION #######################
        self.csv_conversion_input_file_combobox = ""
        self.csv_conversion_input_file_list = ""
        ############# VECTOR GENERATOR ####################
        self.vector_generator_ldf_file = ""
        self.vector_generator_capl_vcu_file = ""
        self.vector_generator_capl_valve_file = ""
        ####################### LOAD CFG #######################ì
        self.load_cfg_data_from_file()

    def load_cfg_data_from_file(self):
        try:
            with open(self.configuration_file_name, 'r') as json_file:
                json_file_no_comment = ''.join(line for line in json_file if not line.startswith('#'))
                file_dict = json.loads(json_file_no_comment)

                try:
                    cfg_data_dict = file_dict['root']['SIL_CFG_DATA']
                except KeyError:
                    print("Field 'SIL_CFG_DATA' in file ", self.configuration_file_name, "does not exist")
                    sys.exit()

                if isinstance(cfg_data_dict, dict):
                    try:
                        ############# TAB CONFIGURATION ####################
                        self.tab_mdf_conversion = self.get_parameter_from_file(cfg_data=cfg_data_dict,
                                                                                   label="tab_mdf_conversion",
                                                                                   expected_type=bool)
                        self.tab_mdf_elaboration = self.get_parameter_from_file(cfg_data=cfg_data_dict,
                                                                                   label="tab_mdf_elaboration",
                                                                                   expected_type=bool)
                        self.tab_csv_conversion = self.get_parameter_from_file(cfg_data=cfg_data_dict,
                                                                                   label="tab_csv_conversion",
                                                                                   expected_type=bool)
                        self.tab_arduino = self.get_parameter_from_file(cfg_data=cfg_data_dict,
                                                                                   label="tab_arduino",
                                                                                   expected_type=bool)
                        self.tab_curve = self.get_parameter_from_file(cfg_data=cfg_data_dict,
                                                                                   label="tab_curve",
                                                                                   expected_type=bool)
                        ############# TAB MDF CONVERTION ####################
                        self.mdf_conversion_input_file_list = cfg_data_dict['mdf_conversion_input_file_list']
                        if not isinstance(self.mdf_conversion_input_file_list, list):
                            print("Error: load_cfg_data_from_file. Wrong type of self.mdf_conversion_input_file_list :",
                                  type(self.mdf_conversion_input_file_list))

                        #output_file = cfg_data_dict['mdf_conversion_output_file']
                        #self.mdf_conversion_output_file_path = output_file['path']

                        ############# TAB MDF ELABORATION ####################
                        #
                        # mdf_elaboration_input_file = cfg_data_dict['mdf_elaboration_insert_read_by_value_delay']
                        # self.mdf_elaboration_input_file_path = mdf_elaboration_input_file['path']
                        #
                        # mdf_elaboration_output_file = cfg_data_dict['mdf_elaboration_output_file']
                        # self.mdf_elaboration_output_file_path = mdf_elaboration_output_file['path']
                        #
                        # "mdf_elaboration_insert_read_by_value_delay": {
                        #     "path": self.mdf_elaboration_insert_read_by_value_delay,
                        # },
                        # "mdf_elaboration_insert_read_by_value_waiting": {
                        #     "path": self.mdf_elaboration_insert_read_by_value_waiting,
                        # },
                        # "mdf_elaboration_insert_read_by_value_time": {
                        #     "path": self.mdf_elaboration_insert_read_by_value_time,
                        # },
                        # "mdf_elaboration_insert_read_by_value_repetitions": {
                        #     "path": self.mdf_elaboration_insert_read_by_value_repetitions,
                        # },
                        # "mdf_elaboration_insert_read_by_threshold_signal_name": {
                        #     "path": self.mdf_elaboration_insert_read_by_threshold_signal_name,
                        # },
                        # "mdf_elaboration_insert_read_by_threshold_value": {
                        #     "path": self.mdf_elaboration_insert_read_by_threshold_value,
                        # },
                        # "mdf_elaboration_output_file": {
                        #     "path": self.ò
                        #
                        #
                        #
                        # mdf_elaboration_input_file = cfg_data_dict['mdf_elaboration_input_file']
                        # self.mdf_elaboration_input_file_path = mdf_elaboration_input_file['path']
                        #
                        # mdf_elaboration_output_file = cfg_data_dict['mdf_elaboration_output_file']
                        # self.mdf_elaboration_output_file_path = mdf_elaboration_output_file['path']

                        ############# CSV CONVERTION ####################
                        self.csv_conversion_input_file_combobox = cfg_data_dict['csv_conversion_input_file_combobox']
                        self.csv_conversion_input_file_list = cfg_data_dict['csv_conversion_input_file_list']
                    except KeyError:
                        print('Field in Conversion_to_MDF wrongly formatted')
                        sys.exit()
                else:
                    print('create_data_from_json_dict(): error in input data')
                    sys.exit()

        except FileNotFoundError:
            print('File self.configuration_file_name does not exist')
            self.save_cfg_data_to_file(filename_default=True, select_new_file=False)

    @staticmethod
    def get_parameter_from_file(cfg_data, label, expected_type):
        if isinstance(cfg_data[label], bool):
            return cfg_data[label]
        else:
            print(f"Error: get_parameter_from_file. {label} does not have type {expected_type.__name__}")
            return None

    def save_cfg_data_to_file(self, filename_default=False, select_new_file=False):
        configuration_file_data = {
            "root": {
                "SIL_CFG_DATA": {},
            }
        }
        configuration_file_data['root']['SIL_CFG_DATA'] = dict({
            ############# TAB CONFIGURATION ####################
            "tab_mdf_conversion": self.tab_mdf_conversion,
            "tab_mdf_elaboration": self.tab_mdf_elaboration,
            "tab_csv_conversion": self.tab_csv_conversion,
            "tab_arduino": self.tab_arduino,
            "tab_curve" : self.tab_curve,
            ############# TAB MDF ELABORATION ####################
            "mdf_conversion_input_file_list":  self.mdf_conversion_input_file_list,
            #"mdf_conversion_input_file_list": self.mdf_conversion_input_file_list,
            ############# TAB MDF ELABORATIO ####################

            "mdf_elaboration_insert_read_by_value_delay": self.mdf_elaboration_insert_read_by_value_delay,
            "mdf_elaboration_insert_read_by_value_waiting": self.mdf_elaboration_insert_read_by_value_waiting,
            "mdf_elaboration_insert_read_by_value_time": self.mdf_elaboration_insert_read_by_value_time,
            "mdf_elaboration_insert_read_by_value_repetitions": self.mdf_elaboration_insert_read_by_value_repetitions,
            "mdf_elaboration_insert_read_by_threshold_signal_name": self.mdf_elaboration_insert_read_by_threshold_signal_name,
            "mdf_elaboration_insert_read_by_threshold_value": self.mdf_elaboration_insert_read_by_threshold_value,
            "mdf_elaboration_output_file": self.mdf_elaboration_output_file_path,
            ############# CSV CONVERTION ####################
            "csv_conversion_input_file_combobox": self.csv_conversion_input_file_combobox,
            "csv_conversion_input_file_list": self.csv_conversion_input_file_list,
            ############# VECTOR GENERATOR ####################
            "Vector_generator_LDF_file": self.vector_generator_ldf_file,
            "Vector_generator_CAPL_VCU_file": self.vector_generator_capl_vcu_file,
            "Vector_generator_CAPL_VALVE_file": self.vector_generator_capl_valve_file
        }
        )

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
