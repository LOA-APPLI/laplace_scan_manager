# libraries
import sys
import logging

from PyQt6.QtWidgets import QApplication
from laplace_log import LoggerLHC, log
from laplace_server.protocol import LOGGER_NAME

# Initialize the logger
LoggerLHC("laplace.scan", file_level="debug", console_level="info")
log.info("Starting loopWindow...")

logging.getLogger(LOGGER_NAME).setLevel(logging.INFO)
logging.getLogger("matplotlib").setLevel(logging.WARNING)



import os 
print(os.getcwd())
# project
from .interface import ScanWindow

if __name__ == "__main__":

    print(os.getcwd())
    app = QApplication(sys.argv) # create the app
    window = ScanWindow()         # create the window
    window.show()                # display the window
    
    log.info("Window opened.")

    # end the process
    exit_code = app.exec()
    log.info(f"Application is exiting with code {exit_code}.")
    sys.exit(exit_code)