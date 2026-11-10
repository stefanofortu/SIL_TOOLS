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
        df = df.rename(columns={'timestamps': 'Time[s]'})
        #print(df.columns)
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
        df.drop(columns=["all_nb[°C]"], inplace=True)
        df.drop(columns=["all_Notaus[ohne]"], inplace=True)
        df.drop(columns=["all_Level[ohne]"], inplace=True)
        df.drop(columns=["all_DI3[ohne]"], inplace=True)
        df.drop(columns=["all_LaudaFeh[ohne]"], inplace=True)
        df.drop(columns=["all_DatenOut1[ohne]"], inplace=True)
        df.drop(columns=["all_DatenOut2[ohne]"], inplace=True)
        df.drop(columns=["all_DatenOut3[ohne]"], inplace=True)
        df.drop(columns=["__samples_origin"], inplace=True)

        # individua i reset
        reset = df['relative_seconds'].diff() < 0
        # numero progressivo di blocco
        gruppo = reset.cumsum()

        # offset da aggiungere a ciascun blocco
        offset = df.groupby(gruppo)['relative_seconds'].transform('first').where(gruppo == 0, 0)

        for g in range(1, gruppo.max() + 1):
            precedente = df.loc[gruppo == g - 1, 'relative_seconds'].max() + 1
            offset.loc[gruppo == g] = precedente

        df['Time[s]'] = df['relative_seconds'] + offset
        print(df.columns)

    @staticmethod
    def save_to_mdf(df, output_file_path, start_time=None):
        # print("df.columns post rename", df.columns)
        Dataframe_to_MDF.save_to_mdf(dataframe=df, output_file_name=output_file_path,
                                     time_column_type="relative", start_time=start_time)
