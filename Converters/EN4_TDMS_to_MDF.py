from asammdf import MDF, Signal
import pandas as pd
from nptdms import TdmsFile
import xml.etree.ElementTree as ET

from numpy import array as np_array
from pandas import Timestamp


class EN4_TDMS_to_MDF:
    @staticmethod
    def exec_conversion(input_file_list, use_same_input_file_name, output_file_name):
        if len(input_file_list) == 0:
            print("Error")

        for input_file in input_file_list:
            # Carica il file TDMS
            print("file ", input_file)
            tdms_file = TdmsFile.read(input_file)

            # Crea un DataFrame combinando tutti i gruppi e canali
            data_frames = []
            print(tdms_file.properties)
            # Itera su ogni gruppo e canale nel file TDMS
            for group in tdms_file.groups():
                for channel in group.channels():
                    # Estrae i dati del canale e converte in DataFrame
                    df_channel = channel.as_dataframe()
                    df_channel.columns = [f"{group.name}_{channel.name}"]  # Rinomina colonne per evitare conflitti
                    data_frames.append(df_channel)
                    #start_time = channel.properties['wf_start_time']
                    #increment = channel.properties['wf_increment']
                    #offset = channel.properties['wf_start_offset']
                    #log_freq_used = channel.properties['log freq used [Hz]']
                    #number_of_sample = channel.properties['wf_samples']
                    print(channel.properties)

                    #print(timestamp)
                    #print(timestamp)

            # print(type(data_frames))
            # print(len(data_frames))
            # for df in data_frames:
            #    #print(type(df))

            # Combina tutti i DataFrame in uno solo
            final_df = pd.concat(data_frames, axis=1)
            columns = final_df.columns
            if "ls_Time2" not in columns:
                print("ls_Time2 not present")
                print(columns)

            if "ls_Time" not in columns:
                print("ls_Time not present")
                print(columns)

                # print(final_df.shape)

            filtered_df = final_df#[['ls_Time', 'ls_Time2', 'ls_EncBenchPos']]
            df_small = filtered_df

            start_time = df_small['DateTime_Unbenannt'].iloc[0]

            # Inserimento di una colonna "relative_time" con valori in 'datetime'
            df_small.insert(2, 'relative_time', df_small['DateTime_Unbenannt'] - start_time)

            df_small["relative_time"] = df_small["relative_time"] / (1000 * 1000 * 1000)
            df_small.to_csv("temp.csv")
            print(df_small)
            for i in range(0, 20):
                #print("ls_Time2", df_small["ls_Time2"][i]/1000/1000/1000)
                pass

            ## Funzione per la gestione della data (se esiste la colonna "Time")
            # def custom_date_parser_tdmsfile(date_string):
            #    return pd.to_datetime(date_string, format="%Y/%m/%d %H:%M:%S.%f")

            signal_name_list = [x for x in df_small.columns if x not in ['ls_Time','ls_Time2','relative_time', "DateTime_Unbenannt"]]

            #############  creare asse dei tempi #############
            timestamps = np_array(df_small["relative_time"])
            import numpy as np
            import matplotlib.pyplot as plt

            #plt.plot(timestamps)
            #plt.title("Valori dell'array")
            #plt.xlabel("Indice")
            ##plt.ylabel("Valore")
            #plt.show()
            ############# ## STEP2 : creare i segnali effettivi dal dataframe #############
            signals_list = []
            for col_name in signal_name_list:
                signal = Signal(samples=np_array(df_small[col_name], dtype=df_small[col_name].dtypes),
                                timestamps=timestamps, name=col_name, unit='')
                signals_list.append(signal)

            # create empty MDf version 4.00 file
            with (MDF(version='4.10') as mdf4):
                # append the signals to the new file
                mdf4.append(signals_list, comment='imported')
                start_time = 0
                #mdf4.start_time = start_time.to_pydatetime()  # datetime.fromisoformat("2024-08-06 17:00:00")

                output_file_name_ = input_file[:-4] + ".mf4"
                # save new file
                mdf4.save(output_file_name_, overwrite=True)
