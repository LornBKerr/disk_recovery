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

from parameter_display import ParameterDisplay
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

class BiosParameterDisplay (ParameterDisplay):
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
        super().__init__(parent, drive_image)
        self.headers = [
            ["Offset", "", "Name", "Size", "Boot Sector", "", "Backup Boot Sector", ""],
            ["(dec)", "(hex)", "", "(bytes)", "(dec)", "(hex)", "(dec)", "(hex)"],
        ]
        """The table headers."""
        self.col_widths = [61, 61, 200, 82, 100, 100, 100, 100]
        """The table column widths."""

        boot_sector = 0  # sector 0
        backup_boot_sector = 6  # sector 6

        self.titles = parent.bpb_titles # the form title table.
        self.table = parent.bpb_table   # the form contents table.

        master_boot_record = BootRecord(self.drive_image, boot_sector)
        backup_boot_record = BootRecord(self.drive_image, backup_boot_sector)

        self.initialize_page(parent)

        self.fill_table(master_boot_record, backup_boot_record)
        self.set_column_widths(self.table, self.titles, self.col_widths)

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
        self.table.setColumnCount(len(self.headers[1]))
        self.table.setRowCount(0)
        self.load_parameters(master_boot_record, backup_boot_record)
        self.set_column_widths(self.table, self.titles, self.col_widths)

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
            row = self.table.rowCount()
            self.table.insertRow(row)
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
            self.display_value(mbr_entry(), row, 4)
            bbr_entry = getattr(backup_boot_record, key)
            self.display_value(mbr_entry(), row, 6)

