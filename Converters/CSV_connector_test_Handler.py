import logging
import math

from openpyxl import load_workbook

from asammdf import MDF, Signal
import numpy as np

import matplotlib.pyplot as plt
import pandas as pd


class CSV_connector_test_Handler:
    @staticmethod
    def exec_conversion(input_file_list, use_same_input_file_name, output_file_name):
        test_ongoing = "45_pin_expression_force"
        application = "WUP50"

        # carica il file
        df_list = []
        for file in input_file_list:
            df = pd.read_csv(
                file,
                sep=";",  # separatore corretto
                decimal=",",  # virgola come decimale
                skiprows=3  # salta header non standard
            )
            df = df.iloc[:, :-2]
            df.columns = ["Forza[N]", "Distanza[mm]", "Tempo[min]"]
            df["Tempo[sec]"] = (df["Tempo[min]"] * 60).round(2)
            if application == "WUP50" and test_ongoing == "45_pin_expression_force":
                df_list.append((df, file[-9:-6]+"_pin"+file[-5:-4]))
            else:
                df_list.append((df, file[-7:-4]))

            # print(df.head(2))
            # print(name)




        if application == "WUP50" and test_ongoing == "45_pin_expression_force":

            for df, name in df_list:
                if name == "g19_pin3":
                    df["Forza[N]"] = df["Forza[N]"]*100/120

            fig, ax1 = plt.subplots()
            #ax12 = ax1.twinx()  # asse a destra

            for df, name in df_list:
                max_dist = df.max()
                #df['Distanza_norm'] = df['Distanza[mm]'] / df['Distanza[mm]'].max()
                df_force_great = df #df[df["Distanza[mm]"] > 0] #df[df["Forza[N]"] > 20]
                ax1.plot(df_force_great["Tempo[sec]"],df_force_great["Forza[N]"],label=f"{name}")
                #ax12.plot(df_force_great["Tempo[sec]"], df_force_great["Distanza[mm]"],linestyle="--",label=f"{name}")


            # etichette assi
            ax1.set_xlabel("Tempo [sec]")
            ax1.set_ylabel("Forza [N]")
            #ax12.set_ylabel("Distanza [mm]")

            # griglia (solo su asse principale)
            ax1.grid()
            # legenda combinata (importantissimo!)
            lines_1, labels_1 = ax1.get_legend_handles_labels()
            #lines_2, labels_2 = ax12.get_legend_handles_labels()

            #ax1.legend(lines_1 + lines_2, labels_1 + labels_2)
            ax1.legend(lines_1, labels_1)

            plt.show()


            fig2, ax2 = plt.subplots()
            for df, name in df_list:
                df_force_pos = df

                #df_force_pos = df[df["Forza[N]"] > 0]
                #df_force_pos = df[df["Distanza[mm]"] > -2]
                val = df.loc[df['Forza[N]'].idxmax(), 'Tempo[sec]']

                df_force_pos = df[df["Tempo[sec]"] < val+10] #df[df["Forza[N]"] > 20]


                ax2.plot(df_force_pos["Distanza[mm]"], df_force_pos["Forza[N]"], label=name)
                ax2.set_xlabel("Distance[mm]")
                ax2.set_ylabel("Force[N]")
                ax2.grid(True)
                ax2.legend()

            plt.show()



        else:
            #######################################################
            #
            # OLDER VERSION OF THE CODE
            #
            #######################################################
            x = np.linspace(0, 10, 100)
            push_test = False
            push_streght_test = True
            pull_off = False

            fig, ax1 = plt.subplots()
            ax12 = ax1.twinx()  # asse a destra



            for df, name in df_list:
                if name == "A70":
                    df["Tempo[sec]"] = df["Tempo[sec]"] + 8
                max_dist = df.max()
                #df['Distanza_norm'] = df['Distanza[mm]'] / df['Distanza[mm]'].max()
                df_force_great = df #df[df["Distanza[mm]"] > 0] #df[df["Forza[N]"] > 20]
                ax1.plot(df_force_great["Tempo[sec]"],df_force_great["Forza[N]"],label=f"{name}")
                ax12.plot(df_force_great["Tempo[sec]"], df_force_great["Distanza[mm]"],linestyle="--",label=f"{name}")

            # etichette assi
            ax1.set_xlabel("Tempo [sec]")
            ax1.set_ylabel("Forza [N]")
            ax12.set_ylabel("Distanza [mm]")

            # griglia (solo su asse principale)
            ax1.grid()

            # legenda combinata (importantissimo!)
            lines_1, labels_1 = ax1.get_legend_handles_labels()
            lines_2, labels_2 = ax12.get_legend_handles_labels()

            ax1.legend(lines_1 + lines_2, labels_1 + labels_2)

            plt.show()

            fig2, ax2 = plt.subplots()
            for df, name in df_list:
                if name == "A70":
                    df["Distanza[mm]"] = df["Distanza[mm]"] + 5
                df_force_pos = df

                #df_force_pos = df[df["Forza[N]"] > 0]
                #df_force_pos = df[df["Distanza[mm]"] > -2]
                val = df.loc[df['Forza[N]'].idxmax(), 'Tempo[sec]']

                df_force_pos = df[df["Tempo[sec]"] < val+10] #df[df["Forza[N]"] > 20]


                ax2.plot(df_force_pos["Distanza[mm]"], df_force_pos["Forza[N]"], label=name)
                ax2.set_xlabel("Distance[mm]")
                ax2.set_ylabel("Force[N]")
                ax2.grid(True)
                ax2.legend()

            plt.show()


            if push_test == True:
                fig3, axes3 = plt.subplots(3, 2, figsize=(10, 6))
                axes3 = axes3.flatten()
                for i, ax in enumerate(axes3):

                    df, name = df_list[i]
                    df_force_pos = df[df["Forza[N]"] > 1]
                    df_force_pos = df_force_pos[df_force_pos["Forza[N]"] < 80]
                    max_dist = math.ceil(df['Distanza[mm]'].max())
                    max_dist = df['Distanza[mm]'].max()

                    ax.plot(df_force_pos["Distanza[mm]"], df_force_pos["Forza[N]"], label=name)
                    ax.set_ylabel('Force[N]', color='b')
                    ax.set_xlabel('Distance[mm]', color='b')

                    ax.set_xlim(0, max_dist)
                    ax.set_xticks(np.arange(0, max_dist, 1))
                    ax.set_ylim(0, 80)
                    ax.axhline(y=75, color='red', linestyle='--', linewidth=2)
                    # ax.set_grid(True)

            if push_streght_test == True:

                fig4, axes4 = plt.subplots(3, 2, figsize=(10, 6))
                axes4 = axes4.flatten()
                for i, ax in enumerate(axes4):
                    df, name = df_list[i]
                    df_force_pos = df[df["Forza[N]"] > 1]
                    df_force_pos = df[df["Distanza[mm]"] > -2]

                    max_dist = math.ceil(df['Distanza[mm]'].max())
                    max_dist = df['Distanza[mm]'].max()

                    ax.plot(df_force_pos["Distanza[mm]"], df_force_pos["Forza[N]"], label=name)
                    ax.set_ylabel('Force[N]', color='b')
                    ax.set_xlabel('Distance[mm]', color='b')

                '''
                # Secondo asse (destra)
                ax2 = ax.twinx()
                ax2.plot(x, y2, 'r', label='cos')
                ax2.set_ylabel('cos', color='r')
                '''
                ax.set_title(f"{name}")

            plt.tight_layout()
            plt.show()


            '''
            ax2.figure(2)
            ax1.plot(df["Tempo[sec]"], df["Forza[N]"], label=file[-7:-4])
            ax2.plot(df["Tempo[sec]"], df["Distanza[mm]"], label=file[-7:-4])
            ax1.xlabel("Tempo[sec]")
            ax2.ylabel("Forza[N]")
            ax2.ylabel("Forza[N]")
            ax2.grid(True)
            plt.legend()
            plt.show()
    
        # etichette assi
        ax1.set_xlabel("Tempo [sec]")
        ax1.set_ylabel("Forza [N]")
        ax2.set_ylabel("Distanza [mm]")
    
        # griglia (solo su asse principale)
        ax1.grid()
    
        # legenda combinata (importantissimo!)
        lines_1, labels_1 = ax1.get_legend_handles_labels()
        lines_2, labels_2 = ax2.get_legend_handles_labels()
    
        ax1.legend(lines_1 + lines_2, labels_1 + labels_2)
    
        plt.title("Forza e Distanza vs Tempo")
        plt.show()
        '''

