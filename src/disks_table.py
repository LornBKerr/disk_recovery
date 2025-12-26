"""
Setup the disk list tab.

Load the table  of disk drives on the 'Select Disk' tab. All usb
connected disks are included.

File:       disks_table.py
Author:     Lorn B Kerr
Copyright:  (c) 2025 Lorn B Kerr
License:    MIT, see file LICENSE
Version:    0.1
"""

import psutil
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QMainWindow,
    QRadioButton,
    QTableWidget,
    QTableWidgetItem,
)

file_name = "disks_table.py"
file_version = "0.1"
changes = {
    "0.1": "Define tab 1 of the table",
}


class DisksTable:
    """Display the disk selection table on the 'Select Disk' Tab."""

    def __init__(self, disk_listing: QTableWidget, parent_window: QMainWindow) -> None:
        """
        Initialize and run the disk repair program.

        Parameters:
            disks_listing (QTableWidget): The QTableWidget to fill.
            parent_window (QMainWindow): The tab requiring the table
        """
        super().__init__()
        self.disk_listing = disk_listing
        self.parent_window = parent_window
        self.usb_drives = []  # the set of usb drives

        self.get_drives()
        self.load_usb_drives()

    def get_drives(self) -> None:
        """
        Get the available disks from the system.

        This scans all available USB disk partitions and adds the
        partition information to the usb drive list. The partition
         information saved includes disk name, disk mount point, and
         disk format type.

         Example for a usb  drive:
            ("/dev/sdc1", "/run/media/<user>/DD8C-10FF", "vfat")
        """
        self.usb_drives.insert(0, ["USB Drives", "Location", "Type"])
        disks = psutil.disk_partitions(False)
        for i in range(len(disks)):
            disk = disks[i]
            if disk[0].startswith("/dev/sd"):
                self.usb_drives.append(disk[0:3:1])

    def load_usb_drives(self) -> None:
        """Display the available usb drives"""
        row = 0
        self.setup_table()

        # set the title row
        self.disk_listing.insertRow(row)
        for col in range(0, 2):
            item = QTableWidgetItem(self.usb_drives[row][col])
            item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.disk_listing.setItem(row, col, item)

        # leave last title item left justified
        item = QTableWidgetItem(self.usb_drives[row][col + 1])
        self.disk_listing.setItem(row, col + 1, item)

        # show the usb drives
        for row in range(1, len(self.usb_drives)):
            self.disk_listing.insertRow(row)
            button = self.get_radio_button(self.usb_drives[row][0], True)
            self.disk_listing.setCellWidget(row, 0, button)
            self.disk_listing.setItem(row, 1, QTableWidgetItem(self.usb_drives[row][1]))
            self.disk_listing.setItem(row, 2, QTableWidgetItem(self.usb_drives[row][2]))

        # resize the table to the entry sizes plus spacing.
        self.disk_listing.resizeColumnsToContents()
        self.disk_listing.setColumnWidth(0, self.disk_listing.columnWidth(0) + 40)
        self.disk_listing.setColumnWidth(1, self.disk_listing.columnWidth(1) + 30)
        self.disk_listing.setColumnWidth(2, self.disk_listing.columnWidth(2) + 20)

    def setup_table(self) -> None:
        """Set the bacic table layout; rows, columns appearance, etc."""
        self.disk_listing.setRowCount(0)
        self.disk_listing.setColumnCount(len(self.usb_drives[0]))
        self.disk_listing.horizontalHeader().setVisible(False)
        self.disk_listing.verticalHeader().setVisible(False)
        self.disk_listing.setShowGrid(False)
        self.disk_listing.setStyleSheet(
            "QTableWidget { background-color: transparent; }"
        )

    def get_radio_button(self, text, truncate=False) -> QRadioButton:
        """
        Define a radio button with the given text and action connected.

        If truncate is True, delete the last character of the text. This
        will be a partition numbe of the drive being shown. When working
        with the boot sectorrs , we are working with the basic disk, not
        a specific partition.

        The action for the radio button click is in the main window.

        Parameters:
            text (str): the text for the radio button
            truncate (bool): delete the last character of the text string.

        Returns:
            QRadioButton: The labeled radio button.
        """
        if truncate:
            text = text[: len(text) - 1]
        radio_button = QRadioButton(text)
        radio_button.clicked.connect(
            lambda: self.parent_window.action_button_click(text)
        )
        return radio_button
