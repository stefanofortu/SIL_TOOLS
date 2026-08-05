from asammdf import MDF
from Classes.Dataframe_to_MDF import Dataframe_to_MDF
from pandas import Timestamp, to_datetime
import numpy as np


class Mdf_Elaboration_Handler:
    def __init__(self):
        pass

    @staticmethod
    def load_from_mdf(input_file_path):
        mdf_obj = MDF(input_file_path)
        df = mdf_obj.to_dataframe()
        print(mdf_obj.start_time)
        start_time = Timestamp(mdf_obj.start_time)
        print(start_time)
        #print(df.head(10))
        print(df.columns)

        print(df["Time[s]"])
        df[["Time[s]"]].to_csv("Time[s].csv", index=False)
        df = df.reset_index()
        #df = df.rename(columns={'timestamps': 'Time[s]'})

        return df, start_time

    @staticmethod
    def insert_read_value(row, read_start_time, read_waiting_time, read_high_time, read_end_time):
        if row['Time[s]'] < read_start_time:
            return 0
        elif row['Time[s]'] > read_end_time:
            return 0
        else:
            instant_in_timed_window = (row['Time[s]'] - read_start_time) % (read_waiting_time + read_high_time)
            if instant_in_timed_window > read_waiting_time:
                return 1
            else:
                return 0

    @staticmethod
    def insert_read(df, read_start_time, read_waiting_time, read_high_time, read_numbers):
        read_end_time = (read_waiting_time + read_high_time) * read_numbers + read_start_time
        df['Read'] = df.apply(Mdf_Elaboration_Handler.insert_read_value,
                              axis=1,
                              read_start_time=read_start_time,
                              read_waiting_time=read_waiting_time,
                              read_high_time=read_high_time,
                              read_end_time=read_end_time)
        return df

    @staticmethod
    def insert_read_by_threshold(df, signal_name, threshold):
        if signal_name not in list(df.columns):
            print("Error: COLUMN NOT FOUND IN DATAFRAME")
        else:
            df['Read'] = df[signal_name].apply(lambda x: 1 if x > threshold else 0)
        return df

    @staticmethod
    def modify_columns(source_column, percentage_max=0.02, offset=1.0):
        random_values = np.random.uniform(-percentage_max, percentage_max, len(source_column))

        modified_column = source_column * (1 + random_values) + offset
        return modified_column

    @staticmethod
    def M04_transormation(df):
        df.rename(columns={"P01_I1[bar]": "P01_I1[A]"}, inplace=True)
        df.rename(columns={"P02_I2[bar]": "P02_I2[A]"}, inplace=True)

        df["P01_I1[A]"] = Mdf_Elaboration_Handler.modify_columns(df["P02_I2[A]"], percentage_max=0.05, offset=0)
        df["P01_U1[V]"] = Mdf_Elaboration_Handler.modify_columns(df["P02_U2[V]"], percentage_max=0, offset=0.2)
        df["P01_dp1[mbar]"] = Mdf_Elaboration_Handler.modify_columns(df["P02_dp2[mbar]"], percentage_max=0.05, offset=0.05)
        df["P03_I3[A]"] = Mdf_Elaboration_Handler.modify_columns(df["P04_I4[A]"], percentage_max=0.05, offset=0)
        df["P03_U3[V]"] = Mdf_Elaboration_Handler.modify_columns(df["P04_U4[V]"], percentage_max=0, offset=0.2)
        df["P03_dp3[mbar]"] = Mdf_Elaboration_Handler.modify_columns(df["P04_dp4[mbar]"], percentage_max=0.05, offset=0.05)
        #df.drop(columns=["P01_I1[bar]"], inplace=True)
        #df.rename(columns={"P02_I2[bar]": "P02_I2[A]"}, inplace=True)

    @staticmethod
    def save_to_mdf(df, output_file_path, start_time=None):
        # print("df.columns post rename", df.columns)
        Dataframe_to_MDF.save_to_mdf(dataframe=df, output_file_name=output_file_path,
                                     time_column_type="relative", start_time=start_time)
