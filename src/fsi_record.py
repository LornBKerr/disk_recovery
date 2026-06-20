"""
Access the values of the File System Info record.

Most disks have 2 records, 1 always at sector 1, the second usually
at sector 7.

Only FAT32/VFat type drives are handled.

File:       fsi_record.py
Author:     Lorn B Kerr
Copyright:  (c) 2026 Lorn B Kerr
License:    MIT, see file LICENSE
Version:    0.1
"""

from bios_records import BiosRecords
from fsi import fsi_block

file_name = "fsi_record.py"
ile_version = "0.1"
changes = {
    "0.0": "Project directory structure set",
    "0.1": "Read Access to all block values.",
}


class FSIRecord (BiosRecords):
    """
    Provide access to the File System Info  block.

    The required values are read directly from the disk boot sector or
    backup boot sector. In the ideal world these will have the same
    contents.
    """
    def __init__(
        self, drive_image: [], fsi_record_sector: int, sector_size: int = 512
    ) -> None:
        """
        Initialize a fsi parameter block.

        Paramaters:
            drive_image: byte[] - the drive image to access.
            fsi_record_sector (int) - the file system info block, either 1 or 7.
            sector_size (int) - the size of each disk sector, default is
            512 bytes.
        """
        self.fsi = fsi_block
        """The parameter block definition."""
        super().__init__(drive_image, fsi_record_sector, sector_size)

    def FSI_LeadSig(self):
        """
        Get the lead signature of FSI Block

        Should return the fixed value of 0x41615252.

        Returns:
            (int) the lead signature of the FSI block.
        """
        return self.int_parameter(
            self.fsi["FSI_LeadSig"]["offset"],
            self.fsi["FSI_LeadSig"]["size"],
        )

    def FSI_Reserved1(self):
        """
        Get the sector size (bytes per sector) from the boot record block.

        Returns:
            (int) the sector size in bytes.
        """
        return self.int_parameter(
            self.fsi["FSI_Reserved1"]["offset"],
            self.fsi["FSI_Reserved1"]["size"],
        )

    def FSI_StructSig(self):
        """
        Get the OEM Name from the boot record block.

        Returns:
            (str) the OEM Name, with leading and trailing spaces removed.
        """
        return self.int_parameter(
            self.fsi["FSI_StructSig"]["offset"],
            self.fsi["FSI_StructSig"]["size"],
        )


    def FSI_Free_Count(self):
        """
        Get the number of sectors per cluster from the boot record block.

        Returns:
            (int) the number of sectors in  a cluster.
        """
        return self.int_parameter(
            self.fsi["FSI_Free_Count"]["offset"],
            self.fsi["FSI_Free_Count"]["size"],
        )

    def FSI_Nxt_Free(self):
        """
        Number of reserved sectors. The boot record sectors are included
        in this value.

        Returns:
            (int) the number of reserved sectors.
        """
        return self.int_parameter(
            self.fsi["FSI_Nxt_Free"]["offset"],
            self.fsi["FSI_Nxt_Free"]["size"],
        )

    def FSI_Reserved2(self):
        """
        Number of File Allocation Tables.

        Returns:
            (int) the number of File Allocation Tables.
        """
        return self.int_parameter(
            self.fsi["FSI_Reserved2"]["offset"],
            self.fsi["FSI_Reserved2"]["size"],
        )

    def FSI_Trail_Sig(self):
        """
        Maximum number of 32-byte directory entries in the root directory
        for FAT12 and FAT16 volumes. It is typically set to 512 for FAT16,
        but is always 0 on FAT32.

        Returns:
            (int) the number of root directory entries.
        """
        return self.int_parameter(
            self.fsi["FSI_Trail_Sig"]["offset"],
            self.fsi["FSI_Trail_Sig"]["size"],
        )

    def str_parameter(self, location: int, size: int):
        """
        Get the string parameter from the boot sector bios parameter
        block located in the first set of bytes of the boot sector.

        Parameters:
            location: int - the byte location in the fsi block.
            size : int - the number of bytes to retrieve and convert.

        Returns:
            (str) the value of the bios parameter requested.
        """
        str_parameter = ""
        i = 0
        for i in range(location, location + size):
            str_parameter += chr(self.sector_data[i])

        # remove leading and trailing whitespace and return name
        return str_parameter.strip()

    def int_parameter(self, location: int, size: int):
        """
        Get the integer parameter from the FSI Block.

        Parameters:
            location: int - the byte location in the fsi block.
            size : int - the number of bytes to retrieve and convert.

        Returns:
            (int) the value of the parameter requested.
        """
        byte_code = self.sector_data[location : location + size]
        return int.from_bytes(byte_code, "little")
