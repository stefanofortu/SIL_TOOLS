from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QPainter, QIcon
from PySide6.QtWidgets import QGridLayout, QLabel, QPushButton, QSizePolicy, QWidget, \
    QSpacerItem, QSpinBox, QWidget, QGroupBox, QHBoxLayout, QComboBox, QVBoxLayout

import serial.tools.list_ports

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
        self.combo.clear()
        self.combo.addItems(list_serial_ports_description())

    def setup_arduino_communication(self):
        self.selected_serial_port = self.combo.currentText()
        port_device = None
        ports = serial.tools.list_ports.comports()
        for port in ports:
            if self.selected_serial_port == port.description:
                port_device = port.device
                print(port_device)
        if port_device:
            if self.arduino_serial:
                if self.arduino_serial.is_open:
                    self.arduino_serial.close()
            try:
                self.arduino_serial = serial.Serial(port=port_device, baudrate=9600, timeout=1)
                print(f"✅ Connected to {self.selected_serial_port}")
                self.circle_widget_com.setColor("green")
            except serial.SerialException as e:
                print(f"❌ SerialException: {e}")
                self.circle_widget_com.setColor("red")
            except ValueError as e:
                print(f"❌ ValueError: {e}")
                self.circle_widget_com.setColor("red")
            except Exception as e:
                print(f"❌ Unexpected error: {e}")
                self.circle_widget_com.setColor("red")

        #if self.arduino_serial:
        #    self.circle_widget_com.setColor("green")
        #else:
        #    self.circle_widget_com.setColor("red")

    def __init__(self):
        super(Pwm_Reader_Widget, self).__init__()
        self.setObjectName(u"Arduino_Widget")
        self.arduino_serial = None
        self.selected_serial_port = None

        self.main_layout = QVBoxLayout()

        com_port_layout = QHBoxLayout()

        self.label = QLabel("Select COM Port:")
        com_port_layout.addWidget(self.label)

        self.combo = QComboBox()
        self.combo.addItems(list_serial_ports_description())
        self.combo.currentIndexChanged.connect(self.setup_arduino_communication)
        com_port_layout.addWidget(self.combo)

        self.refresh_button = QPushButton("")
        self.refresh_button.clicked.connect(self.refresh_ports)
        self.refresh_button.setIcon(QIcon(resource_path("reload.png")))
        #self.refresh_button.setFixedSize(32, 32)
        com_port_layout.addWidget(self.refresh_button)
        # Add small circle widget
        self.circle_widget_com = CircleWidget(diameter=18, color="orange")
        com_port_layout.addWidget(self.circle_widget_com)

        com_port_layout.addStretch()
        self.main_layout.addLayout(com_port_layout)

        self.gridLayout = QGridLayout()

        self.row_group_box_pump_01 = PumpRowGroupBox(name="Pump 01", pump_id=1)
        self.gridLayout.addWidget(self.row_group_box_pump_01, 0, 0)
        self.gridLayout.addItem(QSpacerItem(10, 20, QSizePolicy.Fixed, QSizePolicy.Minimum), 0, 1)
        self.row_group_box_pump_02 = PumpRowGroupBox("Pump 02", pump_id=2)
        self.gridLayout.addWidget(self.row_group_box_pump_02, 0, 2)

        self.row_group_box_pump_03 = PumpRowGroupBox(name="Pump 03", pump_id=3)
        self.gridLayout.addWidget(self.row_group_box_pump_03, 1, 0)
        self.gridLayout.addItem(QSpacerItem(10, 20, QSizePolicy.Fixed, QSizePolicy.Minimum), 1, 1)
        self.row_group_box_pump_04 = PumpRowGroupBox(name="Pump 04", pump_id=4)
        self.gridLayout.addWidget(self.row_group_box_pump_04, 1, 2)

        self.row_group_box_pump_05 = PumpRowGroupBox(name="Pump 05", pump_id=5)
        self.gridLayout.addWidget(self.row_group_box_pump_05, 2, 0)
        self.gridLayout.addItem(QSpacerItem(10, 20, QSizePolicy.Fixed, QSizePolicy.Minimum), 2, 1)
        self.row_group_box_pump_06 = PumpRowGroupBox(name="Pump 06", pump_id=6)
        self.gridLayout.addWidget(self.row_group_box_pump_06, 2, 2)

        self.row_group_box_pump_07 = PumpRowGroupBox(name="Pump 07", pump_id=7)
        self.gridLayout.addWidget(self.row_group_box_pump_07, 3, 0)
        self.gridLayout.addItem(QSpacerItem(10, 20, QSizePolicy.Fixed, QSizePolicy.Minimum), 3, 1)
        self.row_group_box_pump_08 = PumpRowGroupBox("Pump 08", pump_id=8)
        self.gridLayout.addWidget(self.row_group_box_pump_08, 3, 2)

        self.row_group_box_pump_09 = PumpRowGroupBox(name="Pump 09", pump_id=9)
        self.gridLayout.addWidget(self.row_group_box_pump_09, 4, 0)
        self.gridLayout.addItem(QSpacerItem(10, 20, QSizePolicy.Fixed, QSizePolicy.Minimum), 4, 1)
        self.row_group_box_pump_10 = PumpRowGroupBox(name="Pump 10", pump_id=10)
        self.gridLayout.addWidget(self.row_group_box_pump_10, 4, 2)

        self.main_layout.addLayout(self.gridLayout)
        ############### SET MAIN LAYOUT
        self.setLayout(self.main_layout)
        ############### GUI END


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
    def __init__(self, name, pump_id):
        super(PumpRowGroupBox, self).__init__()
        self.pump_id = pump_id
        self.setTitle(name)

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
        set_speed_button.pressed.connect(lambda: self.set_speed(self.pump_id, self.spin_box_pump_speed.value()))

        group_layout.addWidget(set_speed_button)

        # Add explandable spacer
        group_layout.addStretch()

        # Add fixed-width spacer
        group_layout.addItem(QSpacerItem(20, 20, QSizePolicy.Fixed, QSizePolicy.Minimum))

        group_layout.addWidget(QLabel("Status :"))

        label_pump_status = QLabel("xxxx ms (FEEDBACK OK)")
        label_pump_status.setStyleSheet("background-color: white; padding: 5px;")
        group_layout.addWidget(label_pump_status)

        # Add small circle widget
        self.circle_widget_pump_01 = CircleWidget(diameter=18, color="red")
        group_layout.addWidget(self.circle_widget_pump_01)
        self.circle_widget_pump_01.setColor("orange")

        # Add another fixed-width spacer
        group_layout.addItem(QSpacerItem(20, 20, QSizePolicy.Fixed, QSizePolicy.Minimum))

        self.setLayout(group_layout)

    def set_speed(self, pump_id, set_value):
        print(f"Hello {pump_id}, {set_value}")

    def temp_function(self):
        import serial
        import time
        import struct



        arduino = serial.Serial(port='COM6', baudrate=9600, timeout=1)  # Cambia COM se sei su Windows
        time.sleep(2)  # Attendi avvio seriale

        def arduino_query(command):
            arduino.write((command + '\n').encode())
            time.sleep(0.1)
            reply = arduino.readline().decode().strip()
            if reply:
                encode_response(reply)

        # def arduino_query_binary(command):
        #     arduino.write((command + '\n').encode())
        #     dati = [2, 01, 50]
        #     # 3 bytes:
        #     # Posizione 1:
        #     #   - 1 --> richiedi status
        #     #   - 2 --> cambia duty cycle
        #     # Posizione 2: numero dell'output
        #     # Posizione 3: valore di duty cycle se byte pos1 == 1,
        #     arduino.write(bytes(dati))  # invia tutti i byte
        #     time.sleep(0.1)
        #     packet = arduino.read(20)  # Read 20 bytes
        #     if len(packet) == 10:
        #         values = struct.unpack('<10B', packet)  # 20 unsigned 8-bit values
        #         print("Received:", values)

        def encode_response(reply):
            print("Valore ricevuto:", reply)

        while True:
            # Esempi d'uso
            arduino_query("1:0:0")
            time.sleep(4)
            arduino_query("2:1:10")
            time.sleep(4)
            arduino_query("2:01:25")
            time.sleep(4)
            arduino_query("2:01:50")
            time.sleep(4)
            arduino_query("2:01:75")
            time.sleep(4)
            arduino_query("2:01:100")
            time.sleep(4)
