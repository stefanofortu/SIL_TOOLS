from Converters.Dewesoft_to_MDF import Dewesoft_to_MDF
from Converters.EN4_TDMS_to_MDF import EN4_TDMS_to_MDF
from Converters.CSV_to_MDF_Handler import CSV_to_MDF_Handler
from Converters.Vector_to_MDF import Vector_to_MDF
from Converters.Eurotherm_to_MDF import Eurotherm_to_MDF
from Converters.Eurotherm_exported_to_MDF import Eurotherm_exported_to_MDF

############################# MDF CONVERSION ####################################################

GUI_mdf_converstion_selection_list = ["EDAG", "Bertrandt", "PumpLogger", "Dielectrik", "Vector",
                                 "Eurotherm CSV Export Data", "Eurotherm CSV Logged Data",
                                 "TDMS [banco EN4]", "Dewesoft"]


def select_filter_for_file(current_text):
    # append to this list
    possible_filters = ["Text Files (*.txt)", "CSV Files (*.csv)", "Python Files (*.py)",
                        "PumpLogger_data (*.data)", "MDF file (*.mf4)", "TMDS file (*.tdms)",
                        "Dewesoft Data (*.dxd)", "All Files (*)"]

    if current_text == "EDAG":
        selected_filter = possible_filters[0]  # .txt
    elif current_text == "Bertrandt":
        selected_filter = possible_filters[1]  # .csv
    elif current_text == "PumpLogger":
        selected_filter = possible_filters[3]  # .data
    elif current_text == "Dielectrik":
        selected_filter = possible_filters[0]  # .txt
    elif current_text == "Vector":
        selected_filter = possible_filters[4]  # .mf4
    elif current_text == "Eurotherm CSV Export Data":
        selected_filter = possible_filters[4]  # .mf4
    elif current_text == "Eurotherm CSV Logged Data":
        selected_filter = possible_filters[4]  # .mf4
    elif current_text == "TDMS [banco EN4]":
        selected_filter = possible_filters[5]  # .tdms
    elif current_text == "Dewesoft":
        selected_filter = possible_filters[6]  # .tdms
    else:
        print("Pre-defined file extension not present")
        selected_filter = possible_filters[1]

    return possible_filters, selected_filter


def select_and_start_conversion(selected_text, input_file_list, use_same_input_file_name, output_file_name):

    if selected_text == "EDAG":
        CSV_to_MDF_Handler.exec_substitution(input_file_list=input_file_list,
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
        Eurotherm_exported_to_MDF.exec_conversion(input_file_path=input_file_path,
                                         use_same_input_file_name=use_same_input_file_name,
                                         output_file_name=output_file_name)

    elif selected_text == "Eurotherm CSV Logged Data":
        Eurotherm_to_MDF.exec_conversion(input_file_list=input_file_list,
                                         use_same_input_file_name=use_same_input_file_name,
                                         output_file_name=output_file_name)

    elif selected_text == "TDMS [banco EN4]":
        EN4_TDMS_to_MDF.exec_conversion(input_file_list=input_file_list,
                                        use_same_input_file_name=use_same_input_file_name,
                                        output_file_name=output_file_name)
    elif selected_text == "Dewesoft":
        Dewesoft_to_MDF.exec_conversion(input_file_list=input_file_list,
                                        use_same_input_file_name=use_same_input_file_name,
                                        output_file_name=output_file_name)
    else:
        print(f"Wrong selection in selection_comboBox: {selected_text}")


############################# CSV CONVERSION ####################################################
from Converters.MDF_to_CSV import MDF_to_CSV
from Converters.Dewesoft_to_CSV import Dewesoft_to_CSV

CSV_conversion_GUI_selection_list = ["MDF", "Dewesoft"]

def CSV_conversion_select_filter_for_file(current_text):
    # append to this list
    all_filters = ["MDF file (*.mf4)", "Dewesoft file (*.dxd)", "All Files (*)"]

    if current_text == "MDF":
        selected_filter = all_filters[0]  # .mf4
    elif current_text == "Dewesoft":
        selected_filter = all_filters[1]  # .dxd
    else:
        print("Pre-defined file extension not present")
        selected_filter = all_filters[1]

    return all_filters, selected_filter


def CSV_conversion_start_conversion(selected_text, input_file_list, use_same_input_file_name, output_file_name):
    print("CSV_conversion_start_conversion")
    if selected_text == "MDF":
        MDF_to_CSV.exec_substitution(input_file_list=input_file_list,
                                     use_same_input_file_name=use_same_input_file_name,
                                     output_file_name=output_file_name)

    elif selected_text == "Dewesoft":
        Dewesoft_to_CSV.exec_conversion(input_file_list=input_file_list,
                                        use_same_input_file_name=use_same_input_file_name,
                                        output_file_name=output_file_name)
    else:
        print("Wrong selection in selection_comboBox")
