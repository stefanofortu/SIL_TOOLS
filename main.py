import logging
from Classes.LoggingStream import setup_logger

import os
import sys
from PySide6.QtWidgets import QApplication
import PySide6
from Classes.MainWindows import MainWindow
import qdarkstyle
#from Arduino.python.MainWindows_temp import MainWindow
from Classes.QTextEditLogger import logging_setup
logger = logging.getLogger("SIL_TOOLS")

if __name__ == '__main__':
    setup_logger()

    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        logger.debug('PyInstaller bundle running')
        logger.debug("sys._MEIPASS : %s", sys._MEIPASS)
        print(sys._MEIPASS)
    else:
        logger.debug('running in a normal Python process')
    print(PySide6.__version__)

    #sys.argv += ['-platform', 'windows:darkmode=1']
    app = QApplication(sys.argv)

    ## use default style of the pyside
    #app.setStyle("Fusion")
    ### style the application; use qdarkstyle or QSS
    use_qss_stylesheets = False
    if use_qss_stylesheets:
        qss_path = "themes/ConsoleStyle.qss"
        if os.path.exists(qss_path):
            with open(qss_path, "r") as f:
                app.setStyleSheet(f.read())
    else:
        # use qdarkstyle library
        app.setStyleSheet(qdarkstyle.load_stylesheet(qt_api='pyside6'))

    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())