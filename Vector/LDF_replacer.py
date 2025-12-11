import os
from pathlib import Path


def replace_LDF(ldf_file_path):
    replace_data = generate_replacement_data_for_LDF()

    if "TMM1_LDF_Ceer_v" in ldf_file_path:
        TMM2_ldf_file_path = ldf_file_path.replace("/TMM1/TMM1_LDF_Ceer_v", "/TMM2/TMM2_LDF_Ceer_v")
        TMM3_ldf_file_path = ldf_file_path.replace("/TMM1/TMM1_LDF_Ceer_v", "/TMM3/TMM3_LDF_Ceer_v")
        TMM4_ldf_file_path = ldf_file_path.replace("/TMM1/TMM1_LDF_Ceer_v", "/TMM4/TMM4_LDF_Ceer_v")
    else:
        print("input ldf_file_path is wrong formatted")
        exit()

    #self.copy_files()
    extract_and_create_first_folder(TMM2_ldf_file_path)
    search_and_replace_in_file(TMM1_input_file_path=ldf_file_path, output_file_path=TMM2_ldf_file_path,
                               replace_data=replace_data, replace_index=1)
    extract_and_create_first_folder(TMM3_ldf_file_path)
    search_and_replace_in_file(TMM1_input_file_path=ldf_file_path, output_file_path=TMM3_ldf_file_path,
                               replace_data=replace_data, replace_index=2)
    extract_and_create_first_folder(TMM4_ldf_file_path)
    search_and_replace_in_file(TMM1_input_file_path=ldf_file_path, output_file_path=TMM4_ldf_file_path,
                               replace_data=replace_data, replace_index=3)


def generate_replacement_data_for_LDF():
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


def extract_and_create_first_folder(file_path):
    first_folder = ""
    # Get the first folder from the path
    path = Path(file_path)
    if len(path.parts) > 1:
        folder_list = path.parts[:-1]
        first_folder = Path(*folder_list)
    else:
        print("ERROR: ")

    #print("first_folder: ", first_folder)
    # Check if the folder exists
    if not os.path.exists(first_folder):
        # If it doesn't exist, create the folder
        os.makedirs(first_folder)
        #print(f"Folder '{first_folder}' created.")
    else:
        pass
        #print(f"Folder '{first_folder}' already exists.")

def search_and_replace_in_file(TMM1_input_file_path, output_file_path,replace_data, replace_index):
    # Leggi tutto il contenuto
    with open(TMM1_input_file_path, "r", encoding="utf-8") as f:
        content = f.read()

    new_content = content
    # Sostituisci
    for array in replace_data:
        new_content = new_content.replace(array[0], array[replace_index])

    # Set tmm frame number
    new_content = new_content.replace("TMM_number=1;", f"TMM_number={replace_index+1};")


    # Salva se c'è stata una modifica
    if new_content != content:
        with open(output_file_path, "w", encoding="utf-8") as f:
            f.write(new_content)
    else:
        print(f"Nessuna occorrenza trovata in {TMM1_input_file_path}")
