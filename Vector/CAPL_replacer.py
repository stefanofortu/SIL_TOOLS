from Vector.LDF_replacer import extract_and_create_first_folder, search_and_replace_in_file


def replace_CAPL(file_path):
    replace_data = generate_replacement_data_for_VCU_CAPL()

    if "TMM1_VCU_rev" in file_path:
        TMM2_file_path = file_path.replace("/TMM1/TMM1_VCU_rev", "/TMM2/TMM2_VCU_rev")
        TMM3_file_path = file_path.replace("/TMM1/TMM1_VCU_rev", "/TMM3/TMM2_VCU_rev")
        TMM4_file_path = file_path.replace("/TMM1/TMM1_VCU_rev", "/TMM4/TMM2_VCU_rev")
    else:
        print("input TMM1_VCU_rev is wrong formatted")
        exit()

    extract_and_create_first_folder(TMM2_file_path)
    search_and_replace_in_file(TMM1_input_file_path=file_path, output_file_path=TMM2_file_path,
                               replace_data=replace_data, replace_index=1)
    extract_and_create_first_folder(TMM3_file_path)
    search_and_replace_in_file(TMM1_input_file_path=file_path, output_file_path=TMM3_file_path,
                               replace_data=replace_data, replace_index=2)
    extract_and_create_first_folder(TMM4_file_path)
    search_and_replace_in_file(TMM1_input_file_path=file_path, output_file_path=TMM4_file_path,
                               replace_data=replace_data, replace_index=3)


def generate_replacement_data_for_VCU_CAPL():
    base_data = [
        "#include \"TMM1_Valves_rev",
        "linFrame TMM1_CTR_EWP_P1_LIN",
        "linFrame TMM1_CTR_EWP_P2_LIN",
        "linFrame TMM1_CTR_EWP_P3_LIN",
        "linFrame TMM1_V1_PR4W_Rq_LIN",
        "linFrame TMM1_V2_PR4W_Rq_LIN",
        "linFrame TMM1_V3_PR4W_Rq_LIN",
        "linFrame TMM1_DBG_FRAME",
        "linFrame TMM1_ST_EWP_P1_LIN",
        "linFrame TMM1_ST_EWP_P2_LIN",
        "linFrame TMM1_ST_EWP_P3_LIN",
        "linFrame TMM1_V1_PR4W_Stat_LIN",
        "linFrame TMM1_V2_PR4W_Stat_LIN",
        "linFrame TMM1_V3_PR4W_Stat_LIN",
        "linFrame TMM1_REF_DRIVE",
        "write(\"TMM1_"
    ]
    replace_data = []
    for elem in base_data:
        replace_item = [elem,
                        elem.replace("TMM1_", "TMM2_"),
                        elem.replace("TMM1_", "TMM3_"),
                        elem.replace("TMM1_", "TMM4_")]
        replace_data.append(replace_item)
    return replace_data
