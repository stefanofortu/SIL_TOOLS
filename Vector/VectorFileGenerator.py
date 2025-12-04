import sys
from PySide6.QtWidgets import (
    QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QFileDialog, QLabel
)
from PySide6.QtCore import Qt
from pathlib import Path

from Vector.LDF_replacer import replace_LDF
from Vector.CAPL_VALVES_replacer import replace_CAPL_VALVES
from Vector.CAPL_replacer import replace_CAPL


class VectorFileGenerator(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Apri File")
        self.setMinimumSize(500, 100)
        # Layout principale (verticale, nel caso serva aggiungere altro)
        main_layout = QVBoxLayout()

        self.CAPL_file_path = None
        CAPL_selection_button = QPushButton("Select CAPL", self)
        CAPL_selection_button.setMaximumWidth(150)
        CAPL_selection_button.clicked.connect(self.CAPL_open_file)
        self.CAPL_label = QLabel("No file selected", self)
        self.CAPL_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        CAPL_convert_button = QPushButton("Run", self)
        CAPL_convert_button.setMaximumWidth(100)
        CAPL_convert_button.clicked.connect(self.CAPL_convert)
        # Layout orizzontale per bottone + etichetta
        CAPL_layout = QHBoxLayout()
        CAPL_layout.addWidget(CAPL_selection_button)
        CAPL_layout.addWidget(self.CAPL_label)
        CAPL_layout.addWidget(CAPL_convert_button)
        main_layout.addLayout(CAPL_layout)

        self.CAPL_TMM_file_path = None
        VALVE_selection_button = QPushButton("Select VALVE", self)
        VALVE_selection_button.setMaximumWidth(150)
        VALVE_selection_button.clicked.connect(self.CAPL_TMM_open_file)
        self.VALVE_label = QLabel("No file selected", self)
        self.VALVE_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        VALVE_convert_button = QPushButton("Run", self)
        VALVE_convert_button.setMaximumWidth(100)
        VALVE_convert_button.clicked.connect(self.CAPL_TMM_convert)
        # Layout orizzontale per bottone + etichetta
        VALVE_layout = QHBoxLayout()
        VALVE_layout.addWidget(VALVE_selection_button)
        VALVE_layout.addWidget(self.VALVE_label)
        VALVE_layout.addWidget(VALVE_convert_button)
        main_layout.addLayout(VALVE_layout)

        self.LDF_file_path = None
        LDF_selection_button = QPushButton("Select LDF", self)
        LDF_selection_button.setMaximumWidth(150)
        LDF_selection_button.clicked.connect(self.LDF_open_file)
        self.LDF_label = QLabel("No file selected", self)
        self.LDF_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        LDF_convert_button = QPushButton("Run", self)
        LDF_convert_button.setMaximumWidth(100)
        LDF_convert_button.clicked.connect(self.LDF_convert)
        # Layout orizzontale per bottone + etichetta
        LDF_layout = QHBoxLayout()
        LDF_layout.addWidget(LDF_selection_button)
        LDF_layout.addWidget(self.LDF_label)
        LDF_layout.addWidget(LDF_convert_button)
        main_layout.addLayout(LDF_layout)

        self.setLayout(main_layout)

    def LDF_open_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Seleziona TMDS",
                                                   "C:\\Users\\stefano.fortunati\\OneDrive - Industrie Saleri Italo Spa\\Desktop\\TMM_Ceer",
                                                   "LDF (*.ldf);;Tutti i file (*)")
        if file_path:
            self.LDF_label.setText(f"{self.shorten_path(file_path, folders=1)}")
            self.LDF_label.setToolTip(file_path)
            self.LDF_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.LDF_file_path = file_path
        else:
            self.LDF_label.setText("No file selected")

    def LDF_convert(self):
        res = replace_LDF(self.LDF_file_path)
        print("LDF convert completed")

    def CAPL_open_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Seleziona CAPL",
                                                   "C:\\Users\\stefano.fortunati\\OneDrive - Industrie Saleri Italo Spa\\Desktop\\TMM_Ceer",
                                                   "CAPL (*.can);;Tutti i file (*)")
        if file_path:
            self.CAPL_label.setText(f"{self.shorten_path(file_path, folders=1)}")
            self.CAPL_label.setToolTip(file_path)
            self.CAPL_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.CAPL_file_path = file_path
        else:
            self.CAPL_label.setText("No file selected")

    def CAPL_convert(self):
        replace_CAPL(self.CAPL_file_path)
        print("CAPL conversion completed")

    def CAPL_TMM_open_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Seleziona CAPL",
                                                   "C:\\Users\\stefano.fortunati\\OneDrive - Industrie Saleri Italo Spa\\Desktop\\TMM_Ceer",
                                                   "CAPL (*.can);;Tutti i file (*)")
        if file_path:
            self.VALVE_label.setText(f"{file_path}")
            self.VALVE_label.setText(f"{self.shorten_path(file_path, folders=1)}")
            self.VALVE_label.setToolTip(file_path)
            self.VALVE_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.CAPL_TMM_file_path = file_path

        else:
            self.VALVE_label.setText("No file selected")

    def CAPL_TMM_convert(self):
        replace_CAPL_VALVES(self.CAPL_TMM_file_path)
        print("CAPL_TMM_convert completed")

    def shorten_path(self, full_path, folders=2):
        """
        Restituisce gli ultimi 'folders' + nome file.
        Esempio: /a/b/c/d/file.txt -> c/d/file.txt
        """
        p = Path(full_path)
        parts = p.parts  # es: ('C:\\', 'Users', 'Mario', 'Documents', 'file.txt')
        if len(parts) > folders + 1:
            shortened = "...\\" + str(Path(*parts[-(folders + 1):]))
        else:
            shortened = str(p)
        return shortened
