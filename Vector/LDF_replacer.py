def replace_LDF(ldf_file_path):
    replace_data = generate_replacement_data()

    if "TMM1_LDF_Ceer_v" in ldf_file_path:
        TMM2_ldf_file_path = ldf_file_path.replace("TMM1_LDF_Ceer_v", "TMM2_LDF_Ceer_v")
        TMM3_ldf_file_path = ldf_file_path.replace("TMM1_LDF_Ceer_v", "TMM3_LDF_Ceer_v")
        TMM4_ldf_file_path = ldf_file_path.replace("TMM1_LDF_Ceer_v", "TMM4_LDF_Ceer_v")
    else:
        print("input ldf_file_path is wrong formatted")
        exit()

    #self.copy_files()
    search_and_replace_in_file(TMM1_input_file_path=ldf_file_path, output_file_path=TMM2_ldf_file_path,
                               replace_data=replace_data, replace_index=1)
    search_and_replace_in_file(TMM1_input_file_path=ldf_file_path, output_file_path=TMM3_ldf_file_path,
                               replace_data=replace_data, replace_index=2)
    search_and_replace_in_file(TMM1_input_file_path=ldf_file_path, output_file_path=TMM4_ldf_file_path,
                               replace_data=replace_data, replace_index=3)


def generate_replacement_data():
    base_data = [
        "TMM1_CTR_EWP_P1_LIN",
        "TMM1_ST_EWP_P1_LIN",
        "TMM1_CTR_EWP_P2_LIN",
        "TMM1_ST_EWP_P2_LIN",
        "TMM1_CTR_EWP_P3_LIN",
        "TMM1_ST_EWP_P3_LIN",
        "TMM1_V1_PR4W_Rq_LIN",
        "TMM1_V1_PR4W_Stat_LIN",
        "TMM1_V2_PR4W_Rq_LIN",
        "TMM1_V2_PR4W_Stat_LIN",
        "TMM1_V3_PR4W_Rq_LIN",
        "TMM1_V3_PR4W_Stat_LIN",
        "TMM1_DBG_FRAME",
        "TMM1_REF_DRIVE"
    ]
    replace_data = []
    for elem in base_data:
        replace_item = []
        replace_item.append(elem)
        replace_item.append(elem.replace("TMM1_", "TMM2_"))
        replace_item.append(elem.replace("TMM1_", "TMM3_"))
        replace_item.append(elem.replace("TMM1_", "TMM4_"))
        replace_data.append(replace_item)
    return replace_data



def search_and_replace_in_file(TMM1_input_file_path, output_file_path,replace_data, replace_index):
    # Leggi tutto il contenuto
    with open(TMM1_input_file_path, "r", encoding="utf-8") as f:
        content = f.read()

    new_content = content
    # Sostituisci
    for array in replace_data:
        new_content = new_content.replace(array[0], array[replace_index])

    # Salva se c'è stata una modifica
    if new_content != content:
        with open(output_file_path, "w", encoding="utf-8") as f:
            f.write(new_content)
    else:
        print(f"Nessuna occorrenza trovata in {TMM1_input_file_path}")
