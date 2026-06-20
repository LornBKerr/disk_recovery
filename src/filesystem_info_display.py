"""
Display the FileSystem information

The parameters are displayed for both Sector 2 (the boot sector area) and
sector 7 (backup boot sector area). Differences between the two sets of
paramters are highlighted in red.

Only FAT32/VFat type drives are handled.

File:       filesystem_info_display.py
Author:     Lorn B Kerr
Copyright:  (c) 2026 Lorn B Kerr
License:    MIT, see file LICENSE
Version:    0.1
"""

from parameter_display import ParameterDisplay
from fsi_record import FSIRecord
from PySide6.QtWidgets import QMainWindow, QTableWidgetItem
from PySide6.QtCore import Qt

file_name = "filesystem_info_display.py"
file_version = "0.1"
changes = {
    "0.1": "initial table created.",
}

class FileSystemInfoDisplay (ParameterDisplay):
    """
    Display the file system info.

    The filesystem_info_display will display the stored values from the
    boot sector (sector 1) and backup boot sector (sector 7) with
    differences highlighted.
    """

    def __init__(self, parent: QMainWindow, drive_image: []) -> None:
        """
        Read the drive and display the file system parameters.

        Parameters:
            parent (QMainWindow): The owning window
            drive_image (byte[]): Tthe byte array image of the drive.
        """
        super().__init__(parent, drive_image)
        self.headers = [
            ["Offset", "", "Name", "Size", "FSI Sector", "", "Backup FSI Sector", ""],
            ["(dec)",  "(hex)", "", "(bytes)", "(dec)", "(hex)", "(dec)", "(hex)"],
        ]
        """The table headers."""
        self.col_widths = [62, 62, 200, 62, 108, 108, 108, 108]
        """The table column widths."""
        fsi_sector = 1          # sector 1
        backup_fsi_sector = 7   # sector 7

        self.titles = parent.fsi_titles  # the form title table.
        self.table = parent.fsi_table  # the form contents table.

        master_fsi_record = FSIRecord(self.drive_image, fsi_sector)
        backup_fsi_record = FSIRecord(self.drive_image, backup_fsi_sector)

        self.initialize_page(parent)

        self.fill_table(master_fsi_record, backup_fsi_record)
        self.set_column_widths(self.table, self.titles, self.col_widths)

    def fill_table(self, master_fsi_record, backup_fsi_record) -> None:
        """
        Walk down the BootParametersBlock (fsi_???).

        The values will be extracted from both the Boot Sector and
        Backup Boot Sector and displayed, If a pair of entries differ,
        the row will be highted in red.

        Parameters:
            master_fsi_record (dict{str, dict{str, int|str}}: Boot Parameter block
            backup_fsi_record (dict{str, dict{str, int|str}}: Boot Parameter block
        """
        self.table.setColumnCount(len(self.headers[1]))
        self.table.setRowCount(0)
        self.load_parameters(master_fsi_record, backup_fsi_record)
        self.set_column_widths(self.table, self.titles, self.col_widths)

    def load_parameters(
        self, master_fsi_record: BootRecord, backup_fsi_record: BootRecord
    ) -> None:
        """
        Load the values of the FAT block into the table.

        Parameters:
            master_fsi_record (BootRecord): The master Boot Parameter block
            backup_fsi_record (BootRecord): The backup Boot Parameter block
        """
        for key in master_fsi_record.fsi.keys():
            row = self.table.rowCount()
            self.table.insertRow(row)
            self.table_item(
                str(master_fsi_record.fsi[key]["offset"]),
                row,
                0,
                Qt.AlignmentFlag.AlignCenter,
            )
            self.table_item(
                str(hex(master_fsi_record.fsi[key]["offset"])),
                row,
                1,
                Qt.AlignmentFlag.AlignCenter,
            )
            self.table_item(key, row, 2, Qt.AlignmentFlag.AlignLeft)
            self.table_item(
                str(master_fsi_record.fsi[key]["size"]),
                row,
                3,
                Qt.AlignmentFlag.AlignCenter,
            )
            mbr_entry = getattr(master_fsi_record, key)
            self.display_value(mbr_entry(), row, 4)
            bbr_entry = getattr(backup_fsi_record, key)
            self.display_value(mbr_entry(), row, 6)

