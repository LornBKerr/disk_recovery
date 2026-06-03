"""
Display the Boot Paramaters.

The parameters are displayed for both Sector 0 (the boot sector) and
sector 6 (backup boot sector). Differences between the two sets of
paramters are highlighted in red.

Only FAT32/VFat type drives are handled.

File:       boot_parameters_table.py
Author:     Lorn B Kerr
Copyright:  (c) 2026 Lorn B Kerr
License:    MIT, see file LICENSE
Version:    0.2
"""

from boot_record import BootRecord
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QMainWindow, QTableWidgetItem

file_name = "boot_parameters_display.py"
file_version = "0.2"
changes = {
    "0.0": "Project directory structure set",
    "0.1": "initial table created.",
    "0.2": "Table filled in.",
}


class BiosParameterDisplay:
    """
    Display the boot parameters.

    The boot_parameters_display will display the stored values from the
    boot sector (sector 0) and backup boot sector (sector 6) with
    differences highlighted.
    """

    def __init__(self, parent: QMainWindow, drive_image: []) -> None:
        """
        Read the drive and display the bios paramters.

        Parameters:
            parent (QMainWindow): The owning window
            drive_image (byte[]): Tthe byte array image of the drive.
        """
        super().__init__()
        self.headers = [
            ["Offset", "", "Name", "Size", "Boot Sector", "", "Backup Boot Sector", ""],
            ["(dec)", "(hex)", "", "(bytes)", "(dec)", "(hex)", "(dec)", "(hex)"],
        ]
        """The table headers."""
        self.col_widths = [61, 61, 200, 82, 100, 100, 100, 100]
        """The table column widths."""

        self.parent = parent  # the owning Main Window
        self.drive_image = drive_image  # contents of the drive to display.
        self.bpb_titles = parent.bpb_titles  # the form title table.
        self.bpb_table = parent.bpb_table  # the form contents table.
        self.initialize_page(parent)

        boot_sector = 0  # sector 0
        backup_boot_sector = 6  # sector 6

        master_boot_record = BootRecord(self.drive_image, boot_sector)
        backup_boot_record = BootRecord(self.drive_image, backup_boot_sector)
        self.fill_table(master_boot_record, backup_boot_record)
        self.set_column_widths()

    def fill_table(self, master_boot_record, backup_boot_record) -> None:
        """
        Walk down the BootParametersBlock (BPB_???).

        The values will be extracted from both the Boot Sector and
        Backup Boot Sector and displayed, If a pair of entries differ,
        the row will be highted in red.

        Parameters:
            master_boot_record (dict{str, dict{str, int|str}}: Boot Parameter block
            backup_boot_record (dict{str, dict{str, int|str}}: Boot Parameter block
        """
        self.bpb_table.setColumnCount(len(self.headers[1]))
        self.bpb_table.setRowCount(0)
        self.load_parameters(master_boot_record, backup_boot_record)
        self.set_column_widths()

    def load_parameters(
        self, master_boot_record: BootRecord, backup_boot_record: BootRecord
    ) -> None:
        """
        Load the values of the FAT block into the table.

        Parameters:
            master_boot_record (BootRecord): The master Boot Parameter block
            backup_boot_record (BootRecord): The backup Boot Parameter block
        """
        for key in master_boot_record.bpb.keys():
            row = self.bpb_table.rowCount()
            self.bpb_table.insertRow(row)
            self.table_item(
                str(master_boot_record.bpb[key]["offset"]),
                row,
                0,
                Qt.AlignmentFlag.AlignCenter,
            )
            self.table_item(
                str(hex(master_boot_record.bpb[key]["offset"])),
                row,
                1,
                Qt.AlignmentFlag.AlignCenter,
            )
            self.table_item(key, row, 2, Qt.AlignmentFlag.AlignLeft)
            self.table_item(
                str(master_boot_record.bpb[key]["size"]),
                row,
                3,
                Qt.AlignmentFlag.AlignCenter,
            )
            mbr_entry = getattr(master_boot_record, key)
            self.display_bs_value(mbr_entry(), row, 4)
            bbr_entry = getattr(backup_boot_record, key)
            self.display_bs_value(mbr_entry(), row, 6)

    def display_bs_value(self, value: [], row: int, col: int) -> None:
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
            self.bpb_table.setSpan(row, col, 1, 2)
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
        self.bpb_table.setItem(row, col, item)

    def initialize_page(self, parent):
        """Define the basic parameters of the bp_table; column count, etc."""
        self.set_header_table()
        self.setup_bpb_table()

    def set_header_table(self) -> None:
        """Set the header contents."""
        self.bpb_titles.setRowCount(2)
        self.bpb_titles.setColumnCount(len(self.headers[1]))
        self.bpb_titles.horizontalHeader().setVisible(False)
        self.bpb_titles.verticalHeader().setVisible(False)
        last_col = 0
        for col in range(len(self.headers[0])):
            item = QTableWidgetItem(self.headers[0][col])
            item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.bpb_titles.setItem(0, col, item)

        for col in range(len(self.headers[1])):
            item = QTableWidgetItem(self.headers[1][col])
            item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.bpb_titles.setItem(1, col, item)
        height = (self.bpb_titles.rowHeight(0) * 2) + 2
        self.bpb_titles.setMaximumHeight(height)
        self.bpb_titles.setSpan(0, 0, 1, 2)  # offset title
        self.bpb_titles.setSpan(0, 4, 1, 2)  # boot sector title
        self.bpb_titles.setSpan(0, 6, 1, 2)  # backup boot sector title

    def setup_bpb_table(self) -> None:
        """Set the location and hide the headers"""
        self.bpb_table.setRowCount(0)
        self.bpb_table.horizontalHeader().setVisible(False)
        self.bpb_table.verticalHeader().setVisible(False)
        loc_x = self.bpb_table.x()
        loc_y = self.bpb_titles.y() + self.bpb_titles.height()
        width = self.bpb_titles.width()
        height = 500
        self.bpb_table.setGeometry(loc_x, loc_y, width, height)

    def set_column_widths(self) -> None:
        """
        Set the column widths for header table and data table.
        """
        self.bpb_table.resizeColumnsToContents()
        for column in range(0, self.bpb_table.columnCount()):
            self.bpb_table.setColumnWidth(column, self.col_widths[column])
            self.bpb_titles.setColumnWidth(column, self.col_widths[column])
