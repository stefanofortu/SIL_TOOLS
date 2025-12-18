import os
from datetime import datetime

from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QColor, QPainter, QIcon
from PySide6.QtWidgets import QGridLayout, QPushButton, QSizePolicy, QSpacerItem, QSpinBox, QWidget, QGroupBox, \
    QComboBox, QVBoxLayout, QHBoxLayout, QLabel, QFileDialog, QMessageBox
import serial.tools.list_ports

from Arduino.Arduino_Communication import Arduino_Communication
from Arduino.Arduino_GUI_elements import PumpRowGroupBox, CircleWidget, \
    Automatic_Mode_Button, TestSequence, ParameterBox
from icons.resources import resource_path
from openpyxl import load_workbook


def list_serial_ports_device():
    """Return a list of available COM ports."""
    ports = serial.tools.list_ports.comports()
    return [port.device for port in ports]


def list_serial_ports_description():
    """Return a list of available COM ports."""
    ports = serial.tools.list_ports.comports()
    ports_list = [f"{port.description}" for port in ports]
    ports_list.sort()
    return ports_list


class Performance_Curves(QWidget):
    def refresh_ports(self):
        """Refresh the COM port list."""
        self.com_ports_combobox.clear()
        self.com_ports_combobox.addItems(list_serial_ports_description())

    def __init__(self):
        super(Performance_Curves, self).__init__()
        self.setObjectName(u"Pwm_Reader_Widget")
        self.arduino_communication = Arduino_Communication()
        self.test_sequence = TestSequence()

        self.main_layout = QVBoxLayout()

        com_port_layout = QHBoxLayout()

        self.label = QLabel("Select COM Port:")
        com_port_layout.addWidget(self.label)

        self.com_ports_combobox = QComboBox()
        self.com_ports_combobox.addItems(list_serial_ports_description())
        com_port_layout.addWidget(self.com_ports_combobox)

        self.refresh_button = QPushButton("")
        self.refresh_button.clicked.connect(self.refresh_ports)
        self.refresh_button.setIcon(QIcon(resource_path("reload.png")))
        #self.refresh_button.setFixedSize(32, 32)
        com_port_layout.addWidget(self.refresh_button)

        self.connect_button = QPushButton("Connect")
        self.connect_button.setStyleSheet("""
            QPushButton {
                background-color: #195977;
                color: white;
                border-radius: 5px;
                padding: 4px 8px;
            }
            QPushButton:hover { background-color: #1e688c; }
            QPushButton:disabled { background-color: #a0a0a0; color: #666666; }
        """)
        self.connect_button.clicked.connect(self.start_arduino_communication)
        self.connect_button.setIcon(QIcon(resource_path("connect.png")))
        #self.refresh_button.setFixedSize(32, 32)
        com_port_layout.addWidget(self.connect_button)

        self.disconnect_button = QPushButton("Disconnect")
        self.disconnect_button.setStyleSheet("""
            QPushButton {
                background-color: #195977;
                color: white;
                border-radius: 5px;
                padding: 4px 8px;
            }
            QPushButton:hover { background-color: #1e688c; }
            QPushButton:disabled { background-color: #a0a0a0; color: #666666; }
        """)
        self.disconnect_button.clicked.connect(self.stop_arduino_communication)
        self.disconnect_button.setIcon(QIcon(resource_path("disconnect.png")))
        #self.refresh_button.setFixedSize(32, 32)
        com_port_layout.addWidget(self.disconnect_button)

        # Add small circle widget
        self.circle_widget_com = CircleWidget(diameter=18, color="orange")
        com_port_layout.addWidget(self.circle_widget_com)
        com_port_layout.addStretch()
        self.main_layout.addLayout(com_port_layout)

        manual_mode_layout = QHBoxLayout()
        switch_button_label = QLabel("Select operating mode: ")
        manual_mode_layout.addWidget(switch_button_label)

        self.btn_auto_mode = Automatic_Mode_Button()
        self.btn_auto_mode.clicked.connect(self.automatic_button_action)
        #manual_mode_layout.addStretch()
        manual_mode_layout.addWidget(self.btn_auto_mode)
        manual_mode_layout.addStretch()
        self.main_layout.addLayout(manual_mode_layout)

        self.gridLayout = QGridLayout()
        self.eValve_box = ParameterBox(parameter_name="ElettroValvola", parameter_id=10,
                                   min_value=0, max_value=10000, label="mV",
                                   serial_communication=self.arduino_communication)
        self.gridLayout.addWidget(self.eValve_box,0,0)
        self.gridLayout.addItem(QSpacerItem(10, 20, QSizePolicy.Fixed, QSizePolicy.Minimum), 0, 1)

        self.read_box = ParameterBox(parameter_name="Read", parameter_id=10,
                                   min_value=0, max_value=1, label="",
                                   serial_communication=self.arduino_communication)
        self.gridLayout.addWidget(self.read_box,0,2)
        self.gridLayout.addItem(QSpacerItem(10, 20, QSizePolicy.Fixed, QSizePolicy.Minimum), 0, 3)

        self.main_layout.addLayout(self.gridLayout)
        # --- Layout inferiore ---
        layout_automatic_mode = QHBoxLayout()
        # Start e Stop
        self.btn_start = QPushButton("▶ Start")
        self.btn_start.setStyleSheet("""
            QPushButton {
                background-color: #28a745;
                color: white;
                border-radius: 10px;
                padding: 6px 12px;
                font-weight: bold;
            }
            QPushButton:hover { background-color: #218838; }
            QPushButton:disabled { background-color: #a0a0a0; color: #666666; }
        """)
        self.btn_start.setEnabled(False)
        self.btn_start.clicked.connect(self.start_action)
        layout_automatic_mode.addWidget(self.btn_start)

        self.btn_stop = QPushButton("■ Stop")
        self.btn_stop.setStyleSheet("""
            QPushButton {
                background-color: #dc3545;
                color: white;
                border-radius: 10px;
                padding: 6px 12px;
                font-weight: bold;
            }
            QPushButton:hover { background-color: #c82333; }
            QPushButton:disabled { background-color: #a0a0a0; color: #666666; }
        """)
        self.btn_stop.setEnabled(False)
        self.btn_stop.clicked.connect(self.stop_action)
        layout_automatic_mode.addWidget(self.btn_stop)

        # Bottone Load Excel
        self.btn_load_excel = QPushButton("Change Curve Coonfiguration Excel")
        self.btn_load_excel.setIcon(QIcon.fromTheme("document-open"))
        self.btn_load_excel.clicked.connect(self.load_excel)
        self.btn_load_excel.setEnabled(False)

        # Stile simile a Start/Stop
        self.btn_load_excel.setStyleSheet("""
            QPushButton {
                background-color: #007bff;  /* blu */
                color: white;
                border-radius: 10px;
                padding: 6px 12px;
                font-weight: bold;
            }
            QPushButton:hover:!disabled { background-color: #0069d9; }
            QPushButton:disabled { background-color: #a0a0a0; color: #666666; }
        """)
        layout_automatic_mode.addWidget(self.btn_load_excel)

        # Label per mostrare il nome del file
        self.label_file = QLabel("Nessun file selezionato")
        layout_automatic_mode.addWidget(self.label_file)

        self.main_layout.addLayout(layout_automatic_mode)
        self.main_layout.addStretch()
        ############### SET MAIN LAYOUT
        self.setLayout(self.main_layout)
        ############### GUI END

        #######################################################################
        self.timer_feedback = QTimer()
        self.timer_feedback.timeout.connect(self.check_feedback_status)
        self.timer_feedback.start(4000)
        self.current_pump_feedback = 1
        #######################################################################
        # Timer per il "player"
        self.timer_automatic_mode = QTimer()
        self.timer_automatic_mode.timeout.connect(self.next_row)
        self.current_index = 0
        self.data = []

    def start_arduino_communication(self):
        res = self.arduino_communication.start(serial_port_name=self.com_ports_combobox.currentText())
        if res == 1:
            self.circle_widget_com.setColor("green")
        elif res == -1:
            self.circle_widget_com.setColor("red")
        else:
            self.circle_widget_com.setColor("orange")
        self.read_pwm_status()

    def stop_arduino_communication(self):
        self.arduino_communication.close()
        self.circle_widget_com.setColor("red")

    def write_arduino_message(self, message):
        self.arduino_communication.write_message(message=message, verbose=True)

    def read_pwm_status(self):
        if self.arduino_communication.is_connected():
            DUTY_CYCLE_PARAMETER_ID_OFFSET = 16
            for pump_index in range(1, 11):
                parameter_id = DUTY_CYCLE_PARAMETER_ID_OFFSET + pump_index
                message = f"3:{parameter_id:02X}"
                #print(f"message sent {message}")
                reply = self.arduino_communication.write_message(message=message, verbose=False)
                #print(f"reply got {reply}")
                parts = reply.split(":")
                reply_frame_id_hex = parts[0]
                reply_param_id_hex = parts[1]
                reply_value_hex = parts[2]
                # print(parts)
                if reply_frame_id_hex != "3":
                    print("Reply message KO")
                else:
                    if int(reply_param_id_hex, 16) != parameter_id:
                        print("Reply parameter KO")
                    else:
                        # print(f"OK {reply_parameter_id_hex}")
                        if reply_param_id_hex == "11":
                            self.row_group_box_pump_01.update_pwm_speed(reply_value_hex)
                        if reply_param_id_hex == "12": self.row_group_box_pump_02.update_pwm_speed(
                            reply_value_hex)
                        if reply_param_id_hex == "13": self.row_group_box_pump_03.update_pwm_speed(
                            reply_value_hex)
                        if reply_param_id_hex == "14": self.row_group_box_pump_04.update_pwm_speed(
                            reply_value_hex)
                        if reply_param_id_hex == "15": self.row_group_box_pump_05.update_pwm_speed(
                            reply_value_hex)
                        if reply_param_id_hex == "16": self.row_group_box_pump_06.update_pwm_speed(
                            reply_value_hex)
                        if reply_param_id_hex == "17": self.row_group_box_pump_07.update_pwm_speed(
                            reply_value_hex)
                        if reply_param_id_hex == "18": self.row_group_box_pump_08.update_pwm_speed(
                            reply_value_hex)
                        if reply_param_id_hex == "19": self.row_group_box_pump_09.update_pwm_speed(
                            reply_value_hex)
                        if reply_param_id_hex == "1A": self.row_group_box_pump_10.update_pwm_speed(
                            reply_value_hex)

    def check_feedback_status(self):
        if self.arduino_communication.is_connected():
            pump_reply_parameter_offset = 32
            parameter_id = pump_reply_parameter_offset + self.current_pump_feedback
            message = f"3:{parameter_id:02X}"
            #print(f"message sent {message}")
            reply = self.arduino_communication.write_message(message=message, verbose=False)
            #print(f"reply got {reply}")
            parts = reply.split(":")
            reply_frame_id_hex = parts[0]
            reply_parameter_id_hex = parts[1]
            reply_value_hex = parts[2]
            #print(parts)
            if reply_frame_id_hex != "3":
                print("Reply message KO")
            else:
                if int(reply_parameter_id_hex, 16) != parameter_id:
                    print("Reply parameter KO")
                else:
                    #print(f"OK {reply_parameter_id_hex}")
                    if reply_parameter_id_hex == "21": self.row_group_box_pump_01.update_pump_status(reply_value_hex)
                    if reply_parameter_id_hex == "22": self.row_group_box_pump_02.update_pump_status(reply_value_hex)
                    if reply_parameter_id_hex == "23": self.row_group_box_pump_03.update_pump_status(reply_value_hex)
                    if reply_parameter_id_hex == "24": self.row_group_box_pump_04.update_pump_status(reply_value_hex)
                    if reply_parameter_id_hex == "25": self.row_group_box_pump_05.update_pump_status(reply_value_hex)
                    if reply_parameter_id_hex == "26": self.row_group_box_pump_06.update_pump_status(reply_value_hex)
                    if reply_parameter_id_hex == "27": self.row_group_box_pump_07.update_pump_status(reply_value_hex)
                    if reply_parameter_id_hex == "28": self.row_group_box_pump_08.update_pump_status(reply_value_hex)
                    if reply_parameter_id_hex == "29": self.row_group_box_pump_09.update_pump_status(reply_value_hex)
                    if reply_parameter_id_hex == "2A": self.row_group_box_pump_10.update_pump_status(reply_value_hex)

            self.current_pump_feedback += 1
            if self.current_pump_feedback > 10:
                self.current_pump_feedback = 1

    def automatic_button_action(self):
        if self.btn_auto_mode.automatic_mode_active():
            self.btn_load_excel.setDisabled(False)
            self.load_excel(file_path="C:\\Users\\stefano.fortunati\\PythonProjects\\SIL_TOOLS\\Arduino\\Curves_Cfg\\Test_Sequence_Example.xlsx")
            self.btn_start.setDisabled(False)
            self.btn_stop.setDisabled(True)
            self.eValve_box.disable_manual_input(True)
            self.read_box.disable_manual_input(True)
        else:
            self.btn_load_excel.setDisabled(True)
            self.btn_start.setDisabled(True)
            self.btn_stop.setDisabled(True)
            self.eValve_box.enable_manual_input(True)
            self.read_box.enable_manual_input(True)

    def load_excel(self, file_path=None):
        if not file_path:
            # Apri finestra dialogo per Excel
            file_path, _ = QFileDialog.getOpenFileName(
                self, "Open Excel File", "", "Excel Files (*.xlsx *.xls)"
            )
        #print(file_path)
        try:
            self.test_sequence.load_from_file(file_path, verbose=True)
        except FileNotFoundError:
            QMessageBox.critical(self, "Errore", f"File non trovato\n")
            return []
        except IndentationError:
            QMessageBox.critical(self, "Errore", "Il file Excel non è formattato correttamente")
            return []
        except Exception as e:
            QMessageBox.critical(self, "Errore", f"Impossibile leggere il file:\n{e}")
            return []

        # Stampa numero di righe non vuote
        QMessageBox.information(self, "Excel Caricato", f"File caricato correttamente\n"
                                                        f"Numero di step di test: {len(self.test_sequence)}")
        self.btn_start.setEnabled(True)

        if not self.test_sequence.empty:
            file_name = os.path.basename(file_path)
            self.label_file.setText(file_name)

    def start_action(self):
        # Abilita Stop e disabilita Start
        self.btn_stop.setEnabled(True)
        self.btn_start.setEnabled(False)
        self.start_time = 0  # riferimento tempo iniziale
        self.timer_automatic_mode.start(100)  # timer veloce, calcola ritardo dai tempi
        timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-5]  # hh:mm:ss.mmm
        print(f"[{timestamp}] Test started:")
        self.current_index = 0
        self.timer_automatic_mode.start(100)

    def stop_action(self):
        self.timer_automatic_mode.stop()
        # Disabilita Stop e abilita Start
        self.btn_stop.setEnabled(False)
        self.btn_start.setEnabled(True)
        timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-5]  # hh:mm:ss.mmm
        print(f"[{timestamp}] Test completed:")

    def next_row(self):
        # Stampa con timestamp corrente
        timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-5]  # hh:mm:ss.mmm

        if self.current_index < len(self.test_sequence):
            param = self.test_sequence.loc[self.current_index, "Parameter"]
            value = self.test_sequence.loc[self.current_index, "Value"]
            print(f"[{timestamp}] Parameter: {param}, Value: {value}")

            # Calcolo intervallo per la prossima riga
            if self.current_index < len(self.test_sequence) - 1:
                delay = self.test_sequence.loc[self.current_index, "Delay[s]"]
                interval = max(0, delay * 1000)  # converti in ms
                self.timer_automatic_mode.start(interval)

            self.current_index += 1
        else:
            self.timer_automatic_mode.stop()
            self.btn_stop.setEnabled(False)
            self.btn_start.setEnabled(True)
            print(f"[{timestamp}] Test completed")
            return
