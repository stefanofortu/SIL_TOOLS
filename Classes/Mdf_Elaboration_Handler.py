from asammdf import MDF
from Classes.Dataframe_to_MDF import Dataframe_to_MDF
from pandas import Timestamp, to_datetime


class Mdf_Elaboration_Handler:
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
    def save_to_mdf(df, output_file_path):
        # print("df.columns post rename", df.columns)
        Dataframe_to_MDF.save_to_mdf(dataframe_list=[df], output_file_name=output_file_path)
