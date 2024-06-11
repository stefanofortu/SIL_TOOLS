import logging
import sys
from PySide6.QtWidgets import QApplication

from Classes.MainWindows import MainWindow
from Classes.QTextEditLogger import logging_setup

if __name__ == '__main__':
    logging_setup()

    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        logging.debug('PyInstaller bundle running')
        logging.debug("sys._MEIPASS : %s", sys._MEIPASS)
        print(sys._MEIPASS)
    else:
        logging.debug('running in a normal Python process')

    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())
