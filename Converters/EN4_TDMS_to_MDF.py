from asammdf import MDF, Signal
import pandas as pd
import numpy as np
from nptdms import TdmsFile
import xml.etree.ElementTree as ET

from numpy import array as np_array
from pandas import Timestamp


class EN4_TDMS_to_MDF:
    @staticmethod
    def exec_conversion(input_file_list, use_same_input_file_name, output_file_name, verbose=True):
        if len(input_file_list) == 0:
            print("Error input_file_list length")

        for input_file in input_file_list:
            # Carica il file TDMS
            print("input_file ", input_file)
            tdms_file = TdmsFile.read(input_file)

            # Crea un DataFrame combinando tutti i gruppi e canali
            data_frames = []
            first_processed_frame = True
            TDMS_start_time = None
            TDMS_increment = None
            TDMS_offset = None
            TDMS_log_freq_max = None
            TDMS_log_freq_used = None
            TDMS_number_of_sample = None
            # print(tdms_file.properties)
            # Itera su ogni gruppo e canale nel file TDMS
            for group in tdms_file.groups():
                print("group.name ", group.name)  # Prints "group name"
                for channel in group.channels():
                    if first_processed_frame:
                        TDMS_start_time = channel.properties['wf_start_time']
                        TDMS_increment = channel.properties['wf_increment']
                        TDMS_offset = channel.properties['wf_start_offset']
                        TDMS_log_freq_max = channel.properties['log freq max[Hz]']
                        TDMS_log_freq_used = channel.properties['log freq used [Hz]']
                        TDMS_number_of_sample = channel.properties['wf_samples']
                        first_processed_frame = False
                    else:
                        if TDMS_start_time != channel.properties['wf_start_time']:
                            print(f" WARNING : Channel {channel.name} has different start time wrt other channels")
                        if TDMS_increment != channel.properties['wf_increment']:
                            print(f" WARNING : Channel {channel.name} has different 'increment' wrt other channels")
                        if TDMS_offset != channel.properties['wf_start_offset']:
                            print(f" WARNING : Channel {channel.name} has different 'offset' wrt other channels")
                        if TDMS_log_freq_max != channel.properties['log freq max[Hz]']:
                            print(f" WARNING : Channel {channel.name} has different 'log freq max' wrt other channels")
                        if TDMS_log_freq_used != channel.properties['log freq used [Hz]']:
                            print(f" WARNING : Channel {channel.name} has different 'log freq used' wrt other channels")
                        if TDMS_number_of_sample != channel.properties['wf_samples']:
                            print(f" WARNING : Channel {channel.name} has different samples number wrt other channels")

                    # Estrae i dati del canale e converte in DataFrame
                    df_channel = channel.as_dataframe()
                    unit_string = channel.properties['unit_string']
                    df_channel.columns = [
                        f"{group.name}_{channel.name}[{unit_string}]"]  # Rinomina colonne per evitare conflitti
                    data_frames.append(df_channel)

            if verbose:
                print(f"TDMS_start_time: ", TDMS_start_time)
                print(f"TDMS_increment: ", TDMS_increment)
                print(f"TDMS_number_of_sample: ", TDMS_number_of_sample)

            if TDMS_log_freq_used != TDMS_log_freq_max:
                print(f" WARNING : TDMS_log_freq_max ({TDMS_log_freq_max}) is different than TDMS_log_freq_used ({TDMS_log_freq_used})")
            if TDMS_log_freq_used != 1/TDMS_increment:
                print(f" WARNING : TDMS_log_freq_used ({TDMS_log_freq_used}) does not match with TDMS_increment ({TDMS_increment})")


            final_df = pd.concat(data_frames, axis=1)
            if verbose:
                print(final_df.columns)

            if "ls_Time[ms]" in final_df.columns:
                final_df.drop(columns=["ls_Time[ms]"], inplace=True)

            if "ls_Time2[s]" in final_df.columns:
                final_df.drop(columns=["ls_Time2[s]"], inplace=True)

            if verbose:
                print(f"Dataframe shape: {final_df.shape}")

            final_df.to_csv("temp.csv")
            # print(df_small)

            ## Funzione per la gestione della data (se esiste la colonna "Time")
            # def custom_date_parser_tdmsfile(date_string):
            #    return pd.to_datetime(date_string, format="%Y/%m/%d %H:%M:%S.%f")

            signal_name_list = [x for x in final_df.columns if x not in ['ls_Time', 'ls_Time2', 'relative_time']]

            ############# ## STEP1 : creare asse dei tempi #############
            TDMS_duration = TDMS_increment*TDMS_number_of_sample
            if verbose:
                print(f"TDMS_duration: ", TDMS_duration)

            timestamps = np.arange(start=0, stop=TDMS_duration, step=TDMS_increment)
            if len(timestamps) != TDMS_number_of_sample:
                print(f" WARNING : TDMS_number_of_sample ({TDMS_number_of_sample}) != does not match with TDMS_increment ({TDMS_increment})")

            ############# ## STEP2 : creare i segnali effettivi dal dataframe #############
            signals_list = []
            for col_name in signal_name_list:
                signal = Signal(samples=np_array(final_df[col_name], dtype=final_df[col_name].dtypes),
                                timestamps=timestamps, name=col_name, unit='')
                signals_list.append(signal)

            # create empty MDf version 4.00 file
            with (MDF(version='4.10') as mdf4):
                # append the signals to the new file
                mdf4.append(signals_list, comment='imported')
                start_time = 0
                # mdf4.start_time = start_time.to_pydatetime()  # datetime.fromisoformat("2024-08-06 17:00:00")

                output_file_name_ = input_file[:-5] + ".mf4"
                # save new file
                mdf4.save(output_file_name_, overwrite=True)

                print("File saved")
