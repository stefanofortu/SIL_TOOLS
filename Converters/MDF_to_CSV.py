class MDF_to_CSV:

    @staticmethod
    def exec_conversion(input_file_list, use_same_input_file_name, output_file_name):
        input_file_path = input_file_list[0]
        if use_same_input_file_name == True:
            out_filename = input_file_path[:-4] + "_TMM_names" + ".mf4"
        else:
            out_filename = output_file_name
            print("error - use_same_input_file_name == False")
            exit()

        print("CONVERSIONNNNNN DEWESOFT TO CSV")




from Converters.Dewesoft_to_CSV import Dewesoft_to_CSV