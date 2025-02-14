from numpy import array as np_array
from asammdf import MDF, Signal
from pandas import Timestamp


class Dataframe_to_MDF():
    def __init__(self):
        pass

    @staticmethod
    def load_from_mdf(input_file_path):
        mdf_obj = MDF(input_file_path)
        df = mdf_obj.to_dataframe()
        df = df.reset_index()
        df = df.rename(columns={'timestamps': 'Time[s]'})
        start_time = Timestamp(mdf_obj.start_time)
        return df, start_time

    @staticmethod
    def save_to_mdf(dataframe_list, output_file_name, time_column_type="relative"):
        print("dataframe_list must be a list of dataframes:"
              " [dataframe1, dataframe2, dataframe3]")

        if time_column_type != "relative":
            print("time_column_type absolute not implemented yet")
            exit()

        print("each dataframe should have the first column \"Time[s]\" "
              "with relative date or absolute time according to the parameter time_column_type. MISSING CHECKS")
        for df in dataframe_list:
            signal_name_list = [x for x in df.columns if x != "Time[s]"]

            #############  creare asse dei tempi #############
            timestamps = np_array(df["Time[s]"])

            ############# ## STEP2 : creare i segnali effettivi dal dataframe #############

            signals_list = []

            for col_name in signal_name_list:
                signal = Signal(samples=np_array(df[col_name], dtype=df[col_name].dtypes),
                                timestamps=timestamps, name=col_name, unit='')

                signals_list.append(signal)

            # create empty MDf version 4.00 file
            with (MDF(version='4.10') as mdf4):
                # append the signals to the new file
                mdf4.append(signals_list, comment='imported')
                if time_column_type == "absolute":
                    start_time = 0;
                    mdf4.start_time = start_time.to_pydatetime()  # datetime.fromisoformat("2024-08-06 17:00:00")
                # save new file
                mdf4.save(output_file_name, overwrite=True)
