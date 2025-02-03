import logging
from openpyxl import load_workbook

from asammdf import MDF, Signal
import numpy as np
import pandas as pd
from collections import namedtuple

from Classes.Dataframe_to_MDF import Dataframe_to_MDF


class DielectriK_to_MDF:
    def __init__(self):
        pass

    @staticmethod
    def fix_df_dtype(df):
        for col_name in df.columns:
            unique_types = df[col_name].map(type).unique()
            # print(f"Column {col_name} has types: {unique_types}")

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
    def exec_conversion(input_file_path, use_same_input_file_name, output_file_name):
        print("Convert Dielectrik file")
        print(input_file_path)

        # Open the file
        with open(input_file_path, 'r') as file:
            # Read each line in the file, with line number starting at 1
            for line_number, line in enumerate(file, start=0):
                # Check if the line starts with "n°Campione"
                # print(line.lower())
                if line.lower().startswith('n°campione'):
                    print(f"First line that starts with 'n°Campione' found at row {line_number}:")
                    print(line.strip())  # Print the line without extra spaces or newlines
                    break  # Stop after finding the first match

        # Create a list to ignore all the header rows
        ignore_list = list(range(0, line_number))
        ignore_list.append(line_number + 1)
        #print(ignore_list)

        #### READ CSV FILE
        df = pd.read_csv(input_file_path, sep="\t",
                         skiprows=ignore_list,
                         #nrows=10,
                         encoding="latin1")

        df.columns = df.columns.str.strip()

        #### DROP UNECESSARY COLUMNS
        columns_to_delete = []
        for col in df.columns:
            if col.lower().startswith('n°campione'):
                columns_to_delete.append(col)
            if col.lower().startswith('unnamed'):
                columns_to_delete.append(col)

        df = df.drop(columns=columns_to_delete)

        #### FIX MIXED TYPES
        df.replace(" ", np.nan, inplace=True)
        #print("shape before NAN dropping:", df.shape)
        df = df.dropna()
        #print("shape after NAN dropping:", df.shape)

        df = DielectriK_to_MDF.fix_df_dtype(df)

        #### RENAME TO THE CORRECT FILE NAME
        # Rename 'old_name' to 'new_name'
        df = df.rename(columns={'tempo(S)': 'Time[s]'})

        output_file_name = ""
        parts = input_file_path.split(".")
        if len(parts) > 1:
            output_file_name = (".".join(parts[:-1])) + ".mf4"
            #print("output_file_name: ", output_file_name)
        else:
            print("input_file_path has no extension")
            exit()

        #print("df.columns post rename", df.columns)
        Dataframe_to_MDF.save_to_mdf(dataframe_list=[df], output_file_name=output_file_name)

