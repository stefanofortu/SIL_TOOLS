import logging
from openpyxl import load_workbook
# from asammdf import MDF, Signal
import numpy as np
import pandas as pd
from numpy import array as np_array
import matplotlib.pyplot as plt

from Classes.Dataframe_to_MDF import Dataframe_to_MDF


class FRF_analysis:
    # -------------------
    # START CONFIGURATION
    # -------------------
    @staticmethod
    def exec_conversion(input_file_dataframe, folder_path):
        fig2, ax2 = plt.subplots()
        fig1, ax1 = plt.subplots()

        for index, row in input_file_dataframe.iterrows():
            df_data = pd.read_csv(
                filepath_or_buffer=f"{folder_path}{row['Run']:.0f}/{row['Filename']}.csv",
                sep=";",
                skiprows=28,
                # nrows=10
            )
            df_data = df_data.iloc[:, :3]
            df_data.columns = ["Frequency[Hz]", "Magnitude", "Phase"]
            # Convert to numeric
            df_data = df_data.astype(float)
            label = f"#{row['Run']:.0f}_{row['DE']}-{row['Sample']}_{row['Axis']}/{row['Direction']}_{row['Control']}"
            ax1.plot(df_data.iloc[:, 0], df_data["Magnitude"], color=row["Color"], label=label,
                     linestyle=row["Linestyle"], linewidth=row["Linewidth"])
            df_data["Phase2"] = df_data["Phase"]
            df_data.loc[df_data["Phase2"] < -90, "Phase2"] += 360
            # ax2.plot(df_data.iloc[:, 0], df_data["Phase"], color=row["Color"], label=label,
            #         linestyle=row["Linestyle"], linewidth=row["Linewidth"])
            ax2.plot(df_data.iloc[:, 0], df_data["Phase2"], color=row["Color"], label=label,
                     linestyle=row["Linestyle"], linewidth=row["Linewidth"])

        for f in [100, 200, 400, 440]:
            ax1.axvline(x=f, color="orange", linestyle="--", linewidth=1, alpha=0.8)
            ax2.axvline(x=f, color="orange", linestyle="--", linewidth=1, alpha=0.8)

        # Add rectangle: (x, y, width, height)

        from matplotlib.patches import Rectangle

        rect = Rectangle(
            (100, 0),  # bottom-left corner
            width=340,
            height=0.1,  # width, height
            linewidth=1,
            edgecolor='red',
            facecolor='red'
        )
        ax1.add_patch(rect)

        ax1.set_title("Magnitude")
        ax2.set_title("Phase")
        # Major grid (main lines)
        ax1.grid(True, which="major", linestyle="-", linewidth=0.8, alpha=0.8)
        # Minor grid (faint lines)
        ax1.minorticks_on()
        ax1.grid(True, which="minor", linestyle=":", linewidth=0.8, alpha=0.8)

        ax1.legend()
        ax2.legend()

        ax1.set_xscale("log")
        ax2.set_xscale("log")

        ax2.set_ylim(-90, 270)
        # Major grid (main lines)
        ax2.grid(True, which="major", linestyle="-", linewidth=0.8, alpha=0.8)
        # Minor grid (faint lines)
        ax2.minorticks_on()
        ax2.grid(True, which="minor", linestyle=":", linewidth=0.8, alpha=0.8)

        plt.show()


if __name__ == "__main__":
    # file_dictionary = {run: 11,
    # }
    folder_path = "//svrnas001.saleri.it/TestingRoom-Data/dati_report/2026/2026_01_05_0137/logger/new_RUN/"
    mapping_file = folder_path + "mapping.xlsx"
    df = pd.read_excel(mapping_file, sheet_name="mapping", engine="openpyxl")
    df_mapping = df[df["ToBeVisualized"] == "yes"]
    print(df_mapping.head())
    FRF_analysis.exec_conversion(input_file_dataframe=df_mapping, folder_path=folder_path)
