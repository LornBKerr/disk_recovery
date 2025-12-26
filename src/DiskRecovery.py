"""
Run the 'Disk Revvoery' Application.

Only VFat drives are handled.

File:       DiskRepair.py
Author:     Lorn B Kerr
Copyright:  (c) 2025 Lorn B Kerr
License:    MIT, see file LICENSE
Version:    0.1
"""

import sys

from main_window import MainWindow
from PySide6.QtWidgets import QApplication

file_name = "DiskRecovery.py"
file_version = "0.0"
changes = {"0.0": "Project directory structure set"}

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    # handle the system close button and exit commands
    #    app.aboutToQuit.connect(main_window.exit_app_action)
    sys.exit(app.exec())
