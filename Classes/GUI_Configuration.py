from Conversions.CSV_to_MDF_Handler import CSV_to_MDF_Handler
from Conversions.Vector_to_MDF import Vector_to_MDF
from Conversions.Eurotherm_to_MDF import Eurotherm_to_MDF
from Conversions.Eurotherm_exported_to_MDF import Eurotherm_exported_to_MDF

############################# MDF CONVERSION ####################################################

GUI_mdf_converstion_selection = ["EDAG", "Bertrandt", "PumpLogger", "Dielectrik", "Vector",
                                 "Eurotherm CSV Export Data", "Eurotherm CSV Logged Data"]


def gui_mdf_conversion_start_conversion_function(selected_text,
                                                 input_file_path=None,
                                                 use_same_input_file_name=None,
                                                 output_file_name=None):
    if selected_text == "EDAG":
        CSV_to_MDF_Handler.exec_substitution(input_file_path=input_file_path,
                                             use_same_input_file_name=use_same_input_file_name,
                                             output_file_name=output_file_name)

    elif selected_text == "Bertrandt":
        bertrandt_to_mdf_handler.exec_conversion(self.cfg_data.mdf_conversion_input_file_path,
                                                      use_same_name,
                                                      self.cfg_data.mdf_conversion_output_file_path)

    elif selected_text == "PumpLogger":
        pumplogger_to_mdf.exec_conversion(cfg_data.mdf_conversion_input_file_path,
                                               use_same_name,
                                               cfg_data.mdf_conversion_output_file_path)

    elif selected_text == "Dielectrik":
        dielectrik_to_mdf.exec_conversion(cfg_data.mdf_conversion_input_file_path,
                                               use_same_name,
                                               cfg_data.mdf_conversion_output_file_path)

    elif selected_text == "Vector":
        Vector_to_MDF.exec_conversion(input_file_path=cfg_data.mdf_conversion_input_file_path,
                                      use_same_input_file_name=True,
                                      output_file_name=cfg_data.mdf_conversion_output_file_path)

    elif selected_text == "Eurotherm CSV Export Data":
        Eurotherm_to_MDF.exec_conversion(input_file_path=input_file_path,
                                      use_same_input_file_name=use_same_input_file_name,
                                      output_file_name=output_file_name)

    elif selected_text == "Eurotherm CSV Logged Data":
        Eurotherm_exported_to_MDF.exec_conversion(input_file_path=input_file_path,
                                      use_same_input_file_name=use_same_input_file_name,
                                      output_file_name=output_file_name)
    else:
        print("Wrong selection in selection_comboBox")
