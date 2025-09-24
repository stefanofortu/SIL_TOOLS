from libraries.DW_to_Py_Converter import Dewesoft_Converter
from Classes.Dataframe_to_MDF import Dataframe_to_MDF


class Dewesoft_to_MDF:

    @staticmethod
    def exec_conversion(input_file_list, use_same_input_file_name, output_file_name):

        for input_file_name in input_file_list:
            if use_same_input_file_name == True:
                out_filename = input_file_name[:-4] + ".csv"
            else:
                out_filename = output_file_name
                print("error - use_same_input_file_name == False")
                exit()
            print(input_file_name)

            dewesoft_converter = Dewesoft_Converter()
            dewesoft_converter.open(filename=input_file_name)
            # dewesoft_converter.shows_all_info()
            df = dewesoft_converter.to_pandas(verbose=False)
            dewesoft_converter.close()

            df = df.rename(columns={"timestamp": "Time"})
            df.drop(columns="Time[s]", inplace=True)
            Dataframe_to_MDF.save_to_mdf(dataframe=df,
                                         output_file_name=out_filename,
                                         time_column_type="absolute")
