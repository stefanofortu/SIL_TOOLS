from libraries.dewesoft_library.DWDataReaderHeader import *
import ctypes
import sys
import os
############### TIME CONVERSION #################################
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from libraries.dewesoft_library.DWDataReaderClass import DWDataReader
import numpy as np
import pandas as pd


class Dewesoft_Converter(DWDataReader):
    def __init__(self, verbose=False):
        super().__init__(verbose=verbose)
        self.DW_start_time = None
        self.DW_sample_rate_ms = None
        self.DW_duration_s = None
        self.DW_number_of_sample = None
        self.DW_channels_number = None

    def check_file_vs_measurement_info(self):
        #print("Checking measurement info: ")

        measurement_info = DWMeasurementInfo(0, 0, 0, 0)
        check_error(self.lib, self.lib.DWIGetMeasurementInfo(self.reader_instance, ctypes.byref(measurement_info)))

        if self.file_info.sample_rate != measurement_info.sample_rate:
            print("ERROR: file_info.sample_rate != measurement_info.sample_rate")
        self.DW_sample_rate_ms = self.file_info.sample_rate
        # print(f"Sample rate [ms]: {self.DW_sample_rate_ms}")

        if self.file_info.start_store_time != measurement_info.start_measure_time:
            print("ERROR: file_info.start_store_time != measurement_info.start_measure_time")

        if self.file_info.start_store_time != measurement_info.start_store_time:
            print("ERROR: file_info.start_store_time != measurement_info.start_store_time")

        if measurement_info.start_store_time != measurement_info.start_measure_time:
            print("ERROR: measurement_info.start_store_time != measurement_info.start_measure_time")

        self.DW_start_time = self.dewesoft_to_local_time_conversion(measurement_info.start_store_time)
        # print(f"Start store local time: {self.DW_start_time}")

        if self.file_info.duration != measurement_info.duration:
            print("ERROR: file_info.duration != measurement_info.duration")
        self.DW_duration_s = self.file_info.duration
        # print(f"Duration: {self.DW_duration_s}")

        if not (self.DW_duration_s * 1000 / self.DW_sample_rate_ms).is_integer():
            print("Error in DW_number_of_sample creation")
        else:
            self.DW_number_of_sample = int(self.DW_duration_s * 1000 / self.DW_sample_rate_ms)

        ch_count = ctypes.c_int()
        check_error(self.lib, self.lib.DWIGetChannelListCount(self.reader_instance, ctypes.byref(ch_count)))
        self.DW_channels_number = ch_count.value
        # print("Channel count:", DW_channels_number)
        print(f"DW File info:{self.DW_channels_number} channels stored at {int(1000/(self.DW_sample_rate_ms))} Hz "
              f"for {self.file_info.duration} s ({self.DW_number_of_sample} each channel)."
              f"Start measurement at {self.DW_start_time}")

    def to_pandas(self, verbose=False):
        ########## CHECK IF FILE IS OK #1 ###########################
        self.check_file_vs_measurement_info()

        ########## BUILT TIMESTAMP ###########################
        timestamps_relative = np.arange(0, self.DW_duration_s, self.DW_sample_rate_ms / 1000)
        dw_dataframe = pd.DataFrame({'Time[s]': timestamps_relative})
        dw_dataframe['Time[s]'] = dw_dataframe['Time[s]'].round(3)
        dw_dataframe['time_S'] = pd.to_timedelta(dw_dataframe['Time[s]'], unit='seconds')  # e.g. '14:30:00'
        dw_dataframe.insert(0, 'timestamp', self.DW_start_time + dw_dataframe['time_S'])
        dw_dataframe.drop(['time_S'], axis=1, inplace=True)

        channel_count = ctypes.c_int()
        check_error(self.lib, self.lib.DWIGetChannelListCount(self.reader_instance, ctypes.byref(channel_count)))

        channel_list = (DWChannel * channel_count.value)()
        check_error(self.lib, self.lib.DWIGetChannelList(self.reader_instance, channel_list))

        for i in range(channel_count.value):
            ch = channel_list[i]

            if verbose:
                print(f" DATA FROM CHANNEL: ")
                print(f"Channel {ch.index}:")
                print(f"  Name: {decode_bytes(ch.name)}")
                print(f"  Unit: {decode_bytes(ch.unit)}")
                print(f"  Description: {decode_bytes(ch.description)}")
                print(f"  Color: {ch.color}")
                print(f"  Array size: {ch.array_size}")
                print(f"  Data type: {DWDataType(ch.data_type).name}")

            ch_name = decode_bytes(ch.name)
            data_type = self.get_channel_property(ch, DWChannelProps.DW_DATA_TYPE)
            ch_index = self.get_channel_property(ch, DWChannelProps.DW_CH_INDEX)
            ch_type = self.get_channel_property(ch, DWChannelProps.DW_CH_TYPE)
            ch_scale = self.get_channel_property(ch, DWChannelProps.DW_CH_SCALE)
            ch_offset = self.get_channel_property(ch, DWChannelProps.DW_CH_OFFSET)
            ch_longname = self.get_channel_property(ch, DWChannelProps.DW_CH_LONGNAME)

            if verbose:
                print(f" DATA FROM PROPERTIES: ")
                print(f"  Data type (from property): {data_type.name}")
                print(f"  Channel index (from property): {ch_index}")
                print(f"  Channel type (from property): {ch_type.name}")
                print(f"  Scale (from property): {ch_scale}")
                print(f"  Offset (from property): {ch_offset}")
                print(f"  Long name (from property): {ch_longname}")

            if not self.SKIP_XML_DUMP:
                ch_xml = self.get_channel_property(ch, DWChannelProps.DW_CH_XML)
                print(f"  XML (from property): {ch_xml}")

                ch_xmlprops = self.get_channel_property(ch, DWChannelProps.DW_CH_XMLPROPS)
                print(f"  XML properties (from property): {ch_xmlprops}")

            if verbose:
                self.print_channel_arrays(ch)

            sample_cnt = ctypes.c_longlong()
            check_error(self.lib,
                        self.lib.DWIGetScaledSamplesCount(self.reader_instance, ch.index, ctypes.byref(sample_cnt)))
            down_sampling = False
            down_sampling_constant = 1
            if sample_cnt.value != self.DW_duration_s * 1000 / self.DW_sample_rate_ms:
                print(f"Problem in sample count: Sample count in {ch_name}: {sample_cnt.value}, from file info {self.DW_number_of_sample}")
                if sample_cnt.value > self.DW_number_of_sample:
                    if (sample_cnt.value / self.DW_number_of_sample).is_integer():
                        down_sampling = True
                        down_sampling_constant = int(sample_cnt.value / self.DW_number_of_sample)
                        print(f"Downsampling applied for {ch_name} with value {down_sampling_constant}")

            total_count: int = sample_cnt.value * ch.array_size
            # noinspection PyTypeChecker,PyCallingNonCallable
            samples = (ctypes.c_double * total_count)()

            timestamps = None
            # if ch_type == DWChannelType.DW_CH_TYPE_ASYNC:
            #    timestamps = (ctypes.c_double * sample_cnt.value)()

            cmd_status = self.lib.DWIGetScaledSamples(self.reader_instance, ch.index, 0, sample_cnt, samples,
                                                      timestamps)
            if DWStatus(cmd_status) == DWStatus.DWSTAT_ERROR_CAN_NOT_SUPPORTED:
                print("CAN Channel is not stored decoded, skipping...")
                return
            check_error(self.lib, cmd_status)

            ###########################################################################
            #### Lettura Dati Dewesoft per input sincroni e singolo canale
            #### DWChannelType.DW_CH_TYPE_SYNC AND ch.array_size != 1
            ###########################################################################

            if ch_type != DWChannelType.DW_CH_TYPE_SYNC and ch.array_size != 1:
                print("ch_type != DWChannelType.DW_CH_TYPE_SYNC and ch.array_size != 1")
                exit()
            if verbose:
                for i in range(0, sample_cnt.value, 200):
                    print(f"  Value: {i} : {samples[i]:.2f}")

            # samples è un puntatore a un array di 4887 double
            # Sample_cnt.value è la sua lunghezza (4887)
            length = sample_cnt.value
            np_array = np.ctypeslib.as_array(samples, shape=(length,))

            if down_sampling:
                np_array = np_array[::down_sampling_constant]
            dw_dataframe[ch_name] = np_array

        return dw_dataframe

    def to_mdf(self, verbose=False):
        df = self.to_pandas(verbose=verbose)
        print("Conversion to mdf to be completed")

    @staticmethod
    def dewesoft_to_local_time_conversion(start_store_time):
        if not isinstance(start_store_time, float):
            print("DWDataReaderExample.py - dewesoft_to_local_time_conversion(): wrong input type")
        # Dewwsoft time is stored as the number of days since a specific epoch, 1899-12-30 (called "DELPHI_EPOCH")
        DELPHI_EPOCH = datetime(1899, 12, 30)
        datetime_from_delphi = DELPHI_EPOCH + timedelta(days=start_store_time)
        # print("datetime_from_delphi:", datetime_from_delphi.strftime("%Y-%m-%d %H:%M:%S %Z%z"))
        datetime_utc_time = datetime_from_delphi.replace(tzinfo=ZoneInfo("UTC"))
        datetime_local_time = datetime_utc_time.astimezone(ZoneInfo("Europe/Rome"))
        # print("datetime_local_time:", datetime_local_time.strftime("%Y-%m-%d %H:%M:%S %Z%z"))

        return datetime_local_time

if __name__ == "__main__":
    filename = "C:\\Users\\stefano.fortunati\\Desktop\\test_dewesoft.dxd"
    print("Loading file:", filename)

    dewesoft_converter = Dewesoft_Converter()
    dewesoft_converter.open(filename=filename)
    df1 = dewesoft_converter.to_pandas()
    dewesoft_converter.close()
