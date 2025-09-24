from asammdf import MDF
import xml.etree.ElementTree as ET

class Vector_to_MDF:

    @staticmethod
    def exec_conversion(input_file_path, use_same_input_file_name, output_file_name):
        if use_same_input_file_name == True:
            out_filename = input_file_path[:-4] + "_TMM_names" + ".mf4"
        else:
            out_filename = output_file_name
            print("error - use_same_input_file_name == False")
            exit()

        mdf_obj = MDF(input_file_path)
        for group in mdf_obj.groups:
            for channel in group.channels:
                if channel.source is not None:
                    if channel.source.comment is not None and channel.source.comment != "":
                        #print("channel.source.comment ", channel.source.comment)
                        root = ET.fromstring(channel.source.comment)
                        TMM_num = "TMM" + root.find('.//e[@name="ChannelNo"]').text
                        #print(f"Channel Number: {TMM_num}")
                        new_name = TMM_num + "_" + channel.name
                        print(channel.name + " --> " + new_name)
                        channel.name = new_name
        mdf_obj.save(out_filename)


        # to_keep = ["TMM3_TARVL_RPM_EWP_P1"]#, "TARVL_RPM_EWP_P2", "TARVL_RPM_EWP_P3", "DBG_test_type"]
        # mdf_obj = MDF(input_file_path)# raw=True)  # ignore_value2text_conversions =True)
        # needed_signals = ['TMM1_TARVL_RPM_EWP_P1', 'TMM1_TARVL_RPM_EWP_P2']
        # signals = mdf_obj.select(needed_signals, ignore_value2text_conversions=True)
        # print(signals)
        #
        #
        # tarv = mdf_obj.get('TMM3_TARVL_RPM_EWP_P1')
        # print(tarv, tarv.samples, tarv.timestamps, tarv.raw, tarv.source)
        # array = tarv.samples
        # #tarv.plot()
        # #tarv.plot()
        # print("hello")
        # print(array)
        # print(np.unique(array))
        # print("1")
        # tarv_physical = tarv.physical()
        # #tarv_physical.plot()
        # print("2")
        # print(tarv_physical)
        # print(tarv_physical.samples)
        # print("3")
        # print(np.unique(tarv_physical.samples))
        #
        #
        # col=["TMM1_TARVL_RPM_EWP_P1", "TMM1_TARVL_RPM_EWP_P2", "TMM1_TARVL_RPM_EWP_P3"]
        # df = mdf_obj.to_dataframe(ignore_value2text_conversions=True)
        # df = df.reset_index()
        # df = df.rename(columns={'timestamps': 'Time[s]'})
        # df.to_csv("hello2.csv", columns=col)
        # start_time = Timestamp(mdf_obj.start_time)
        # exit()
        # for group in mdf_obj.groups:
        #     print(group)
        # for group in mdf_obj.groups:
        #     for channel in group.channels:
        #         if channel is not None:
        #             print("channel.name ", channel.name)
        #         if channel.source is not None:
        #             if channel.source.comment is not None and channel.source.comment != "":
        #                 print("channel.source.comment ", channel.source.comment)
        #                 root = ET.fromstring(channel.source.comment)
        #                 TMM_num = "TMM" + root.find('.//e[@name="ChannelNo"]').text
        #                 print(f"Channel Number: {TMM_num}")
        #                 channel.name = TMM_num + "_" + channel.name
        # # mdf_obj.save("translated.mf4")
        #
        # #print(df["TMM1_TARVL_RPM_EWP_P1"].head())
        # # df = mdf_obj.filter(to_keep).export('pandas')
        #
        # df = df.reset_index()
        # df = df.rename(columns={'timestamps': 'Time[s]'})
        # df.to_csv("hello.csv")
        # start_time = Timestamp(mdf_obj.start_time)
        # exit()
        # return df, start_time
