import logging
from openpyxl import load_workbook

from asammdf import MDF, Signal
import numpy as np
import pandas as pd
from collections import namedtuple


class Bertrandt_to_MDF_Handler:
    def __init__(self):
        pass

    @staticmethod
    def fix_df_dtype(df):
        for col_name in df.columns:
            unique_types = df[col_name].map(type).unique()
            #print(f"Column {col_name} has types: {unique_types}")

            if len(unique_types) == 1:
                if df[col_name].dtypes == 'str':
                    #df[col_name] = df[col_name].str.replace(',', '.')
                    #df[col_name] = df[col_name].str.replace(' ', '')
                    df[col_name] = pd.to_numeric(df[col_name], errors='coerce')
                elif df[col_name].dtypes == 'object':
                    #print(df[col_name].dtypes)
                    #print((type(df[col_name])))
                    df[col_name] = df[col_name].str.replace(',', '.').astype(float)
                elif df[col_name].dtypes == 'int64':
                    df[col_name] = df[col_name].astype(int)
                elif df[col_name].dtypes == 'float64':
                    # print("float64 ", col_name)
                    df[col_name] = df[col_name].replace(',', '.').astype(float)
                else:
                    print("exception raised 2")
                    print("Unknow dtypes type: " + col_name + df[col_name].dtypes)
            else:
                df[col_name] = df[col_name].astype(str)
                df[col_name] = df[col_name].str.replace(',', '.')
                df[col_name] = df[col_name].str.replace(' ', '')
                df[col_name] = pd.to_numeric(df[col_name], errors='coerce')
                # df[col_name] = df[col_name].str.replace(',', '.').astype(float)
        return df

    # -------------------
    # START CONFIGURATION
    # -------------------
    @staticmethod
    def exec_conversion(input_file_path, use_same_input_file_name, output_file_name):
        print("Convert Bertrandt file")
        print(input_file_path)

        df = pd.read_csv(input_file_path, sep="\t",
                         skiprows=[0, 1, 2, 3, 4, 5, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21],
                         # usecols=[x for x in range(0,10)],  # [x for x in range(0,10)],
                         # usecols=[4, 5, 12, 13, 20, 21, 36, 37, 52, 53, 68, 69, 84, 85, 100, 101, 116, 117, 132, 133,
                         #         148, 149],
                         # usecols =[82,83,84,85,86,87,88,89,106,107,108,109,110,111,112,113],
                         # nrows=1000,
                         #nrows=36000,
                         encoding="latin1")

        df_sample_rate = pd.read_csv(input_file_path, sep="\t",
                                     skiprows=[0, 1, 2, 3, 4, 5, 7, 8],
                                     # usecols=[x for x in range(0,10)],
                                     # usecols=[4, 5, 12, 13, 20, 21, 36, 37, 52, 53, 68, 69, 84, 85, 100, 101, 116, 117,
                                     #         132, 133, 148, 149],
                                     # usecols=[82, 83, 84, 85, 86, 87, 88, 89, 106, 107, 108, 109, 110, 111, 112, 113],
                                     nrows=1,
                                     encoding="latin1")
        #
        # print("START ", df['Name.4'].tail(10))
        # print(df_sample_rate.columns)

        # crea un lista di tuple dove:
        # posizione 0 : nome della colonna del timestamp
        # posizione 1 : nome della colonna del segnale
        # posizione 2 : sample rate
        header = ["Name"]
        df.to_csv('output_start.csv', columns=header)
        #print(df[["Name"]])
        #print("IS NA", df[["Name"]].isna().sum())
        #print("IS NULL", df[["Name"]].isnull().sum())

        df.replace(" ", np.nan, inplace=True)
        #print(df[["Name"]])

        signal_structure_list = []
        Signal_Structure = namedtuple('Signal_Structure',
                                      ['time_col_name', 'signal_col_name', 'sample_rate'])
        # inizializza le colonne con sample rate = 0
        counter = 0
        df_sr_columns = df_sample_rate.columns.tolist()
        while counter < len(df_sr_columns) - 1:
            s = Signal_Structure(df_sr_columns[counter],
                                 df_sr_columns[counter + 1],
                                 df_sample_rate.loc[0, df_sr_columns[counter + 1]])
            if str(s.time_col_name).startswith("Name"):
                signal_structure_list.append(s)
            else:
                print("Timestamp column does not start with 'Name'" + s.time_col_name)
            counter = counter + 2

        #print(signal_structure_list)

        columns_100ms = []
        columns_500ms = []
        for signal_structure in signal_structure_list:
            if signal_structure.sample_rate == 100:
                columns_100ms.append(signal_structure.time_col_name)
                columns_100ms.append(signal_structure.signal_col_name)
            elif signal_structure.sample_rate == 500:
                columns_500ms.append(signal_structure.time_col_name)
                columns_500ms.append(signal_structure.signal_col_name)
            else:
                print("Error - signal_structure.sample_rate not possible")

        col_to_drop = [x for x in df.columns.tolist() if ((x not in columns_100ms) and (x not in columns_500ms))]
        df.drop(columns=col_to_drop)

        # print(columns_500ms)
        # print("STEP 1 ", df['Name.4'].tail(10))


        # print(df['Name.4'].tail(10))
        # print("STEP 2 ", df['Name.4'].tail(10))

        df_100ms = df[columns_100ms].copy()
        df_500ms = df[columns_500ms].copy()
        print("shape before NAN dropping: 100ms:", df_100ms.shape)
        print("shape before NAN dropping: 500ms:", df_500ms.shape)
        df_100ms = df_100ms.dropna()
        df_500ms = df_500ms.dropna()
        print("shape after NAN dropping: 100ms:", df_100ms.shape)
        print("shape after NAN dropping: 500ms:", df_500ms.shape)
        header = ["Name"]
        df.to_csv('output.csv', columns=header)
        #df_500ms = df_500ms[df_500ms['Name']==""]
        #print(df_500ms.shape)

        df_100ms = Bertrandt_to_MDF_Handler.fix_df_dtype(df_100ms)
        df_500ms = Bertrandt_to_MDF_Handler.fix_df_dtype(df_500ms)

        #print("df_100ms.tail()", df_100ms.tail())
        #print("df_500ms.tail()", df_500ms.tail())
        # print("Name.4 -->", df_100ms['Name.4'].tail(20))

        for signal_structure in signal_structure_list:
            if signal_structure.sample_rate == 100:
                df_100ms[signal_structure.time_col_name] = np.divide(df_100ms[signal_structure.time_col_name], 1000)
            if signal_structure.sample_rate == 500:
                df_500ms[signal_structure.time_col_name] = np.divide(df_500ms[signal_structure.time_col_name], 1000)

        #print(df_100ms.shape)
        #print(df_500ms.shape)

        # print(len(df.columns))
        # print(len(tuple_signal_list))
        #
        # columns_100ms = []
        # columns_500ms = []
        # for col in df_sample_rate.columns:
        #     if df_sample_rate.loc[0, col] == 100:
        #         columns_100ms.append(col)
        #     elif df_sample_rate.loc[0, col] == 500:
        #         columns_500ms.append(col)
        #     elif df_sample_rate.loc[0, col] == "SampleTime[ms]":
        #         pass
        #     else:
        #         print("Error")
        #
        # print("columns_100ms", columns_100ms)
        # print("columns_500ms", columns_500ms)
        # #
        # # -------------------
        # # END CONFIGURATION
        # # -------------------
        # print("df.columns", list(df.columns))
        #
        # sample_rates = df.iloc[0].to_numpy()
        # # print(sample_rates)
        #
        # df.drop(0, axis=0, inplace=True)
        # # check number of column: -if it's odd, drop last one
        # if df.shape[1] % 2 == 1:
        #     df.drop(df.columns[-1], axis=1, inplace=True)
        #
        # for tup in tuple_signal_list:
        #     if tup[0].startswith("Name"):
        #         df[tup[0]] = np.divide(df[tup[0]], 1000)
        #     else:
        #         print("Timestamp column does not start with 'Name'")
        #
        # for col_name in df.columns:
        #     if df[col_name].dtypes == 'object':
        #         try:
        #             # print("object", col_name)
        #             df[col_name] = df[col_name].str.replace(',', '.').astype(float)
        #         except:
        #             pass
        #     elif df[col_name].dtypes == 'int64':
        #         print("int ", col_name)
        #         df[col_name] = df[col_name].astype(int)
        #
        #     elif df[col_name].dtypes == 'float64':
        #         # print("float64 ", col_name)
        #         df[col_name] = df[col_name].replace(',', '.').astype(float)
        #     else:
        #         print(col_name)
        #         print(df[col_name].dtypes)

        # ############
        # STEP1 : modificare il data set, per trasformare da str a decimali i numeri
        # ############
        # original_data_frame = ""

        #############
        ## STEP2 : creare asse dei tempi
        #############
        # Inserimento di una colonna "time" con valori in 'datetime'
        # df.insert(1, 'time', pd.to_datetime(df[df.columns[0]],format="%d.%m.%Y %H:%M:%S,%f"))
        # start_time = df['time'].iloc[0]

        # print("columns_to_process", df.columns)
        # print(df.head(5))

        # Inserimento di una colonna "relative_time" con valori in 'datetime'
        # df.insert(1, 'relative_time', df['time'] - 0)
        # print(df.head(5))

        # timestamp_500ms = np.array(df["Name"])
        # print("timestamp_500ms", timestamp_500ms)

        # timestamp_100ms = np.array(df["Name.1"])
        # print("timestamp_100ms", timestamp_100ms)

        #############
        ## STEP2 : creare i segnali effettivi dal dataframe
        #############

        signals_list_100ms = []
        signals_list_500ms = []

        for signal_structure in signal_structure_list:
            if signal_structure.sample_rate == 100:
                timestamp = np.array(df_100ms[signal_structure.time_col_name], dtype='float64')
                # print(signal_structure.time_col_name)
                # print(timestamp[-10:])
                signal = Signal(samples=np.array(df_100ms[signal_structure.signal_col_name],
                                                 dtype=df_100ms[signal_structure.signal_col_name].dtypes),
                                timestamps=timestamp,
                                name=signal_structure.signal_col_name,
                                unit='')
                # print(signal)
                signals_list_100ms.append(signal)

            if signal_structure.sample_rate == 500:
                timestamp = np.array(df_500ms[signal_structure.time_col_name], dtype='float64')
                # print(tup[0])
                #print(timestamp[-10:])

                signal = Signal(samples=np.array(df_500ms[signal_structure.signal_col_name],
                                                 dtype=df_500ms[signal_structure.signal_col_name].dtypes),
                                timestamps=timestamp,
                                name=signal_structure.signal_col_name,
                                unit='')
                # print(signal)
                signals_list_500ms.append(signal)

        # create empty MDf version 4.00 file
        with (MDF(version='4.10') as mdf4):
            # append the signals to the new file
            mdf4.append(signals_list_100ms, comment='imported')
            mdf4.append(signals_list_500ms, comment='imported')

            # mdf4.start_time = start_time.to_pydatetime()  # datetime.fromisoformat("2024-08-06 17:00:00")
            # save new file
            if use_same_input_file_name == True:
                out_filename = input_file_path[:-4] + ".mf4"
            else:
                out_filename = output_file_name
                print("error - use_same_input_file_name == False")
                # mdf4.save(path + filename + ".mf4", overwrite=True)
            # print(out_filename)
            mdf4.save(out_filename, overwrite=True)
            print("====> Conversione completata <====")
