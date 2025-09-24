from libraries.dewesoft_library.DWDataReaderHeader import *
import ctypes


class DWDataReader:
    def __init__(self, verbose=False):
        self.file_info = DWFileInfo(0, 0, 0)
        self.lib = load_library()
        self.reader_instance = READER_HANDLE()

        self.MAX_SAMPLES_PER_CH = 10
        self.SKIP_XML_DUMP = True
        if verbose and self.MAX_SAMPLES_PER_CH >= 0:
            print(f"Max samples per channel limited to {self.MAX_SAMPLES_PER_CH}")

        if verbose and self.SKIP_XML_DUMP:
            print("XML dump will be skipped")

        ver_major = ctypes.c_int()
        ver_minor = ctypes.c_int()
        ver_patch = ctypes.c_int()
        check_error(self.lib,
                    self.lib.DWGetVersionEx(ctypes.byref(ver_major), ctypes.byref(ver_minor), ctypes.byref(ver_patch)))
        if verbose:
            print(f"Dewesoft Data Reader version: {ver_major.value}.{ver_minor.value}.{ver_patch.value}")

        check_error(self.lib, self.lib.DWICreateReader(ctypes.byref(self.reader_instance)))

    def open(self, filename, verbose=False):
        #print("Loading file:", filename)

        c_filename = ctypes.c_char_p(filename.encode())
        self.file_info = DWFileInfo(0, 0, 0)
        check_error(self.lib, self.lib.DWIOpenDataFile(self.reader_instance, c_filename, ctypes.byref(self.file_info)))
        if verbose:
            print("DWFile info: ")
            print(f"  Sample rate:      {self.file_info.sample_rate}")
            print(f"  Start store time: {self.file_info.start_store_time}")
            print(f"  Duration:         {self.file_info.duration}")


    def shows_all_info(self):
        print("DWFile info: ")
        print(f"  Sample rate:      {self.file_info.sample_rate}")
        print(f"  Start store time: {self.file_info.start_store_time}")
        print(f"  Duration:         {self.file_info.duration}")

        self.get_file_metadata()
        self.get_file_events()
        self.get_file_header_entries()

        self.get_file_channels()
        self.get_file_complex_channels()
        self.get_file_binary_channels()

    def close(self):
        check_error(self.lib, self.lib.DWICloseDataFile(self.reader_instance))
        check_error(self.lib, self.lib.DWIDestroyReader(self.reader_instance))

    def get_file_metadata(self):
        print("===")
        print(" File metadata: ")
        print("===")

        measurement_info = DWMeasurementInfo(0, 0, 0, 0)
        check_error(self.lib, self.lib.DWIGetMeasurementInfo(self.reader_instance, ctypes.byref(measurement_info)))
        print("DWMeasurement info: ")
        print(f"  Sample rate:        {measurement_info.sample_rate}")
        print(f"  Start measure time: {measurement_info.start_measure_time}")
        print(f"  Start store time:   {measurement_info.start_store_time}")
        print(f"  Duration:           {measurement_info.duration}")

        storing_type_c = ctypes.c_int(DWStoringType.ST_ALWAYS_FAST)
        check_error(self.lib, self.lib.DWIGetStoringType(self.reader_instance, ctypes.byref(storing_type_c)))
        storing_type = DWStoringType(storing_type_c.value)
        print("Storing type:", storing_type.name)

        ch_count = ctypes.c_int()

        check_error(self.lib, self.lib.DWIGetHeaderEntryCount(self.reader_instance, ctypes.byref(ch_count)))
        print("Header entry count:", ch_count.value)

        check_error(self.lib, self.lib.DWIGetChannelListCount(self.reader_instance, ctypes.byref(ch_count)))
        print("Channel count:", ch_count.value)

        check_error(self.lib, self.lib.DWIGetComplexChannelListCount(self.reader_instance, ctypes.byref(ch_count)))
        print("Complex channel count:", ch_count.value)

        check_error(self.lib, self.lib.DWIGetBinChannelListCount(self.reader_instance, ctypes.byref(ch_count)))
        print("Binary channel count:", ch_count.value)

    def get_file_events(self):
        print("===")
        print(" File events: ")
        print("===")

        event_count = ctypes.c_int()
        check_error(self.lib, self.lib.DWIGetEventListCount(self.reader_instance, ctypes.byref(event_count)))

        event_list = (DWEvent * event_count.value)()
        check_error(self.lib, self.lib.DWIGetEventList(self.reader_instance, event_list))

        for i in range(event_count.value):
            event = event_list[i]
            event_type = DWEventType(event.event_type)
            print(f"Event {i}:")
            print(f"  Type: {event_type.name}")
            print(f"  Timestamp: {event.time_stamp}")
            print(f"  Description: {decode_bytes(event.event_text)}")

    def get_file_header_entries(self):
        print("===")
        print(" File header entries: ")
        print("===")

        entry_count = ctypes.c_int()
        check_error(self.lib, self.lib.DWIGetHeaderEntryCount(self.reader_instance, ctypes.byref(entry_count)))

        header_entries = (DWChannel * entry_count.value)()
        check_error(self.lib, self.lib.DWIGetHeaderEntryList(self.reader_instance, header_entries))

        for i in range(entry_count.value):
            entry = header_entries[i]

            ENTRY_TEXT_MAX_LEN = 255
            entry_text = create_string_buffer('', ENTRY_TEXT_MAX_LEN)
            check_error(self.lib, self.lib.DWIGetHeaderEntryText(self.reader_instance, entry.index, entry_text,
                                                                 ENTRY_TEXT_MAX_LEN))

            print(f"Entry {i}:")
            print(f"  Name: {decode_bytes(entry.name)}")
            print(f"  Unit: {decode_bytes(entry.unit)}")
            print(f"  Value: {decode_bytes(entry_text.value)}")

    def get_channel_property(self, ch: DWChannel, property: DWChannelProps):
        buf_len_default = ctypes.c_int(INT_SIZE)
        buf_len = ctypes.c_int(INT_SIZE)
        if property == DWChannelProps.DW_CH_INDEX:
            check_error(self.lib,
                        self.lib.DWIGetChannelProps(self.reader_instance, ch.index, DWChannelProps.DW_CH_INDEX_LEN,
                                                    ctypes.byref(buf_len), ctypes.byref(buf_len_default)))
        elif property == DWChannelProps.DW_CH_LONGNAME:
            check_error(self.lib,
                        self.lib.DWIGetChannelProps(self.reader_instance, ch.index, DWChannelProps.DW_CH_LONGNAME_LEN,
                                                    ctypes.byref(buf_len), ctypes.byref(buf_len_default)))
        elif property == DWChannelProps.DW_CH_XML:
            check_error(self.lib,
                        self.lib.DWIGetChannelProps(self.reader_instance, ch.index, DWChannelProps.DW_CH_XML_LEN,
                                                    ctypes.byref(buf_len), ctypes.byref(buf_len_default)))
        elif property == DWChannelProps.DW_CH_XMLPROPS:
            check_error(self.lib,
                        self.lib.DWIGetChannelProps(self.reader_instance, ch.index, DWChannelProps.DW_CH_XMLPROPS_LEN,
                                                    ctypes.byref(buf_len), ctypes.byref(buf_len_default)))
            if buf_len.value == 0:
                return None
        elif property == DWChannelProps.DW_CH_SCALE or property == DWChannelProps.DW_CH_OFFSET:
            buf_len = ctypes.c_int(DOUBLE_SIZE)

        buff = create_string_buffer('', buf_len.value)
        p_buff = ctypes.cast(buff, ctypes.POINTER(ctypes.c_void_p))

        check_error(self.lib, self.lib.DWIGetChannelProps(self.reader_instance, ch.index, property, p_buff,
                                                          ctypes.byref(buf_len)))

        if property == DWChannelProps.DW_DATA_TYPE:
            data_type = ctypes.cast(p_buff, ctypes.POINTER(ctypes.c_int)).contents
            return DWDataType(data_type.value)
        if property == DWChannelProps.DW_CH_INDEX:
            ch_index = ctypes.cast(p_buff, ctypes.c_char_p)
            return decode_bytes(ch_index.value)
        if property == DWChannelProps.DW_CH_TYPE:
            ch_type = ctypes.cast(p_buff, ctypes.POINTER(ctypes.c_int)).contents
            return DWChannelType(ch_type.value)
        if property == DWChannelProps.DW_CH_SCALE:
            ch_scale = ctypes.cast(p_buff, ctypes.POINTER(ctypes.c_double)).contents
            return ch_scale.value
        if property == DWChannelProps.DW_CH_OFFSET:
            ch_offset = ctypes.cast(p_buff, ctypes.POINTER(ctypes.c_double)).contents
            return ch_offset.value
        if property == DWChannelProps.DW_CH_XML:
            ch_xml = ctypes.cast(p_buff, ctypes.c_char_p)
            return decode_bytes(ch_xml.value)
        if property == DWChannelProps.DW_CH_XMLPROPS:
            ch_xmlprops = ctypes.cast(p_buff, ctypes.c_char_p)
            return decode_bytes(ch_xmlprops.value)
        if property == DWChannelProps.DW_CH_LONGNAME:
            ch_longname = ctypes.cast(p_buff, ctypes.c_char_p)
            return decode_bytes(ch_longname.value)

        raise ValueError(f"Unsupported property: {property}")

    def print_array_info(self, ch: DWChannel, array_info: DWArrayInfo):
        print(f"Array {array_info.index}:")
        print(f"  Name: {decode_bytes(array_info.name)}")
        print(f"  Unit: {decode_bytes(array_info.unit)}")
        print(f"  Size: {array_info.size}")

        for i in range(array_info.size):
            ARR_VALUE_MAX_LEN = 255
            array_value = create_string_buffer('', ARR_VALUE_MAX_LEN)
            check_error(self.lib,
                        self.lib.DWIGetArrayIndexValue(self.reader_instance, ch.index, array_info.index, i, array_value,
                                                       ARR_VALUE_MAX_LEN))
            print(f"  Value {i}: {decode_bytes(array_value.value)}")

    def print_channel_arrays(self, ch: DWChannel):
        array_count = ctypes.c_int()
        check_error(self.lib, self.lib.DWIGetArrayInfoCount(self.reader_instance, ch.index, ctypes.byref(array_count)))

        array_list = (DWArrayInfo * array_count.value)()
        check_error(self.lib, self.lib.DWIGetArrayInfoList(self.reader_instance, ch.index, array_list))

        for i in range(array_count.value):
            array_info = array_list[i]
            self.print_array_info(ch, array_info)

    def print_channel_info(self, ch: DWChannel):
        print(f"Channel {ch.index}:")
        print(f"  Name: {decode_bytes(ch.name)}")
        print(f"  Unit: {decode_bytes(ch.unit)}")
        print(f"  Description: {decode_bytes(ch.description)}")
        print(f"  Color: {ch.color}")
        print(f"  Array size: {ch.array_size}")
        print(f"  Data type: {DWDataType(ch.data_type).name}")

        data_type = self.get_channel_property(ch, DWChannelProps.DW_DATA_TYPE)
        print(f"  Data type (from property): {data_type.name}")

        ch_index = self.get_channel_property(ch, DWChannelProps.DW_CH_INDEX)
        print(f"  Channel index (from property): {ch_index}")

        ch_type = self.get_channel_property(ch, DWChannelProps.DW_CH_TYPE)
        print(f"  Channel type (from property): {ch_type.name}")

        ch_scale = self.get_channel_property(ch, DWChannelProps.DW_CH_SCALE)
        print(f"  Scale (from property): {ch_scale}")

        ch_offset = self.get_channel_property(ch, DWChannelProps.DW_CH_OFFSET)
        print(f"  Offset (from property): {ch_offset}")

        if not self.SKIP_XML_DUMP:
            ch_xml = self.get_channel_property(ch, DWChannelProps.DW_CH_XML)
            print(f"  XML (from property): {ch_xml}")

            ch_xmlprops = self.get_channel_property(ch, DWChannelProps.DW_CH_XMLPROPS)
            print(f"  XML properties (from property): {ch_xmlprops}")

        ch_longname = self.get_channel_property(ch, DWChannelProps.DW_CH_LONGNAME)
        print(f"  Long name (from property): {ch_longname}")

        self.print_channel_arrays(ch)

    def print_channel_values(self, ch: DWChannel):
        print("===")
        print(" Channel values: ")
        print("===")

        sample_cnt = ctypes.c_longlong()
        check_error(self.lib,
                    self.lib.DWIGetScaledSamplesCount(self.reader_instance, ch.index, ctypes.byref(sample_cnt)))
        print(f"  Sample count: {sample_cnt.value}")

        display_sample_cnt = sample_cnt.value
        if self.MAX_SAMPLES_PER_CH >= 0 and display_sample_cnt > self.MAX_SAMPLES_PER_CH:
            display_sample_cnt = self.MAX_SAMPLES_PER_CH
        display_array_size = ch.array_size
        if self.MAX_SAMPLES_PER_CH >= 0 and display_array_size > self.MAX_SAMPLES_PER_CH:
            display_array_size = self.MAX_SAMPLES_PER_CH

        total_count: int = sample_cnt.value * ch.array_size
        # noinspection PyTypeChecker,PyCallingNonCallable
        samples = (ctypes.c_double * total_count)()

        ch_type = self.get_channel_property(ch, DWChannelProps.DW_CH_TYPE)

        timestamps = None
        if ch_type == DWChannelType.DW_CH_TYPE_ASYNC:
            timestamps = (ctypes.c_double * sample_cnt.value)()

        cmd_status = self.lib.DWIGetScaledSamples(self.reader_instance, ch.index, 0, sample_cnt, samples, timestamps)
        if DWStatus(cmd_status) == DWStatus.DWSTAT_ERROR_CAN_NOT_SUPPORTED:
            print("  CAN Channel is not stored decoded, skipping...")
            return
        check_error(self.lib, cmd_status)

        for i in range(sample_cnt.value):
            if i >= display_sample_cnt:
                print(f"  ...")
                break
            if ch.array_size == 1:
                if ch_type == DWChannelType.DW_CH_TYPE_ASYNC:
                    print(f"  Timestamp: {timestamps[i]:.2f}  Value: {samples[i]:.2f}")
                else:
                    print(f"  Value: {samples[i]:.2f}")
            else:
                if ch_type == DWChannelType.DW_CH_TYPE_ASYNC:
                    print(f"  Timestamp: {timestamps[i]:.2f}")
                for j in range(ch.array_size):
                    if j >= display_array_size:
                        print(f"  ...")
                        break
                    print(f"  Value[{j}]: {samples[i * ch.array_size + j]:.2f}")

    def print_complex_channel_values(self, ch: DWChannel):
        print("===")
        print(" Complex channel values: ")
        print("===")

        sample_cnt = ctypes.c_longlong()
        check_error(self.lib,
                    self.lib.DWIGetComplexScaledSamplesCount(self.reader_instance, ch.index, ctypes.byref(sample_cnt)))
        print(f"  Sample count: {sample_cnt.value}")

        display_sample_cnt = sample_cnt.value
        if self.MAX_SAMPLES_PER_CH >= 0 and display_sample_cnt > self.MAX_SAMPLES_PER_CH:
            display_sample_cnt = self.MAX_SAMPLES_PER_CH
        display_array_size = ch.array_size
        if self.MAX_SAMPLES_PER_CH >= 0 and display_array_size > self.MAX_SAMPLES_PER_CH:
            display_array_size = self.MAX_SAMPLES_PER_CH

        total_count: int = sample_cnt.value * ch.array_size
        samples = (DWComplex * total_count)()

        ch_type = self.get_channel_property(ch, DWChannelProps.DW_CH_TYPE)

        timestamps = None
        if ch_type == DWChannelType.DW_CH_TYPE_ASYNC:
            timestamps = (ctypes.c_double * sample_cnt.value)()

        check_error(self.lib,
                    self.lib.DWIGetComplexScaledSamples(self.reader_instance, ch.index, 0, sample_cnt, samples,
                                                        timestamps))

        for i in range(sample_cnt.value):
            if i >= display_sample_cnt:
                print(f"  ...")
                break
            if ch.array_size == 1:
                if ch_type == DWChannelType.DW_CH_TYPE_ASYNC:
                    print(f"  Timestamp: {timestamps[i]:.2f}  Value: ({samples[i].re:.2f}  {samples[i].im:.2f})")
                else:
                    print(f"  Value: ({samples[i].re:.2f}  {samples[i].im:.2f})")
            else:
                if ch_type == DWChannelType.DW_CH_TYPE_ASYNC:
                    print(f"  Timestamp: {timestamps[i]:.2f}")
                for j in range(ch.array_size):
                    if j >= display_array_size:
                        print(f"  ...")
                        break
                    print(
                        f"  Value[{j}]: ({samples[i * ch.array_size + j].re:.2f}  {samples[i * ch.array_size + j].im:.2f})")

    def print_binary_channel_values(self, ch: DWChannel):
        print("===")
        print(" Binary channel values: ")
        print("===")

        sample_cnt = ctypes.c_longlong()
        check_error(self.lib,
                    self.lib.DWIGetScaledSamplesCount(self.reader_instance, ch.index, ctypes.byref(sample_cnt)))
        print(f"  Sample count: {sample_cnt.value}")

        display_sample_cnt = sample_cnt.value
        if self.MAX_SAMPLES_PER_CH >= 0 and display_sample_cnt > self.MAX_SAMPLES_PER_CH:
            display_sample_cnt = self.MAX_SAMPLES_PER_CH
        display_array_size = ch.array_size
        if self.MAX_SAMPLES_PER_CH >= 0 and display_array_size > self.MAX_SAMPLES_PER_CH:
            display_array_size = self.MAX_SAMPLES_PER_CH

        total_count: int = sample_cnt.value * ch.array_size
        samples = (DWBinarySample * total_count)()

        ch_type = self.get_channel_property(ch, DWChannelProps.DW_CH_TYPE)
        assert ch_type == DWChannelType.DW_CH_TYPE_ASYNC
        assert ch.array_size == 1

        timestamps = (ctypes.c_double * sample_cnt.value)()
        check_error(self.lib,
                    self.lib.DWIGetBinRecSamples(self.reader_instance, ch.index, 0, sample_cnt, samples, timestamps))

        for i in range(sample_cnt.value):
            if i >= display_sample_cnt:
                print(f"  ...")
                break
            BIN_BUF_SIZE = 1024
            bin_rec = samples[i]
            bin_buf = create_string_buffer('', BIN_BUF_SIZE)
            bin_buf_pos = ctypes.c_longlong(0)
            check_error(self.lib, self.lib.DWIGetBinData(self.reader_instance, ch.index, bin_rec, bin_buf,
                                                         ctypes.byref(bin_buf_pos),
                                                         BIN_BUF_SIZE))
            print(f"  Timestamp: {timestamps[i]:.2f}  Value: {decode_bytes(bin_buf.value)}")

    def print_reduced_channel_values(self, ch: DWChannel):
        print("===")
        print(" Reduced channel values: ")
        print("===")

        sample_cnt = ctypes.c_int()
        block_size = ctypes.c_double()

        check_error(self.lib,
                    self.lib.DWIGetReducedValuesCount(self.reader_instance, ch.index, ctypes.byref(sample_cnt),
                                                      ctypes.byref(block_size)))

        print(f"  Reduced block count: {sample_cnt.value}")
        print(f"  Reduced block size: {block_size.value}")

        display_sample_cnt = sample_cnt.value
        if self.MAX_SAMPLES_PER_CH >= 0 and display_sample_cnt > self.MAX_SAMPLES_PER_CH:
            display_sample_cnt = self.MAX_SAMPLES_PER_CH

        blocks = (DWReducedValue * sample_cnt.value)()
        check_error(self.lib, self.lib.DWIGetReducedValues(self.reader_instance, ch.index, 0, sample_cnt, blocks))
        for i in range(sample_cnt.value):
            if i >= display_sample_cnt:
                print(f"  ...")
                break
            block = blocks[i]
            print(
                f"  Timestamp: {block.time_stamp:.2f}  Ave: {block.ave:.2f}  Min: {block.min:.2f}  Max: {block.max:.2f}  Rms: {block.rms:.2f}")

    def get_file_channels(self):
        print("===")
        print(" Channels: ")
        print("===")

        channel_count = ctypes.c_int()
        check_error(self.lib, self.lib.DWIGetChannelListCount(self.reader_instance, ctypes.byref(channel_count)))

        channel_list = (DWChannel * channel_count.value)()
        check_error(self.lib, self.lib.DWIGetChannelList(self.reader_instance, channel_list))

        for i in range(channel_count.value):
            ch = channel_list[i]
            self.print_channel_info(ch)
            self.print_channel_values(ch)
            self.print_reduced_channel_values(ch)

    def get_file_complex_channels(self):
        print("===")
        print(" Complex channels: ")
        print("===")

        channel_count = ctypes.c_int()
        check_error(self.lib, self.lib.DWIGetComplexChannelListCount(self.reader_instance, ctypes.byref(channel_count)))

        channel_list = (DWChannel * channel_count.value)()
        check_error(self.lib, self.lib.DWIGetComplexChannelList(self.reader_instance, channel_list))

        for i in range(channel_count.value):
            ch = channel_list[i]
            self.print_channel_info(ch)
            self.print_complex_channel_values(ch)
            self.print_reduced_channel_values(ch)

    def get_file_binary_channels(self):
        print("===")
        print(" Binary channels: ")
        print("===")

        channel_count = ctypes.c_int()
        check_error(self.lib, self.lib.DWIGetBinChannelListCount(self.reader_instance, ctypes.byref(channel_count)))

        channel_list = (DWChannel * channel_count.value)()
        check_error(self.lib, self.lib.DWIGetBinChannelList(self.reader_instance, channel_list))

        for i in range(channel_count.value):
            ch = channel_list[i]
            self.print_channel_info(ch)
            self.print_binary_channel_values(ch)


if __name__ == "__main__":
    file_name = "C:\\Users\\stefano.fortunati\\Desktop\\test_dewesoft.dxd"

    dw_data_reader = DWDataReader()
    dw_data_reader.open(filename=file_name)
    dw_data_reader.shows_all_info()
    dw_data_reader.close()
