def replace_CAPL_VALVES(ldf_file_path):
    replace_data = generate_replacement_data()
    print(ldf_file_path)
    if "TMM1_Valves_rev" in ldf_file_path:
        TMM2_file_path = ldf_file_path.replace("TMM1_Valves_rev", "TMM2_Valves_rev")
        TMM3_file_path = ldf_file_path.replace("TMM1_Valves_rev", "TMM3_Valves_rev")
        TMM4_file_path = ldf_file_path.replace("TMM1_Valves_rev", "TMM4_Valves_rev")
    else:
        print("input capl_tmm_file_path is wrong formatted")
        exit()
    print(TMM2_file_path)
    print(TMM3_file_path)
    print(TMM4_file_path)
    search_and_replace_in_file(TMM1_input_file_path=ldf_file_path, output_file_path=TMM2_file_path,
                               replace_data=replace_data, replace_index=1)
    search_and_replace_in_file(TMM1_input_file_path=ldf_file_path, output_file_path=TMM3_file_path,
                               replace_data=replace_data, replace_index=2)
    search_and_replace_in_file(TMM1_input_file_path=ldf_file_path, output_file_path=TMM4_file_path,
                               replace_data=replace_data, replace_index=3)


def generate_replacement_data():
    base_data = []
    replace_data = []
    for elem in base_data:
        replace_item = [elem,
                        elem.replace("TMM1_", "TMM2_"),
                        elem.replace("TMM1_", "TMM3_"),
                        elem.replace("TMM1_", "TMM4_")]
        replace_data.append(replace_item)
    return replace_data


def search_and_replace_in_file(TMM1_input_file_path, output_file_path, replace_data, replace_index):
    # Leggi tutto il contenuto
    with open(TMM1_input_file_path, "r", encoding="utf-8") as f:
        content = f.read()

    new_content = content
    # Sostituisci
    for array in replace_data:
        new_content = new_content.replace(array[0], array[replace_index])

    if new_content == content:
        print(f"Nessuna occorrenza trovata. File salvato. {TMM1_input_file_path}")
    # Salva se c'è stata una modifica
    with open(output_file_path, "w", encoding="utf-8") as f:
        f.write(new_content)
