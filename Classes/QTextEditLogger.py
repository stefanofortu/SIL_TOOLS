import logging
import sys
from PySide6.QtWidgets import QPlainTextEdit

def logging_setup():
    rootLogger = logging.getLogger('')
    rootLogger.handlers.clear()

    rootLogger.setLevel(level=logging.DEBUG)

    logFormatter = logging.Formatter("[%(asctime)s] %(levelname).5s: %(message)s", datefmt='%d/%m/%y %H:%M')

    fileHandler = logging.FileHandler("output.log")
    fileHandler.setFormatter(logFormatter)
    fileHandler.setLevel(level=logging.DEBUG)

    consoleHandler = logging.StreamHandler(sys.stdout)
    consoleHandler.setFormatter(logFormatter)
    consoleHandler.setLevel(level=logging.DEBUG)

    rootLogger.handlers.clear()
    rootLogger.addHandler(fileHandler)
    rootLogger.addHandler(consoleHandler)

class QTextEditLogger(logging.Handler):
    def __init__(self, parent):
        super().__init__()
        self.widget = QPlainTextEdit(parent)
        self.widget.setReadOnly(True)
        self.setFormatter(logging.Formatter("[%(asctime)s] %(levelname).5s: %(message)s", datefmt='%d/%m/%y %H:%M'))
        logging.getLogger().setLevel(logging.DEBUG)

    def emit(self, record):
        msg = self.format(record)
        self.widget.appendPlainText(msg)
