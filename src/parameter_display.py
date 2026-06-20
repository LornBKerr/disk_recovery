"""
Parent class for various display classes

Handle the common functions to diplay tab pages for the app.

Only FAT32/VFat type drives are handled.

File:       display.py
Author:     Lorn B Kerr
Copyright:  (c) 2026 Lorn B Kerr
License:    MIT, see file LICENSE
Version:    0.1
"""

from boot_record import BootRecord
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QMainWindow, QTableWidgetItem

file_name = "boot_parameters_display.py"
file_version = "0.1"
changes = {
    "0.1": "initial table created.",
}


class ParameterDisplay:
    """
    Display the boot parameters.

    The boot_parameters_display will display the stored values from the
    boot sector (sector 0) and backup boot sector (sector 6) with
    differences highlighted.
    """
    def __init__(self, parent: QMainWindow, drive_image: []) -> None:
        self.parent = parent  # the owning Main Window
        self.drive_image = drive_image  # contents of the drive to display.
        
        self.titles = None  # the form title table.
        self.table = None   # the form contents table.
        self.headers = []
        self.col_widths = []

    def initialize_page(self, parent):
        """Define the basic parameters of the bp_table; column count, etc."""
        self.set_header_table()
        self.setup_table()

    def set_header_table(self) -> None:
        """Set the header contents."""
        self.titles.setRowCount(2)
        self.titles.setColumnCount(len(self.headers[1]))
        self.titles.horizontalHeader().setVisible(False)
        self.titles.verticalHeader().setVisible(False)

        for col in range(len(self.headers[0])):
            item = QTableWidgetItem(self.headers[0][col])
            item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.titles.setItem(0, col, item)

        for col in range(len(self.headers[1])):
            item = QTableWidgetItem(self.headers[1][col])
            item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.titles.setItem(1, col, item)
        height = (self.titles.rowHeight(0) * 2) + 2
        self.titles.setMaximumHeight(height)
        self.titles.setSpan(0, 0, 1, 2)  # offset
        self.titles.setSpan(0, 4, 1, 2)  # sector title
        self.titles.setSpan(0, 6, 1, 2)  # backup sector title

    def display_value(self, value: [], row: int, col: int) -> None:
        """
        Display the boot sector entry value at the row given.

        If the value is numeric, display both dec and hex values. If the
        value is not numeric, display the text value, If the value is a
        jump code, display the instruction.

        Parmeters:
            value (Any); the boot sector value as byte array
            row (int) - the row to display the values.
            col (int) - the column to display the value (either 4 or 6).
        """
        self.table_item(str(value), row, col, Qt.AlignmentFlag.AlignCenter)

        if type(value) is str:  # spread across two columns
            self.table.setSpan(row, col, 1, 2)
        else:
            self.table_item(str(hex(value)), row, col + 1, Qt.AlignmentFlag.AlignCenter)

    def table_item(
        self, item: any, row: int, col: int, alignment: Qt.AlignmentFlag
    ) -> None:
        """
        Add an entry to the table.

        Parameters:
            item (any) - The value to be added to the table.
            row (int) - the row to place the the item.
            col (int) - the column to place the item.
            alignment (Qt.AlignmentFlag) - the alignment of the item.
        """
        item = QTableWidgetItem(item)
        item.setTextAlignment(alignment | Qt.AlignmentFlag.AlignVCenter)
        self.table.setItem(row, col, item)

    def setup_table(self) -> None:
        """Set the location and hide the headers"""
        self.table.setRowCount(0)
        self.table.horizontalHeader().setVisible(False)
        self.table.verticalHeader().setVisible(False)
        loc_x = self.table.x()
        loc_y = self.titles.y() + self.titles.height()
        width = self.titles.width()
        height = 500
        self.table.setGeometry(loc_x, loc_y, width, height)

    def set_column_widths(self, table: QTableWidget, titles:QTableWidget, col_widths) -> None:
        """
        Set the column widths for header table and data table.
        """
        table.resizeColumnsToContents()
        for column in range(0, titles.columnCount()):
            table.setColumnWidth(column, col_widths[column])
            titles.setColumnWidth(column, self.col_widths[column])
