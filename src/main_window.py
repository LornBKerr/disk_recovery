"""
Sector level read USB connected drives on a Fedora Linux System.

Only VFAT drives are handled.

File:       main.py
Author:     Lorn B Kerr
Copyright:  (c) 2025 Lorn B Kerr
License:    MIT, see file LICENSE
Version:    0.1
"""

from disks_table import DisksTable
from PySide6.QtWidgets import (
    QMainWindow,
)
from ui_main_form import Ui_MainWindow

file_name = "main_window.py"
file_version = "0.1"
changes = {
    "0.0": "Project directory structure set",
    "0.1": "Show 'disk select' tab.",
}


class MainWindow(QMainWindow, Ui_MainWindow):
    """
    This executes the disk recovery process.
    """

    def __init__(self) -> None:
        """Initialize and run the disk repair program."""
        super().__init__()
        self.setupUi(self)
        self.usb_drives = []  # the set of usb drives
        self.setWindowTitle("Disk Recovery")
        self.initialize_tab_widget()
        DisksTable(self.disk_listing, self)

        self.show()

    def initialize_tab_widget(self) -> None:
        """Set the tab names and number of tabs required."""
        self.tab_widget.setTabText(0, "Select Disk")
        self.tab_widget.setTabText(1, "BIOS Parameter Block")
        self.tab_widget.setTabVisible(1, False)
        self.tab_widget.setCurrentIndex(0)

    def usb_button_clicked(self, button_text: str):
        """
        Handle the disk table button click selecting an usb drive.

        Parameters:
            button_text: the name of the clicked button.
        """
        self.tab_widget.setTabVisible(1, True)
        self.tab_widget.setCurrentIndex(1)
