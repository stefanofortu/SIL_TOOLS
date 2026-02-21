from asammdf import MDF, Signal
import pandas as pd
import numpy as np
from nptdms import TdmsFile
import xml.etree.ElementTree as ET

from numpy import array as np_array
from pandas import Timestamp


class EDAG_TDMS_to_MDF:
    @staticmethod
    def exec_conversion(input_file_list, use_same_input_file_name, output_file_name, verbose=True):
        if len(input_file_list) == 0:
            print("Error input_file_list length")

        for input_file in input_file_list:
            # Carica il file TDMS
            # print("input_file ", input_file)
            tdms_file = TdmsFile.read(input_file)

            # Crea un DataFrame combinando tutti i gruppi e canali
            data_frames = []
            first_processed_frame = True
            first_samples_extracted = True
            TDMS_start_time = None
            TDMS_increment: float = None
            TDMS_offset = None
            TDMS_log_freq_max = None
            TDMS_log_freq_used = None
            TDMS_number_of_sample: int = None
            TDMS_real_number_of_sample: int = None
            if verbose:
                print(tdms_file.properties)
            # Itera su ogni gruppo e canale nel file TDMS
            for group in tdms_file.groups():
                if verbose:
                    print(f"Reading {group.name} data...")  # Prints "group name"
                    print("group.properties : ", group.properties, flush=True)
                for channel in group.channels():
                    print("channel.properties : ", channel.properties, flush=True)
                    channel = channel
                    if group.name != "DateTime":
                        # do a lot of additional checks, per tutti i canali tranne che DateTime
                        if first_processed_frame:
                            TDMS_start_time = channel.properties['wf_start_time']
                            TDMS_increment = channel.properties['wf_increment']
                            TDMS_offset = channel.properties['wf_start_offset']
                            TDMS_number_of_sample = channel.properties['wf_samples']
                            first_processed_frame = False
                        else:
                            if TDMS_start_time != channel.properties['wf_start_time']:
                                print(f" WARNING : Channel {channel.name} has different start time wrt other channels")
                            if TDMS_increment != channel.properties['wf_increment']:
                                print(f" WARNING : Channel {channel.name} has different 'increment' wrt other channels")
                            if TDMS_offset != channel.properties['wf_start_offset']:
                                print(f" WARNING : Channel {channel.name} has different 'offset' wrt other channels")
                            if TDMS_number_of_sample != channel.properties['wf_samples']:
                                print(
                                    f" WARNING : Channel {channel.name} has different samples number wrt other channels")

                    # Estrae i dati di questo canale, senza eccezioni e li converte in DataFrame
                    df_channel = channel.as_dataframe()

                    if group.name == "DateTime":
                        ch_name = "DateTime"
                    else:
                        ch_name = channel.name
                    print(f" The shape of the channel {ch_name} is {df_channel.shape[0]}")
                    channel_to_keep = True
                    # a causa di un baco nel timeframe di EDAG, wf_samples è sempre settato a 1
                    if first_samples_extracted:
                        TDMS_real_number_of_sample = df_channel.shape[0]
                        first_samples_extracted = False
                    else:
                        if TDMS_real_number_of_sample != df_channel.shape[0]:
                            print(
                                f" WARNING : Channel {channel.name} has different REAL sample number wrt other channels")
                            print(
                                f" Channel has {df_channel.shape[0]} samples, while number real of sample is {TDMS_real_number_of_sample}")
                            if df_channel.shape[0] % TDMS_real_number_of_sample == 0:
                                print(f"Channel is a multiple, it will be downsampled")
                                divider = int(df_channel.shape[0] / TDMS_real_number_of_sample)
                                df_channel = df_channel.iloc[::divider]
                                df_channel.reset_index(drop=True, inplace=True)
                                print(f" The shape of the channel {ch_name} has been changed to {df_channel.shape[0]}")
                            else:
                                channel_to_keep = False

                    # assegna nome alle colonne
                    if group.name == "DateTime":
                        df_channel.columns = ["DateTime"]
                    else:
                        try:
                            unit_string = channel.properties['unit_string']
                        except KeyError:
                            try:
                                unit_string = channel.properties['Einheit']
                            except KeyError:
                                raise KeyError("Neither 'unit_string' nor 'Einheit' found")
                        df_channel.columns = [
                            f"{group.name}_{channel.name}[{unit_string}]"]

                    if channel_to_keep:
                        data_frames.append(df_channel)

            if verbose:
                print(f"TDMS_start_time: ", TDMS_start_time)
                print(f"TDMS_increment: ", TDMS_increment)
                print(f"TDMS_number_of_sample: ", TDMS_number_of_sample)
                print(f"TDMS_real_number_of_sample: ", TDMS_real_number_of_sample)

            print("Number of signals to be converted: ", len(data_frames))
            final_df = pd.concat(data_frames, axis=1)
            if verbose:
                print(final_df.columns)

            # df_reduced = final_df.head(20)
            # print(df_reduced.head(5))
            # df_reduced.to_csv("df_reduced.csv")

            if "DateTime" in final_df.columns:
                final_df.drop(columns=["DateTime"], inplace=True)
                final_df['year'] = final_df['DateTime'].dt.year
                final_df['month'] = final_df['DateTime'].dt.month
                final_df['day'] = final_df['DateTime'].dt.day
                final_df['hours'] = final_df['DateTime'].dt.hour
                final_df['minutes'] = final_df['DateTime'].dt.minute
                final_df['seconds'] = final_df['DateTime'].dt.second
            # Compute relative time (timedelta) from the first sample
            if "DateTime" in final_df.columns:
                final_df['relative_seconds'] = (final_df['DateTime'] - final_df['DateTime'].iloc[0]).dt.total_seconds()

            # Convert timedelta64 to seconds
            #timestamps = final_df['relative_time'] / np.timedelta64(1, 's')

            #print(final_df['relative_seconds'])
            #exit()

            if verbose:
                print(f"Dataframe shape: {final_df.shape}")

            signal_name_list = [x for x in final_df.columns if x not in ["DateTime"]]

            ############# ## STEP1 : creare asse dei tempi #############
            TDMS_duration = TDMS_increment * TDMS_real_number_of_sample
            if verbose:
                print(f"TDMS_duration: ", TDMS_duration)

            timestamps = np.arange(start=0, stop=TDMS_duration, step=TDMS_increment)
            if "DateTime" in final_df.columns:
                timestamps = np.array(final_df['relative_seconds'])
            else:
                timestamps = np.arange(start=0, stop=TDMS_duration, step=TDMS_increment)

            if len(timestamps) != TDMS_real_number_of_sample:
                print(
                    f" WARNING : TDMS_number_of_sample ({TDMS_number_of_sample}) != does not match with TDMS_increment ({TDMS_increment})")
                return

            ############# ## STEP2 : creare i segnali effettivi dal dataframe #############
            signals_list = []
            for col_name in signal_name_list:
                signal = Signal(samples=np_array(final_df[col_name], dtype=final_df[col_name].dtypes),
                                timestamps=timestamps, name=col_name, unit='')
                signals_list.append(signal)


            # Convert characters to their ASCII integer codes

            #final_df['DateTime_str'] = final_df['DateTime'].astype(str)
            #final_df['DateTime_str'] = final_df['DateTime_str'].str.ljust(30)
            #data = np.array(final_df['DateTime_str'])
            #data_numeric = np.array([[ord(c) for c in row] for row in data], dtype=np.uint8)

            #sig = Signal(data_numeric, timestamps=timestamps, name='Channel_string',
            #             comment='String channel', encoding='latin-1')
            #signals_list.append(sig)
            # create empty MDf version 4.00 file
            with (MDF(version='4.10') as mdf4):
                # append the signals to the new file
                mdf4.append(signals_list, comment='imported')
                start_time = 0
                mdf4.start_time = pd.to_datetime(TDMS_start_time)
                output_file_name_ = input_file[:-5] + ".mf4"
                # save new file
                mdf4.save(output_file_name_, overwrite=True)

                print("File saved")
