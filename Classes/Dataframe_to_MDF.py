from numpy import array as np_array
from asammdf import MDF, Signal
from pandas import Timestamp


class Dataframe_to_MDF:
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
    def save_to_mdf(dataframe, output_file_name, time_column_type="relative"):
        print("dataframe_list must be a list of dataframes:"
              " [dataframe1, dataframe2, dataframe3]")
        print("time_column_type=relative OBSOLETE")

        if time_column_type == "relative":
            print("time_column_type == relative to be reviewed")
            exit()

        print("OBSOLETE each dataframe should have the first column \"Time[s]\" "
              "with relative date or absolute time according to the parameter time_column_type. MISSING CHECKS")
        if time_column_type == "relative":
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
                        start_time = 0
                        mdf4.start_time = start_time.to_pydatetime()  # datetime.fromisoformat("2024-08-06 17:00:00")
                    # save new file
                    mdf4.save(output_file_name, overwrite=True)

        if time_column_type == "absolute":
            df = dataframe
            signal_name_list = [x for x in df.columns if x != "Time"]
            print(f"signal_name_list {signal_name_list}")
            print("OBSOLETE each dataframe should have the first column \"Time\" "
                  "with absolute time in pydatetime format. MISSING CHECKS")
            print(df.head(5))
            #############  creare asse dei tempi #############
            start_time = df['Time'].iloc[0]
            print(start_time)
            print(type(start_time))
            # Inserimento di una colonna "Time_rel" con valori in 'datetime'
            df.insert(2, 'Time_rel[s]', df['Time'] - start_time)
            # Creazione dei timestamp
            timestamps = np_array(df["Time_rel[s]"].dt.total_seconds())
            print(timestamps)


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
                    mdf4.start_time = start_time  # datetime.fromisoformat("2024-08-06 17:00:00")
                # save new file
                mdf4.save(output_file_name, overwrite=True)
