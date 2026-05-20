"""
Setup the drive list tab.

Load the table of disk images on the 'Select Drive Images' tab.
The listing will include all .'drv_img' files found in the drive_images
folder.

File:       drives_table.py
Author:     Lorn B Kerr
Copyright:  (c) 2026 Lorn B Kerr
License:    MIT, see file LICENSE
Version:    0.1
"""

import glob
import os
from datetime import datetime

from format_int_string import IntString
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QMainWindow,
    QRadioButton,
    QTableWidget,
    QTableWidgetItem,
)

file_name = "drives_table.py"
file_version = "0.1"
changes = {
    "0.1": "Define tab 1 of the table",
}


class DrivesTable:
    """Display the disk selection table on the 'Select Disk' Tab."""

    def __init__(self, drive_listing: QTableWidget, parent: QMainWindow) -> None:
        """
        Initialize and run the disk repair program.

        Parameters:
            disks_listing (QTableWidget): The QTableWidget to fill.
            parent (QMainWindow): The tab requiring the table
        """
        super().__init__()
        self.drive_listing = drive_listing
        self.parent = parent
        self.drive_images = []  # the set of drive images.

        self.get_drives()
        self.load_drives()

    def get_drives(self) -> None:
        """
        Get the available drive images from the system.

        Drive images are expected to be in folder '../drive_images' and
        have a suffix of '.drv_img'. Name, file date, and file size are
        collected for each file found. Format of date and time may vary.

        Example:
            ["sda.drv_img", "3/10/2026, 1:12:38 PM", "62.0 GB"]
        """

        def sortFunc(a):
            return a[0]

        self.drive_images = []
        for file in glob.glob("**/drive_images/*.drv_img", recursive=True):
            filesize = IntString.format(os.path.getsize(file), True, 2)
            dt_object = datetime.fromtimestamp(os.path.getmtime(file))
            # Format as "YYYY-MM-DD HH:MM:SS"
            formatted_time = dt_object.strftime("%Y-%m-%d %H:%M:%S")
            self.drive_images.append([file, filesize, formatted_time])
        self.drive_images.sort(key=sortFunc)
        self.drive_images.insert(0, ["Drive Images", "Size", "Time"])

    def load_drives(self) -> None:
        """Display the available usb drives"""
        row = 0
        self.setup_table()

        # set the title row
        self.drive_listing.insertRow(row)
        for col in range(0, 2):
            item = QTableWidgetItem(self.drive_images[row][col])
            item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.drive_listing.setItem(row, col, item)

        # leave last title item left justified
        item = QTableWidgetItem(self.drive_images[row][col + 1])
        self.drive_listing.setItem(row, col + 1, item)

        # show the drive images
        if len(self.drive_images) > 1:
            for row in range(1, len(self.drive_images)):
                self.drive_listing.insertRow(row)
                button = self.get_radio_button(self.drive_images[row][0])
                self.drive_listing.setCellWidget(row, 0, button)
                self.drive_listing.setItem(
                    row, 1, QTableWidgetItem(self.drive_images[row][1])
                )
                self.drive_listing.setItem(
                    row, 2, QTableWidgetItem(self.drive_images[row][2])
                )

            # resize the table to the entry sizes plus spacing.
            self.drive_listing.resizeColumnsToContents()
            self.drive_listing.setColumnWidth(0, self.drive_listing.columnWidth(0) + 40)
            self.drive_listing.setColumnWidth(1, self.drive_listing.columnWidth(1) + 30)
            self.drive_listing.setColumnWidth(2, self.drive_listing.columnWidth(2) + 20)
        else:
            self.drive_listing.insertRow(1)
            item = QTableWidgetItem("No Drives were found")
            self.drive_listing.setItem(1, 0, QTableWidgetItem(item))
            self.drive_listing.setSpan(1, 0, 1, 3)

    def setup_table(self) -> None:
        """Set the bacic table layout; rows, columns appearance, etc."""
        self.drive_listing.setRowCount(0)
        self.drive_listing.setColumnCount(len(self.drive_images[0]))
        self.drive_listing.horizontalHeader().setVisible(False)
        self.drive_listing.verticalHeader().setVisible(False)
        self.drive_listing.setShowGrid(False)
        self.drive_listing.setStyleSheet(
            "QTableWidget { background-color: transparent; }"
        )

    def get_radio_button(self, text, truncate=False) -> QRadioButton:
        """
        Define a radio button with the given text and action connected.

        If truncate is True, delete the last character of the text. This
        will be a partition numbe of the drive being shown. When working
        with the boot sectors, we are working with the basic disk, not
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
        radio_button.clicked.connect(lambda: self.parent.drive_button_clicked(text))
        return radio_button
