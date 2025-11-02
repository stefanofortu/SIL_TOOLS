import time

from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QColor, QPainter, QIcon
from PySide6.QtWidgets import QGridLayout, QLabel, QPushButton, QSizePolicy, QWidget, \
    QSpacerItem, QSpinBox, QWidget, QGroupBox, QHBoxLayout, QComboBox, QVBoxLayout
import serial.tools.list_ports

from Classes.Arduino_Communication import Arduino_Communication
from icons.resources import resource_path


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


class Pwm_Reader_Widget(QWidget):
    def refresh_ports(self):
        """Refresh the COM port list."""
        self.com_ports_combobox.clear()
        self.com_ports_combobox.addItems(list_serial_ports_description())

    def __init__(self):
        super(Pwm_Reader_Widget, self).__init__()
        self.setObjectName(u"Pwm_Reader_Widget")
        self.arduino_communication = Arduino_Communication()

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
        self.connect_button.clicked.connect(self.start_arduino_communication)
        self.connect_button.setIcon(QIcon(resource_path("connect.png")))
        #self.refresh_button.setFixedSize(32, 32)
        com_port_layout.addWidget(self.connect_button)

        self.connect_button = QPushButton("Disconnect")
        self.connect_button.clicked.connect(self.stop_arduino_communication)
        self.connect_button.setIcon(QIcon(resource_path("disconnect.png")))
        #self.refresh_button.setFixedSize(32, 32)
        com_port_layout.addWidget(self.connect_button)

        # Add small circle widget
        self.circle_widget_com = CircleWidget(diameter=18, color="orange")
        com_port_layout.addWidget(self.circle_widget_com)

        com_port_layout.addStretch()
        self.main_layout.addLayout(com_port_layout)

        self.gridLayout = QGridLayout()

        self.row_group_box_pump_01 = PumpRowGroupBox(name="Pump 01", pump_id=1,
                                                     serial_communication=self.arduino_communication)
        self.gridLayout.addWidget(self.row_group_box_pump_01, 0, 0)
        self.gridLayout.addItem(QSpacerItem(10, 20, QSizePolicy.Fixed, QSizePolicy.Minimum), 0, 1)
        self.row_group_box_pump_02 = PumpRowGroupBox("Pump 02", pump_id=2,
                                                     serial_communication=self.arduino_communication)
        self.gridLayout.addWidget(self.row_group_box_pump_02, 0, 2)

        self.row_group_box_pump_03 = PumpRowGroupBox(name="Pump 03", pump_id=3,
                                                     serial_communication=self.arduino_communication)
        self.gridLayout.addWidget(self.row_group_box_pump_03, 1, 0)
        self.gridLayout.addItem(QSpacerItem(10, 20, QSizePolicy.Fixed, QSizePolicy.Minimum), 1, 1)
        self.row_group_box_pump_04 = PumpRowGroupBox(name="Pump 04", pump_id=4,
                                                     serial_communication=self.arduino_communication)
        self.gridLayout.addWidget(self.row_group_box_pump_04, 1, 2)

        self.row_group_box_pump_05 = PumpRowGroupBox(name="Pump 05", pump_id=5,
                                                     serial_communication=self.arduino_communication)
        self.gridLayout.addWidget(self.row_group_box_pump_05, 2, 0)
        self.gridLayout.addItem(QSpacerItem(10, 20, QSizePolicy.Fixed, QSizePolicy.Minimum), 2, 1)
        self.row_group_box_pump_06 = PumpRowGroupBox(name="Pump 06", pump_id=6,
                                                     serial_communication=self.arduino_communication)
        self.gridLayout.addWidget(self.row_group_box_pump_06, 2, 2)

        self.row_group_box_pump_07 = PumpRowGroupBox(name="Pump 07", pump_id=7,
                                                     serial_communication=self.arduino_communication)
        self.gridLayout.addWidget(self.row_group_box_pump_07, 3, 0)
        self.gridLayout.addItem(QSpacerItem(10, 20, QSizePolicy.Fixed, QSizePolicy.Minimum), 3, 1)
        self.row_group_box_pump_08 = PumpRowGroupBox("Pump 08", pump_id=8,
                                                     serial_communication=self.arduino_communication)
        self.gridLayout.addWidget(self.row_group_box_pump_08, 3, 2)

        self.row_group_box_pump_09 = PumpRowGroupBox(name="Pump 09", pump_id=9,
                                                     serial_communication=self.arduino_communication)
        self.gridLayout.addWidget(self.row_group_box_pump_09, 4, 0)
        self.gridLayout.addItem(QSpacerItem(10, 20, QSizePolicy.Fixed, QSizePolicy.Minimum), 4, 1)
        self.row_group_box_pump_10 = PumpRowGroupBox(name="Pump 10", pump_id=10,
                                                     serial_communication=self.arduino_communication)
        self.gridLayout.addWidget(self.row_group_box_pump_10, 4, 2)

        self.main_layout.addLayout(self.gridLayout)
        ############### SET MAIN LAYOUT
        self.setLayout(self.main_layout)
        ############### GUI END

        self.timer = QTimer()
        self.timer.timeout.connect(self.check_feedback_status)
        self.timer.start(4000)
        self.current_pump_feedback = 1

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
                reply_parameter_id_hex = parts[1]
                reply_value_hex = parts[2]
                # print(parts)
                if reply_frame_id_hex != "3":
                    print("Reply message KO")
                else:
                    if int(reply_parameter_id_hex, 16) != parameter_id:
                        print("Reply parameter KO")
                    else:
                        # print(f"OK {reply_parameter_id_hex}")
                        if reply_parameter_id_hex == "11": self.row_group_box_pump_01.update_pwm_speed(
                            reply_value_hex)
                        if reply_parameter_id_hex == "12": self.row_group_box_pump_02.update_pwm_speed(
                            reply_value_hex)
                        if reply_parameter_id_hex == "13": self.row_group_box_pump_03.update_pwm_speed(
                            reply_value_hex)
                        if reply_parameter_id_hex == "14": self.row_group_box_pump_04.update_pwm_speed(
                            reply_value_hex)
                        if reply_parameter_id_hex == "15": self.row_group_box_pump_05.update_pwm_speed(
                            reply_value_hex)
                        if reply_parameter_id_hex == "16": self.row_group_box_pump_06.update_pwm_speed(
                            reply_value_hex)
                        if reply_parameter_id_hex == "17": self.row_group_box_pump_07.update_pwm_speed(
                            reply_value_hex)
                        if reply_parameter_id_hex == "18": self.row_group_box_pump_08.update_pwm_speed(
                            reply_value_hex)
                        if reply_parameter_id_hex == "19": self.row_group_box_pump_09.update_pwm_speed(
                            reply_value_hex)
                        if reply_parameter_id_hex == "1A": self.row_group_box_pump_10.update_pwm_speed(
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


class CircleWidget(QWidget):
    def __init__(self, diameter=20, color="red"):
        super().__init__()
        self.diameter = diameter
        self.color = color
        self.setFixedSize(diameter, diameter)  # ensure the widget stays square

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(QColor(self.color))
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(0, 0, self.diameter, self.diameter)

    def setColor(self, new_color):
        self.color = QColor(new_color)
        self.update()  # Trigger repaint


class PumpRowGroupBox(QGroupBox):
    def __init__(self, name, pump_id, serial_communication):
        super(PumpRowGroupBox, self).__init__()
        self.pump_id = pump_id
        self.setTitle(name)
        self.group_box_serial_communication = serial_communication

        self.setStyleSheet("""
        QGroupBox::title {
           subcontrol-origin: margin; padding: 0 5px; color: darkblue;
            }
        QGroupBox {
            font-size: 14px;
            font-weight: bold;
            border: 1px solid blue;
            border-radius: 5px;
            margin-top: 16px;
            }
        """)
        group_layout = QHBoxLayout()

        group_layout.addWidget(QLabel("Speed"))

        self.spin_box_pump_speed = QSpinBox(self)
        self.spin_box_pump_speed.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        self.spin_box_pump_speed.setMinimumWidth(75)
        self.spin_box_pump_speed.setMaximum(100)
        self.spin_box_pump_speed.setSuffix(" %")
        group_layout.addWidget(self.spin_box_pump_speed)

        set_speed_button = QPushButton(self)
        set_speed_button.setText("Set ➡")
        set_speed_button.setStyleSheet("font-weight: bold;")
        set_speed_button.setMaximumWidth(75)
        set_speed_button.pressed.connect(
            lambda: self.set_pwm_speed(pump_id=self.pump_id,
                                       speed_value=self.spin_box_pump_speed.value())
        )

        group_layout.addWidget(set_speed_button)

        # Add explandable spacer
        group_layout.addStretch()

        # Add fixed-width spacer
        group_layout.addItem(QSpacerItem(20, 20, QSizePolicy.Fixed, QSizePolicy.Minimum))

        group_layout.addWidget(QLabel("Status :"))

        self.label_pump_status = QLabel("xxxx ms ()")
        self.label_pump_status.setStyleSheet("background-color: white; padding: 5px;")
        group_layout.addWidget(self.label_pump_status)

        # Add small circle widget
        self.circle_widget_pump = CircleWidget(diameter=18, color="red")
        group_layout.addWidget(self.circle_widget_pump)
        self.circle_widget_pump.setColor("orange")

        # Add another fixed-width spacer
        group_layout.addItem(QSpacerItem(20, 20, QSizePolicy.Fixed, QSizePolicy.Minimum))

        self.setLayout(group_layout)

    def set_pwm_speed(self, pump_id, speed_value):
        print("==================================")
        print("========SET DUTY===================")
        duty_cycle_parameter_offset = 16
        parameter_id = duty_cycle_parameter_offset + pump_id
        message = f"4:{parameter_id:02X}:{speed_value:02X}"
        self.group_box_serial_communication.write_message(message=message, verbose=True)

    def update_pwm_speed(self, value_hex):
        value_dec = int(value_hex, 16)
        self.spin_box_pump_speed.setValue(value_dec)

    def update_pump_status(self, value_hex):
        value_dec = int(value_hex, 16)
        value_dec = value_dec % 2500
        pump_status = ""
        if 450 <= value_dec <= 550:
            pump_status = "FEEDBACK OK"
            self.circle_widget_pump.setColor("green")
        elif 950 <= value_dec <= 1050:
            pump_status = "DRY RUN"
            self.circle_widget_pump.setColor("red")
        elif 1450 <= value_dec <= 1550:
            pump_status = "OVERTEMPERATURE"
            self.circle_widget_pump.setColor("red")
        elif 1950 <= value_dec <= 2050:
            pump_status = "UNDER-OVER-VOLTAGE"
            self.circle_widget_pump.setColor("red")
        else:
            pump_status = "UNKNOWN"
            self.circle_widget_pump.setColor("orange")

        self.label_pump_status.setText(f"{value_dec} ms ({pump_status})")
