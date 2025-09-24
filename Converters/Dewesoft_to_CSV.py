from libraries.DW_to_Py_Converter import Dewesoft_Converter


class Dewesoft_to_CSV:

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

            df["timestamp"] = df["timestamp"].dt.strftime("%d/%m/%Y %H:%M:%S.%f")
            df = df.rename(columns={"timestamp": "Time"})

            df.to_csv(out_filename, index=False)
            print("csv salvato")


if __name__ == "__main__":
    filename = "C:\\Users\\stefano.fortunati\\Desktop\\test_dewesoft.dxd"
    print("Loading file:", filename)

    dewesoft_converter = Dewesoft_Converter()
    dewesoft_converter.open(filename=filename)
    df1 = dewesoft_converter.to_pandas()
    dewesoft_converter.close()