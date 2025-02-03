'''
Created on 11 dic 2023

@author: andrea.pasotti
'''

Sonceboz_LDF = '\n\
\n\
LIN_description_file;\n\
LIN_protocol_version = "2.0";\n\
LIN_language_version = "2.0";\n\
LIN_speed = 19.2 kbps;\n\
Nodes {\n\
    Master: TME, 10 ms, 0.1 ms;\n\
    Slaves: MVW_1;\n\
}\n\
Signals {\n\
    MVW1_Err_Blockierung_TF: 1, 0, MVW_1, TME;\n\
    MVW1_Err_Blockierung_TNCTOC: 1, 1, MVW_1, TME;\n\
    MVW1_Err_EDefekt_MoKomp_TF: 1, 0, MVW_1, TME;\n\
    MVW1_Err_EDefekt_MoKomp_TNCTOC: 1, 1, MVW_1, TME;\n\
    MVW1_Err_EDefekt_TSens_TF: 1, 0, MVW_1, TME;\n\
    MVW1_Err_EDefekt_TSens_TNCTOC: 1, 1, MVW_1, TME;\n\
    MVW1_Err_Notlaufpos_TF: 1, 0, MVW_1, TME;\n\
    MVW1_Err_Notlaufpos_TNCTOC: 1, 1, MVW_1, TME;\n\
    MVW1_Err_RAMROMNADChange_TF: 1, 0, MVW_1, TME;\n\
    MVW1_Err_RAMROMNADChange_TNCTOC: 1, 1, MVW_1, TME;\n\
    MVW1_Err_Ueberspannung_TF: 1, 0, MVW_1, TME;\n\
    MVW1_Err_Ueberspannung_TNCTOC: 1, 1, MVW_1, TME;\n\
    MVW1_Err_Uebertemperatur_TF: 1, 0, MVW_1, TME;\n\
    MVW1_Err_Uebertemperatur_TNCTOC: 1, 1, MVW_1, TME;\n\
    MVW1_Err_Unterspannung_TF: 1, 0, MVW_1, TME;\n\
    MVW1_Err_Unterspannung_TNCTOC: 1, 1, MVW_1, TME;\n\
    MVW1_ErrMem_State: 2, 0, MVW_1, TME;\n\
    MVW1_Geschwindigkeitsstatus: 4, 0, MVW_1, TME;\n\
    MVW1_Ist_Position_Aktuator: 16, 65534, MVW_1, TME;\n\
    MVW1_ResponseError: 1, 0, MVW_1, TME;\n\
    MVW1_ResponseError_TNCTOC: 1, 1, MVW_1, TME;\n\
    MVW1_Spulenbestromung: 2, 0, MVW_1, TME;\n\
    MVW1_Temp: 8, 254, MVW_1, TME;\n\
    STRG2_Adresse_Aktuator: 8, 0, TME, MVW_1;\n\
    STRG2_Geschwindigkeitsvorgabe: 4, 0, TME, MVW_1;\n\
    STRG2_Notlauffreigabe: 2, 0, TME, MVW_1;\n\
    STRG2_Select_Positionsvorgabe: 2, 2, TME, MVW_1;\n\
    STRG2_Soll_Position_Aktuator: 16, 0, TME, MVW_1;\n\
    STRG2_Spulenbestromung: 2, 0, TME, MVW_1;\n\
}\n\
Diagnostic_signals {\n\
        MasterReqB0:8,0;\n\
        MasterReqB1:8,0;\n\
        MasterReqB2:8,0;\n\
        MasterReqB3:8,0;\n\
        MasterReqB4:8,0;\n\
        MasterReqB5:8,0;\n\
        MasterReqB6:8,0;\n\
        MasterReqB7:8,0;\n\
        SlaveRespB0:8,0;\n\
        SlaveRespB1:8,0;\n\
        SlaveRespB2:8,0;\n\
        SlaveRespB3:8,0;\n\
        SlaveRespB4:8,0;\n\
        SlaveRespB5:8,0;\n\
        SlaveRespB6:8,0;\n\
        SlaveRespB7:8,0;\n\
}\n\
Frames {\n\
    EVe_02_Control: 0x12, TME, 8 {\n\
        STRG2_Adresse_Aktuator, 0;\n\
        STRG2_Spulenbestromung, 16;\n\
        STRG2_Select_Positionsvorgabe, 18;\n\
        STRG2_Geschwindigkeitsvorgabe, 20;\n\
        STRG2_Soll_Position_Aktuator, 24;\n\
        STRG2_Notlauffreigabe, 56;\n\
    }\n\
    MVW1_01: 0x31, MVW_1, 8 {\n\
        MVW1_Ist_Position_Aktuator, 0;\n\
        MVW1_Geschwindigkeitsstatus, 16;\n\
        MVW1_Temp, 24;\n\
        MVW1_Spulenbestromung, 32;\n\
        MVW1_ErrMem_State, 38;\n\
        MVW1_ResponseError, 40;\n\
        MVW1_ResponseError_TNCTOC, 41;\n\
        MVW1_Err_EDefekt_MoKomp_TF, 42;\n\
        MVW1_Err_EDefekt_MoKomp_TNCTOC, 43;\n\
        MVW1_Err_EDefekt_TSens_TF, 44;\n\
        MVW1_Err_EDefekt_TSens_TNCTOC, 45;\n\
        MVW1_Err_Uebertemperatur_TF, 46;\n\
        MVW1_Err_Uebertemperatur_TNCTOC, 47;\n\
        MVW1_Err_Ueberspannung_TF, 48;\n\
        MVW1_Err_Ueberspannung_TNCTOC, 49;\n\
        MVW1_Err_Unterspannung_TF, 50;\n\
        MVW1_Err_Unterspannung_TNCTOC, 51;\n\
        MVW1_Err_Blockierung_TF, 52;\n\
        MVW1_Err_Blockierung_TNCTOC, 53;\n\
        MVW1_Err_RAMROMNADChange_TF, 54;\n\
        MVW1_Err_RAMROMNADChange_TNCTOC, 55;\n\
        MVW1_Err_Notlaufpos_TF, 56;\n\
        MVW1_Err_Notlaufpos_TNCTOC, 57;\n\
    }\n\
}\n\
Diagnostic_frames {\n\
    MasterReq: 60 {\n\
        MasterReqB0, 0;\n\
        MasterReqB1, 8;\n\
        MasterReqB2, 16;\n\
        MasterReqB3, 24;\n\
        MasterReqB4, 32;\n\
        MasterReqB5, 40;\n\
        MasterReqB6, 48;\n\
        MasterReqB7, 56;\n\
    }\n\
    SlaveResp: 61    {\n\
        SlaveRespB0, 0;\n\
        SlaveRespB1, 8;\n\
        SlaveRespB2, 16;\n\
        SlaveRespB3, 24;\n\
        SlaveRespB4, 32;\n\
        SlaveRespB5, 40;\n\
        SlaveRespB6, 48;\n\
        SlaveRespB7, 56;\n\
    }\n\
}\n\
Node_attributes {\n\
    MVW_1 {\n\
        LIN_protocol = 2.0;\n\
        configured_NAD = 0x3C;\n\
        product_id = 0x010C, 0x0001, 0x01;\n\
        response_error = MVW1_ResponseError;\n\
        P2_min = 10 ms;\n\
        ST_min = 10 ms;\n\
        configurable_frames {\n\
            EVe_02_Control = 0x4012;\n\
            MVW1_01 = 0x4031;\n\
        }\n\
    }\n\
}\n\
Schedule_tables {\n\
    NormalTable {\n\
        EVe_02_Control delay 50 ms;\n\
        MVW1_01 delay 50 ms;\n\
    //    ETF_MotorStates delay 50 ms;\n\
    //    SporadicControlFrame delay 20 ms;\n\
    }\n\
// ETFCollisionResolving {\n\
//    Motor1State_Event delay 50 ms;\n\
//  }\n\
// InitTable {\n\
//    AssignNAD { EWAPU } delay 10 ms;\n\
//    SlaveResp delay 10 ms;\n\
//    AssignFrameIdRange { EWAPU, 0 } delay 10 ms;\n\
//    AssignFrameIdRange { EWAPU, 4 } delay 10 ms;\n\
//  }\n\
}\n\
\n'