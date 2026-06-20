"""
Access the values of the boot paramter blocks.

Provide common functions supporting access to the first 2 sectors of the
disk holding the basic bios paramters along with the 2 backup copies'
sectors 6 and 7.

Only FAT32/VFat type drives are handled.

File:       bios_records.py
Author:     Lorn B Kerr
Copyright:  (c) 2026 Lorn B Kerr
License:    MIT, see file LICENSE
Version:    0.2
"""

from fsi import fsi_block

file_name = "bios_record.py"
ile_version = "0.1"
changes = {
    "0.1": "Refactored to handle common functions.",
}


class BiosRecords:
    """
    Provide access to the Bios and File System Info blocks.

    The required values are read directly from the disk boot sectors or
    backup boot sectors. In the ideal world, these will have the same
    contents.
    """

    def __init__(
        self, drive_image: [], parameter_sector: int, sector_size: int = 512
    ) -> None:
        """
        Initialize a boot parameter block.

        Parameters:
            drive_image: byte[] - the drive image to access.
            parameter_sector (int) - the parameter block, one of 0, 1,
            6, or 7.
            sector_size (int) - the size of each disk sector, default is
            512 bytes.
        """
        self.parameter_sector = parameter_sector
        """The parameter block definition."""
        self.sector_data: [] = []
        """The sector contents."""
        self.sector_data_start: int = parameter_sector * sector_size
        """The initial byte address of the sector to be read."""

        try:
            with open(drive_image, "rb") as f:
                f.seek(self.sector_data_start)
                self.sector_data = f.read(512)

        except FileNotFoundError:
            print("Error: The file was not found.")
        except Exception as e:
            print(f"An error occurred: {e}")
