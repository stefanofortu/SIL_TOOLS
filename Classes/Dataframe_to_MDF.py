from asammdf import MDF, Signal

class Dataframe_to_MDF():
    def __init__(self):
        pass

    @staticmethod
    def save_to_mdf(data_dctionary, time_column_type= "absolute"):
        print("dataframe_list must be a list of dataframes:"
              " [dataframe1, dataframe2, dataframe3]")

        print("each dataframe should have the first column \"Time\" with absolute or relative date time according to the parameter time_column_type")
        return
        column_to_delete = []
        for col_name in columns_to_process:
            number_of_nan_values = df[col_name].isnull().sum()
            column_size = df[col_name].size
            if number_of_nan_values == column_size:
                # print(col_name , ": all Nan")
                column_to_delete.append(col_name)

        columns_to_process = [col for col in columns_to_process if col not in column_to_delete]
        #############
        ## STEP2 : creare asse dei tempi
        #############
        timestamps = np.array(df["relative_time"].apply(lambda x: x.seconds))

        #############
        ## STEP2 : creare i segnali effettivi dal dataframe
        #############

        signals_list = []

        for col_name in columns_to_process:
            signal = Signal(samples=np.array(df[col_name], dtype=df[col_name].dtypes),
                            timestamps=timestamps, name=col_name, unit='')

            signals_list.append(signal)

        # create empty MDf version 4.00 file
        with (MDF(version='4.10') as mdf4):
            # append the signals to the new file
            mdf4.append(signals_list, comment='imported')
            mdf4.start_time = start_time.to_pydatetime()  # datetime.fromisoformat("2024-08-06 17:00:00")
            # save new file
            if use_same_input_file_name == True:
                out_filename = input_file_path[:-4] + ".mf4"
            else:
                out_filename = output_file_name
                mdf4.save(path + filename + ".mf4", overwrite=True)
            #print(out_filename)
            mdf4.save(out_filename, overwrite=True)
