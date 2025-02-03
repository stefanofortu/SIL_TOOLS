'''
Created on 2 ott 2023

@author: andrea.pasotti
'''

Heart_LDF = '\n\
/*  QGate V5.8.0 - 26.02.23 01:33:33 MEZ*/ \n\
/* ************************************************************************** */\n\
/*                                                                            */\n\
/*                                 BMW AG                                       */\n\
/*                        All rights reserved                                 */\n\
/*                                                                            */\n\
/* ************************************************************************** */\n\
/*                                                                            */\n\
/*  Description: LIN Description file                                         */\n\
/*  Distribution: J23KW09                                                     */\n\
/*  Konfiguration: EESystem25_23KW09 [19]                                     */\n\
/*  Konfigurationsstand: G065-26-07-130                                       */\n\
/*  Bus: IPF_LIN_1 [18]                                                       */\n\
/*                                                                            */\n\
/* ************************************************************************** */\n\
\n\
LIN_description_file;\n\
LIN_protocol_version = "2.2";\n\
LIN_language_version = "2.2";\n\
LIN_speed =  19.2 kbps;\n\
Channel_name = "IPF_LIN_1";\n\
\n\
Nodes {\n\
    Master: IPF_HVM, 10.0 ms, 0.1 ms;\n\
    Slaves: EWP_BAT, EWP_HK;\n\
}\n\
\n\
Signals {\n\
    ControlCurrentAllowedMaximumP1LIN: 8, 255, IPF_HVM, EWP_HK;\n\
    ControlCurrentAllowedMaximumP2LIN: 8, 255, IPF_HVM, EWP_BAT;\n\
    ControlSpeedEmergencyRunP1LIN: 8, 255, IPF_HVM, EWP_HK;\n\
    ControlSpeedEmergencyRunP2LIN: 8, 255, IPF_HVM, EWP_BAT;\n\
    ControlSpeedTargetValueP1LIN: 8, 255, IPF_HVM, EWP_HK;\n\
    ControlSpeedTargetValueP2LIN: 8, 255, IPF_HVM, EWP_BAT;\n\
    StatusCurrentActualValueP1LIN: 8, 255, EWP_HK, IPF_HVM;\n\
    StatusCurrentActualValueP2LIN: 8, 255, EWP_BAT, IPF_HVM;\n\
    StatusDataInternalP1LIN: 8, 255, EWP_HK, IPF_HVM;\n\
    StatusDataInternalP2LIN: 8, 255, EWP_BAT, IPF_HVM;\n\
    StatusErrorBlockingP1LIN: 2, 3, EWP_HK, IPF_HVM;\n\
    StatusErrorBlockingP2LIN: 2, 3, EWP_BAT, IPF_HVM;\n\
    StatusErrorCommP1LIN: 1, 0, EWP_HK, IPF_HVM;\n\
    StatusErrorCommP2LIN: 1, 0, EWP_BAT, IPF_HVM;\n\
    StatusErrorDryRunP1LIN: 2, 3, EWP_HK, IPF_HVM;\n\
    StatusErrorDryRunP2LIN: 2, 3, EWP_BAT, IPF_HVM;\n\
    StatusErrorElectricalFaultP1LIN: 2, 3, EWP_HK, IPF_HVM;\n\
    StatusErrorElectricalFaultP2LIN: 2, 3, EWP_BAT, IPF_HVM;\n\
    StatusErrorOverCurrentP1LIN: 2, 3, EWP_HK, IPF_HVM;\n\
    StatusErrorOverCurrentP2LIN: 2, 3, EWP_BAT, IPF_HVM;\n\
    StatusErrorOverTemperatureP1LIN: 2, 3, EWP_HK, IPF_HVM;\n\
    StatusErrorOverTemperatureP2LIN: 2, 3, EWP_BAT, IPF_HVM;\n\
    StatusErrorSpeedMonitoringP1LIN: 2, 3, EWP_HK, IPF_HVM;\n\
    StatusErrorSpeedMonitoringP2LIN: 2, 3, EWP_BAT, IPF_HVM;\n\
    StatusErrorVoltageOutOfRangeP1LIN: 2, 3, EWP_HK, IPF_HVM;\n\
    StatusErrorVoltageOutOfRangeP2LIN: 2, 3, EWP_BAT, IPF_HVM;\n\
    StatusSpeedActualValueP1LIN: 8, 255, EWP_HK, IPF_HVM;\n\
    StatusSpeedActualValueP2LIN: 8, 255, EWP_BAT, IPF_HVM;\n\
    StatusSpeedTargetValueP1LIN: 8, 255, EWP_HK, IPF_HVM;\n\
    StatusSpeedTargetValueP2LIN: 8, 255, EWP_BAT, IPF_HVM;\n\
    StatusTemperatureActualValueP1LIN: 8, 255, EWP_HK, IPF_HVM;\n\
    StatusTemperatureActualValueP2LIN: 8, 255, EWP_BAT, IPF_HVM;\n\
    StatusVoltageActualValueP1LIN: 8, 255, EWP_HK, IPF_HVM;\n\
    StatusVoltageActualValueP2LIN: 8, 255, EWP_BAT, IPF_HVM;\n\
}\n\
\n\
Diagnostic_signals {\n\
    MasterReqB0: 8, 0;\n\
    MasterReqB1: 8, 0;\n\
    MasterReqB2: 8, 0;\n\
    MasterReqB3: 8, 0;\n\
    MasterReqB4: 8, 0;\n\
    MasterReqB5: 8, 0;\n\
    MasterReqB6: 8, 0;\n\
    MasterReqB7: 8, 0;\n\
    SlaveRespB0: 8, 0;\n\
    SlaveRespB1: 8, 0;\n\
    SlaveRespB2: 8, 0;\n\
    SlaveRespB3: 8, 0;\n\
    SlaveRespB4: 8, 0;\n\
    SlaveRespB5: 8, 0;\n\
    SlaveRespB6: 8, 0;\n\
    SlaveRespB7: 8, 0;\n\
}\n\
\n\
Frames {\n\
    ControlP1LIN: 57, IPF_HVM, 3{\n\
        ControlSpeedTargetValueP1LIN, 0;\n\
        ControlSpeedEmergencyRunP1LIN, 8;\n\
        ControlCurrentAllowedMaximumP1LIN, 16;\n\
    }\n\
    ControlP2LIN: 40, IPF_HVM, 3{\n\
        ControlSpeedTargetValueP2LIN, 0;\n\
        ControlSpeedEmergencyRunP2LIN, 8;\n\
        ControlCurrentAllowedMaximumP2LIN, 16;\n\
    }\n\
    StatusP1LIN: 56, EWP_HK, 8{\n\
        StatusSpeedTargetValueP1LIN, 0;\n\
        StatusSpeedActualValueP1LIN, 8;\n\
        StatusVoltageActualValueP1LIN, 16;\n\
        StatusTemperatureActualValueP1LIN, 24;\n\
        StatusCurrentActualValueP1LIN, 32;\n\
        StatusErrorElectricalFaultP1LIN, 40;\n\
        StatusErrorSpeedMonitoringP1LIN, 42;\n\
        StatusErrorCommP1LIN, 44;\n\
        StatusErrorOverTemperatureP1LIN, 46;\n\
        StatusErrorOverCurrentP1LIN, 48;\n\
        StatusErrorDryRunP1LIN, 50;\n\
        StatusErrorVoltageOutOfRangeP1LIN, 52;\n\
        StatusErrorBlockingP1LIN, 54;\n\
        StatusDataInternalP1LIN, 56;\n\
    }\n\
    StatusP2LIN: 39, EWP_BAT, 8{\n\
        StatusSpeedTargetValueP2LIN, 0;\n\
        StatusSpeedActualValueP2LIN, 8;\n\
        StatusVoltageActualValueP2LIN, 16;\n\
        StatusTemperatureActualValueP2LIN, 24;\n\
        StatusCurrentActualValueP2LIN, 32;\n\
        StatusErrorElectricalFaultP2LIN, 40;\n\
        StatusErrorSpeedMonitoringP2LIN, 42;\n\
        StatusErrorCommP2LIN, 44;\n\
        StatusErrorOverTemperatureP2LIN, 46;\n\
        StatusErrorOverCurrentP2LIN, 48;\n\
        StatusErrorDryRunP2LIN, 50;\n\
        StatusErrorVoltageOutOfRangeP2LIN, 52;\n\
        StatusErrorBlockingP2LIN, 54;\n\
        StatusDataInternalP2LIN, 56;\n\
    }\n\
}\n\
\n\
\n\
\n\
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
    SlaveResp: 61 {\n\
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
\n\
Node_attributes{\n\
        EWP_BAT {\n\
            LIN_protocol = "2.1";\n\
            configured_NAD = 0x5A;\n\
            initial_NAD = 0x5A;\n\
            product_id = 0x7FFF,0xFFFF,0x00;\n\
            response_error = StatusErrorCommP2LIN;\n\
            P2_min = 50.0 ms;\n\
            ST_min = 0.0 ms;\n\
            configurable_frames {\n\
                        StatusP2LIN;\n\
                        ControlP2LIN;\n\
                        }\n\
        }\n\
        EWP_HK {\n\
            LIN_protocol = "2.1";\n\
            configured_NAD = 0x4B;\n\
            initial_NAD = 0x4B;\n\
            product_id = 0x7FFF,0xFFFF,0x00;\n\
            response_error = StatusErrorCommP1LIN;\n\
            P2_min = 50.0 ms;\n\
            ST_min = 0.0 ms;\n\
            configurable_frames {\n\
                        StatusP1LIN;\n\
                        ControlP1LIN;\n\
                        }\n\
        }\n\
    }\n\
\n\
Schedule_tables {\n\
        RUN_P1 { \n\
            ControlP1LIN delay 10.0 ms;\n\
            StatusP1LIN delay 10.0 ms;\n\
        }\n\
        RUN_P2 { \n\
            ControlP2LIN delay 10.0 ms;\n\
            StatusP2LIN delay 10.0 ms;\n\
        }\n\
        RUN_MAIN { \n\
            ControlP1LIN delay 10.0 ms;\n\
            ControlP2LIN delay 10.0 ms;\n\
            StatusP1LIN delay 10.0 ms;\n\
            StatusP2LIN delay 10.0 ms;\n\
        }\n\
        DIAG_19200_10 { \n\
            MasterReq delay 10.0 ms;\n\
            SlaveResp delay 10.0 ms;\n\
        }\n\
        DIAG_RESP_19200_10 { \n\
            SlaveResp delay 10.0 ms;\n\
        }\n\
        DIAG_RQ_19200_10 { \n\
            MasterReq delay 10.0 ms;\n\
        }\n\
        /*\n\
        INIT_ALL { \n\
            AssignFrameIdRange { EWP_HK , 0, 120, 57, 0xFF, 0xFF }  delay 10.0 ms;\n\
            AssignFrameIdRange { EWP_BAT , 0, 231, 168, 0xFF, 0xFF }  delay 10.0 ms;\n\
        }\n\
        */\n\
    }\n\
\n\
Signal_encoding_types {\n\
        ControlCurrentAllowedMaximumPxLIN {\n\
                physical_value, 0 , 251 , 0.2 , 0 , "A";\n\
                logical_value, 252, "Maximaler_Strom_erlaubt";\n\
                logical_value, 253, "Funktionsschnittstelle_ist_nicht_verfuegbar";\n\
                logical_value, 254, "Funktion_meldet_Fehler";\n\
                logical_value, 255, "Signal_unbefuellt"; /* @ErrorValue */\n\
        }\n\
        ControlSpeedPxLIN {\n\
                physical_value, 0 , 250 , 1 , 0 , "";\n\
                logical_value, 253, "Funktionsschnittstelle_ist_nicht_verfuegbar";\n\
                logical_value, 254, "Funktion_meldet_Fehler";\n\
                logical_value, 255, "Signal_unbefuellt"; /* @ErrorValue */\n\
        }\n\
        StatusCurrentActualValuePxLIN {\n\
                physical_value, 0 , 251 , 0.2 , 0 , "A";\n\
                logical_value, 252, "Measured_current_greater_than_50_2_A";\n\
                logical_value, 253, "Funktionsschnittstelle_ist_nicht_verfuegbar";\n\
                logical_value, 254, "Funktion_meldet_Fehler";\n\
                logical_value, 255, "Signal_unbefuellt"; /* @ErrorValue */\n\
        }\n\
        StatusDataInternalPxLIN {\n\
                physical_value, 0 , 255 , 1 , 0 , "Decodierung wird von LIN nicht unterstützt siehe NK";\n\
        }\n\
        StatusErrorBlockingPxLIN {\n\
                logical_value, 0, "No_blocking_detected";\n\
                logical_value, 1, "Blocking_detected";\n\
                logical_value, 3, "Signal_unbefuellt"; /* @ErrorValue */\n\
        }\n\
        StatusErrorCommXyzLIN {\n\
                logical_value, 0, "no_Error";\n\
                logical_value, 1, "Communication_Error";\n\
        }\n\
        StatusErrorDryRunPxLIN {\n\
                logical_value, 0, "No_dry_run_detected";\n\
                logical_value, 1, "Dry_run_detected";\n\
                logical_value, 2, "No_dry_run_detection_performed_since_activation";\n\
                logical_value, 3, "Signal_unbefuellt"; /* @ErrorValue */\n\
        }\n\
        StatusErrorElectricalFaultPxLIN {\n\
                logical_value, 0, "No_electrical_fault_detected";\n\
                logical_value, 1, "Electrical_fault_detected";\n\
                logical_value, 3, "Signal_unbefuellt"; /* @ErrorValue */\n\
        }\n\
        StatusErrorOverCurrentPxLIN {\n\
                logical_value, 0, "No_overcurrent_detected";\n\
                logical_value, 1, "Overcurrent_detected_Speed_shutdown";\n\
                logical_value, 2, "Overcurrent_detected_Speed_degradation";\n\
                logical_value, 3, "Signal_unbefuellt"; /* @ErrorValue */\n\
        }\n\
        StatusErrorOverTemperaturePxLIN {\n\
                logical_value, 0, "No_overtemperature_detected";\n\
                logical_value, 1, "Overtemperature_detected_Speed_shutdown";\n\
                logical_value, 2, "Overtemperature_detected_Speed_degradation";\n\
                logical_value, 3, "Signal_unbefuellt"; /* @ErrorValue */\n\
        }\n\
        StatusErrorSpeedMonitoringPxLIN {\n\
                logical_value, 0, "No_governor_deviation_detected";\n\
                logical_value, 1, "Governor_deviation_detected";\n\
                logical_value, 2, "Governor_deviation_diagnosis_inactive";\n\
                logical_value, 3, "Signal_unbefuellt"; /* @ErrorValue */\n\
        }\n\
        StatusErrorVoltageOutOfRangePxLIN {\n\
                logical_value, 0, "No_over_or_undervoltage_detected";\n\
                logical_value, 1, "Undervoltage_detected";\n\
                logical_value, 2, "Overvoltage_detected";\n\
                logical_value, 3, "Signal_unbefuellt"; /* @ErrorValue */\n\
        }\n\
        StatusSpeedPxLIN {\n\
                physical_value, 0 , 250 , 1 , 0 , "";\n\
                logical_value, 253, "Funktionsschnittstelle_ist_nicht_verfuegbar";\n\
                logical_value, 254, "Funktion_meldet_Fehler";\n\
                logical_value, 255, "Signal_unbefuellt"; /* @ErrorValue */\n\
        }\n\
        StatusTemperatureActualValuePxLIN {\n\
                physical_value, 0 , 252 , 1 , -49 , "°C";\n\
                logical_value, 253, "Funktionsschnittstelle_ist_nicht_verfuegbar";\n\
                logical_value, 254, "Funktion_meldet_Fehler";\n\
                logical_value, 255, "Signal_unbefuellt"; /* @ErrorValue */\n\
        }\n\
        StatusVoltageActualValuePxLIN {\n\
                physical_value, 0 , 252 , 0.1 , 0 , "V";\n\
                logical_value, 253, "Funktionsschnittstelle_ist_nicht_verfuegbar";\n\
                logical_value, 254, "Funktion_meldet_Fehler";\n\
                logical_value, 255, "Signal_unbefuellt"; /* @ErrorValue */\n\
        }\n\
    }\n\
\n\
Signal_representation {\n\
        ControlCurrentAllowedMaximumPxLIN: ControlCurrentAllowedMaximumP1LIN,ControlCurrentAllowedMaximumP2LIN;\n\
        ControlSpeedPxLIN: ControlSpeedEmergencyRunP1LIN,ControlSpeedEmergencyRunP2LIN,ControlSpeedTargetValueP1LIN,ControlSpeedTargetValueP2LIN;\n\
        StatusCurrentActualValuePxLIN: StatusCurrentActualValueP1LIN,StatusCurrentActualValueP2LIN;\n\
        StatusDataInternalPxLIN: StatusDataInternalP1LIN,StatusDataInternalP2LIN;\n\
        StatusErrorBlockingPxLIN: StatusErrorBlockingP1LIN,StatusErrorBlockingP2LIN;\n\
        StatusErrorDryRunPxLIN: StatusErrorDryRunP1LIN,StatusErrorDryRunP2LIN;\n\
        StatusErrorElectricalFaultPxLIN: StatusErrorElectricalFaultP1LIN,StatusErrorElectricalFaultP2LIN;\n\
        StatusErrorOverCurrentPxLIN: StatusErrorOverCurrentP1LIN,StatusErrorOverCurrentP2LIN;\n\
        StatusErrorOverTemperaturePxLIN: StatusErrorOverTemperatureP1LIN,StatusErrorOverTemperatureP2LIN;\n\
        StatusErrorSpeedMonitoringPxLIN: StatusErrorSpeedMonitoringP1LIN,StatusErrorSpeedMonitoringP2LIN;\n\
        StatusErrorVoltageOutOfRangePxLIN: StatusErrorVoltageOutOfRangeP1LIN,StatusErrorVoltageOutOfRangeP2LIN;\n\
        StatusSpeedPxLIN: StatusSpeedActualValueP1LIN,StatusSpeedActualValueP2LIN,StatusSpeedTargetValueP1LIN,StatusSpeedTargetValueP2LIN;\n\
        StatusTemperatureActualValuePxLIN: StatusTemperatureActualValueP1LIN,StatusTemperatureActualValueP2LIN;\n\
        StatusVoltageActualValuePxLIN: StatusVoltageActualValueP1LIN,StatusVoltageActualValueP2LIN;\n\
    }\n\
\n\
\n\
'