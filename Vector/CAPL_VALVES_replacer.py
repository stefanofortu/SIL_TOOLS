from Vector.LDF_replacer import extract_and_create_first_folder, search_and_replace_in_file
def replace_CAPL_VALVES(ldf_file_path):
    replace_data = generate_replacement_data_for_capl_valves()
    print(ldf_file_path)
    if "TMM1_Valves_rev" in ldf_file_path:
        TMM2_file_path = ldf_file_path.replace("TMM1/TMM1_Valves_rev", "TMM2/TMM2_Valves_rev")
        TMM3_file_path = ldf_file_path.replace("TMM1/TMM1_Valves_rev", "TMM3/TMM3_Valves_rev")
        TMM4_file_path = ldf_file_path.replace("TMM1/TMM1_Valves_rev", "TMM4/TMM4_Valves_rev")
    else:
        print("input capl_tmm_file_path is wrong formatted")
        exit()
    search_and_replace_in_file(TMM1_input_file_path=ldf_file_path, output_file_path=TMM2_file_path,
                               replace_data=replace_data, replace_index=1)
    search_and_replace_in_file(TMM1_input_file_path=ldf_file_path, output_file_path=TMM3_file_path,
                               replace_data=replace_data, replace_index=2)
    search_and_replace_in_file(TMM1_input_file_path=ldf_file_path, output_file_path=TMM4_file_path,
                               replace_data=replace_data, replace_index=3)


def generate_replacement_data_for_capl_valves():
    base_data = [
        "TMM1_::"
    ]
    replace_data = []
    for elem in base_data:
        replace_item = [elem,
                        elem.replace("TMM1_", "TMM2_"),
                        elem.replace("TMM1_", "TMM3_"),
                        elem.replace("TMM1_", "TMM4_")]
        replace_data.append(replace_item)
    return replace_data

