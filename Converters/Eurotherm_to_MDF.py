import logging
from openpyxl import load_workbook
from asammdf import MDF, Signal
import numpy as np
import pandas as pd
from numpy import array as np_array
from Classes.Dataframe_to_MDF import Dataframe_to_MDF


class Eurotherm_to_MDF:


    @staticmethod
    def fix_df_dtype(df):
        for col_name in df.columns:
            unique_types = df[col_name].map(type).unique()
            print(f"Column {col_name} has types: {unique_types}")
            if col_name != 'Time_rel[s]' and col_name != 'Time':
                if len(unique_types) == 1:
                    if df[col_name].dtypes == 'str':
                        # df[col_name] = df[col_name].str.replace(',', '.')
                        # df[col_name] = df[col_name].str.replace(' ', '')
                        #### REMOVE ALL UNECESSARY SPACES
                        df[col_name] = df[col_name].str.strip()
                        df[col_name] = pd.to_numeric(df[col_name], errors='coerce')
                    elif df[col_name].dtypes == 'object':
                        # print(df[col_name].dtypes)
                        # print((type(df[col_name])))
                        df[col_name] = df[col_name].str.strip()
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
                    df[col_name] = df[col_name].str.strip()
                    df[col_name] = df[col_name].str.replace(',', '.')
                    df[col_name] = df[col_name].str.replace(' ', '')
                    df[col_name] = pd.to_numeric(df[col_name], errors='coerce')
                    # df[col_name] = df[col_name].str.replace(',', '.').astype(float)
        return df





    # -------------------
    # START CONFIGURATION
    # -------------------
    @staticmethod
    def exec_conversion(input_file_list, use_same_input_file_name, output_file_name):
        print(input_file_list)
        dataframe_list = []
        nome_gruppo_list = []
        header_line_number = 0
        for input_file_path in input_file_list:
            print(f"Convert Eurotherm_ file {input_file_path}")

            # Open the file
            with open(input_file_path, 'r') as file:
                # Read each line in the file, with line number starting at 1
                for line_number, line in enumerate(file, start=1):
                    # Check if the line starts with "n°Campione"
                    #print(line.lower())
                    if line.startswith('"Nome Gruppo"'):
                        key, value = [part.strip('"') for part in line.split('\t')]
                        parsed = {key: value}
                        #print(parsed)
                        nome_gruppo = parsed["Nome Gruppo"].replace('\t', '').replace('"', '').replace(' ', '_').strip()
                        nome_gruppo_list.append(nome_gruppo)

                    if line.lower().startswith('"date/ora"'):
                        header_line_number = line_number
                        print(f"First line that starts with 'Date/Ora' found at row {header_line_number}:")
                        print(line.strip())  # Print the line without extra spaces or newlines
                        break  # Stop after finding the first match
            headers = []
            units = []
            with open(input_file_path, 'r') as file:
                # Read each line in the file, with line number starting at 1
                for line_number, line in enumerate(file, start=1):
                    if line_number == header_line_number:
                        headers = parts = [p.strip().strip('"') for p in line.split('\t') if p.strip() != ""]
                        print(headers)
                    if line_number == header_line_number+1:
                        #print(line.strip())
                        units = parts = [p.strip().strip('"') for p in line.split('\t') if p.strip() != ""]
                        print(units)
                        break

            merged_headers = [
                f"{h} [{u}]" if u else h
                for h, u in zip(headers, units + [""] * (len(headers) - len(units)))
            ]
            print(merged_headers)

            merged_headers = [
                f"{h} ({u})" if u else h
                for h, u in zip(headers, units + [""] * (len(headers) - len(units)))
            ]

            # Create a list to ignore all the header rows and the unit row
            ignore_list = list(range(0, header_line_number-1))
            ignore_list.append(header_line_number)
            print(f"ignore_list {ignore_list}")


            #### READ CSV FILE
            df = pd.read_csv(input_file_path, sep="\t",
                             skiprows=ignore_list,
                             decimal=",",
                             # nrows=10,
                             encoding="latin1")

            df.columns = df.columns.str.strip()

            print(df.head(10))

            #### DROP UNECESSARY COLUMNS
            columns_to_delete = []
            for col in df.columns:
                if col.lower().startswith('n°campione'):
                    columns_to_delete.append(col)
                if col.lower().startswith('unnamed'):
                    columns_to_delete.append(col)

            df = df.drop(columns=columns_to_delete)
            #print(df.head(10))

            df = df.rename(columns={"Date/Ora": "Data_Ora"})
            #print(df.head(2))

            # Inserimento di una colonna "time" con valori in 'datetime'
            #df.insert(1, 'time', pd.to_datetime(df[df.columns["Data_Ora"]],format="%d.%m.%Y %H:%M:%S,%f"))

            df.insert(1, "Time",  pd.to_datetime(df["Data_Ora"], format="%d/%m/%y %H:%M:%S"))

            start_time = df['Time'].iloc[0]
            # print(df.head(10))
            # Inserimento di una colonna "relative_time" con valori in 'datetime'
            df.insert(2, 'Time_rel[s]', df['Time'] - start_time)

            # print(df.head(10))

            df = df.drop(columns=["Data_Ora"])

            #### FIX MIXED TYPES
            df.replace(" ", np.nan, inplace=True)
            # print("shape before NAN dropping:", df.shape)
            df = df.dropna()
            # print("shape after NAN dropping:", df.shape)

            df = Eurotherm_to_MDF.fix_df_dtype(df)

            dataframe_list.append(df)

        print(len(dataframe_list))
        print(dataframe_list[0].head(5))

        # Concatenate all DataFrames in the list
        df_concat = pd.concat(dataframe_list, ignore_index=True)
        print(df_concat.head(5))

        df_concat = df_concat.sort_values(by="Time").reset_index(drop=True)
        start_time = df_concat['Time'].iloc[0]
        df_concat = df_concat.drop(columns=["Time_rel[s]"])
        # print(df.head(10))
        # Inserimento di una colonna "relative_time" con valori in 'datetime'
        df_concat.insert(2, 'Time_rel[s]', df_concat['Time'] - start_time)

        # print(df.head(10))

        output_file_name = ""
        parts = input_file_list[0].split("/")
        #print(parts)
        if len(parts) > 1:
            output_file_name = ("/".join(parts[:-1])) + "/" + nome_gruppo_list[0] + ".mf4"
            print("output_file_name: ", output_file_name)
        else:
            print("input_file_path has no path")
            exit()

        #for df in dataframe_list:
        signal_name_list = [x for x in df_concat.columns if (x != "Time_rel[s]" and x != 'Time')]
        #############  creare asse dei tempi #############
        timestamps = np_array(df_concat["Time_rel[s]"].dt.total_seconds())

        ############# ## STEP2 : creare i segnali effettivi dal dataframe #############
        signals_list = []
        for col_name in signal_name_list:
            signal = Signal(samples=np_array(df_concat[col_name], dtype=df_concat[col_name].dtypes),
                            timestamps=timestamps, name=col_name, unit='')
            signals_list.append(signal)
            #print(df[col_name].dtypes, signal)

        # create empty MDf version 4.00 file
        with (MDF(version='4.10') as mdf4):
            # append the signals to the new file
            mdf4.append(signals_list, comment='imported')
            mdf4.start_time = start_time
            # save new file
            mdf4.save(output_file_name, overwrite=True)