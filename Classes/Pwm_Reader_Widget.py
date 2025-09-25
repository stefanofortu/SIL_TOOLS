from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QPainter
from PySide6.QtWidgets import QGridLayout, QLabel,QPushButton, QSizePolicy, QWidget,\
    QSpacerItem, QSpinBox, QWidget, QGroupBox, QHBoxLayout


class Pwm_Reader_Widget(QWidget):
    def __init__(self):
        super(Pwm_Reader_Widget, self).__init__()
        self.setObjectName(u"Arduino_Widget")

        self.gridLayout = QGridLayout()

        self.row_group_box_pump_01 = PumpRowGroupBox("Pump 01")
        self.gridLayout.addWidget(self.row_group_box_pump_01, 0, 0)
        self.gridLayout.addItem(QSpacerItem(10, 20, QSizePolicy.Fixed, QSizePolicy.Minimum), 0, 1)
        self.row_group_box_pump_02 = PumpRowGroupBox("Pump 02")
        self.gridLayout.addWidget(self.row_group_box_pump_02, 0, 2)

        self.row_group_box_pump_03 = PumpRowGroupBox("Pump 03")
        self.gridLayout.addWidget(self.row_group_box_pump_03, 1, 0)
        self.gridLayout.addItem(QSpacerItem(10, 20, QSizePolicy.Fixed, QSizePolicy.Minimum), 1, 1)
        self.row_group_box_pump_04 = PumpRowGroupBox("Pump 04")
        self.gridLayout.addWidget(self.row_group_box_pump_04, 1, 2)

        self.row_group_box_pump_05 = PumpRowGroupBox("Pump 05")
        self.gridLayout.addWidget(self.row_group_box_pump_05, 2, 0)
        self.gridLayout.addItem(QSpacerItem(10, 20, QSizePolicy.Fixed, QSizePolicy.Minimum), 2, 1)
        self.row_group_box_pump_06 = PumpRowGroupBox("Pump 06")
        self.gridLayout.addWidget(self.row_group_box_pump_06, 2, 2)

        self.row_group_box_pump_07 = PumpRowGroupBox("Pump 07")
        self.gridLayout.addWidget(self.row_group_box_pump_07, 3, 0)
        self.gridLayout.addItem(QSpacerItem(10, 20, QSizePolicy.Fixed, QSizePolicy.Minimum), 3, 1)
        self.row_group_box_pump_08 = PumpRowGroupBox("Pump 08")
        self.gridLayout.addWidget(self.row_group_box_pump_08, 3, 2)

        self.row_group_box_pump_09 = PumpRowGroupBox("Pump 09")
        self.gridLayout.addWidget(self.row_group_box_pump_09, 4, 0)
        self.gridLayout.addItem(QSpacerItem(10, 20, QSizePolicy.Fixed, QSizePolicy.Minimum), 4, 1)
        self.row_group_box_pump_10 = PumpRowGroupBox("Pump 10")
        self.gridLayout.addWidget(self.row_group_box_pump_10, 4, 2)

        ############### SET MAIN LAYOUT
        self.setLayout(self.gridLayout)
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
    def __init__(self, name):
        super(PumpRowGroupBox, self).__init__()

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

        spin_box_pump_speed = QSpinBox(self)
        spin_box_pump_speed.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        spin_box_pump_speed.setMinimumWidth(75)
        spin_box_pump_speed.setMaximum(100)
        spin_box_pump_speed.setSuffix(" %")
        group_layout.addWidget(spin_box_pump_speed)

        set_speed_button = QPushButton(self)
        set_speed_button.setText("Set ➡")
        set_speed_button.setStyleSheet("font-weight: bold;")
        set_speed_button.setMaximumWidth(75)
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
