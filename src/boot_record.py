"""
Values to define parameters of the bios.

Most disks have 2 boot records, 1 always at sector 0, the second usually
at sector 6.

Only FAT32/VFat type drives are handled.

File:       boot_record.py
Author:     Lorn B Kerr
Copyright:  (c) 2026 Lorn B Kerr
License:    MIT, see file LICENSE
Version:    0.2
"""

from bpb import boot_param_block

file_name = "boot_record.py"
ile_version = "0.11"
changes = {
    "0.0": "Project directory structure set",
    "0.1": "Read Access to all parameter block values.",
    "0.2": "Change return type of BS_VolId() from hex int to int.",
}


class BootRecord:
    """
    Provide access to the boot record parameter block.

    The required values are read directly from the disk boot sector or
    backup boot sector. In the ideal world these will have the same
    contents.
    """

    def __init__(
        self, drive_image: [], boot_record_sector: int, sector_size: int = 512
    ) -> None:
        """
        Initialize a boot parameter block.

        Paramaters:
            drive_image: byte[] - the drive image to access.
            boot_record_sector (int) - the parameter block, either 0 or 6.
            sector_size (int) - the size of each disk sector, default is
            512 bytes.
        """
        self.bpb = boot_param_block
        """The parameter block definition."""
        self.sector_data: [] = []
        """The sector contents."""
        self.sector_data_start: int = boot_record_sector * sector_size
        """The initial byte address of the sector to be read."""

        try:
            with open(drive_image, "rb") as f:
                f.seek(self.sector_data_start)
                self.sector_data = f.read(512)

        except FileNotFoundError:
            print("Error: The file was not found.")
        except Exception as e:
            print(f"An error occurred: {e}")

    def BS_JmpBoot(self):
        """
        Get the jump to boot code from the boot record block.

        Only handles the case where jump opcode is 0xEB; jmp short.

        Returns:
            (str) the jump to boot code.
        """
        offset = self.bpb["BS_JmpBoot"]["offset"]
        code = self.sector_data[offset : self.bpb["BS_JmpBoot"]["size"]]
        if code[0] == 0xEB and code[2] == 0x90:
            return "JMP Short " + str(hex(code[1])) + ", NOP"
        else:
            print("ERROR: Code " + self.bpb[0] + " is not handled.")

    def BS_OEMName(self):
        """
        Get the OEM Name from the boot record block.

        Returns:
            (str) the OEM Name, with leading and trailing spaces removed.
        """
        return self.str_bios_parameter(
            self.bpb["BS_OEMName"]["offset"],
            self.bpb["BS_OEMName"]["size"],
        )

    def BPB_BytesPerSec(self):
        """
        Get the sector size (bytes per sector) from the boot record block.

        Returns:
            (int) the sector size in bytes.
        """
        return self.int_bios_parameter(
            self.bpb["BPB_BytesPerSec"]["offset"],
            self.bpb["BPB_BytesPerSec"]["size"],
        )

    def BPB_SectorsPerCluster(self):
        """
        Get the number of sectors per cluster from the boot record block.

        Returns:
            (int) the number of sectors in  a cluster.
        """
        return self.int_bios_parameter(
            self.bpb["BPB_SectorsPerCluster"]["offset"],
            self.bpb["BPB_SectorsPerCluster"]["size"],
        )

    def BPB_RsvdSecCount(self):
        """
        Number of reserved sectors. The boot record sectors are included
        in this value.

        Returns:
            (int) the number of reserved sectors.
        """
        return self.int_bios_parameter(
            self.bpb["BPB_RsvdSecCount"]["offset"],
            self.bpb["BPB_RsvdSecCount"]["size"],
        )

    def BPB_numFats(self):
        """
        Number of File Allocation Tables.

        Returns:
            (int) the number of File Allocation Tables.
        """
        return self.int_bios_parameter(
            self.bpb["BPB_numFats"]["offset"],
            self.bpb["BPB_numFats"]["size"],
        )

    def BPB_RootEntCnt(self):
        """
        Maximum number of 32-byte directory entries in the root directory
        for FAT12 and FAT16 volumes. It is typically set to 512 for FAT16,
        but is always 0 on FAT32.

        Returns:
            (int) the number of root directory entries.
        """
        return self.int_bios_parameter(
            self.bpb["BPB_RootEntCnt"]["offset"],
            self.bpb["BPB_RootEntCnt"]["size"],
        )

    def BPB_TotSec16(self):
        """
        The old 16 bit count of the total sectors in the logical volume.
        If set to 0, use BPB_TotSec32 must be used. For FAt12 and Fat15
        volums, use this value, for FAT32 volumns, this value must be 0.

        Returns:
            (int) 16 bit count of the total sectors in the logical volume.
        """
        return self.int_bios_parameter(
            self.bpb["BPB_TotSec16"]["offset"],
            self.bpb["BPB_TotSec16"]["size"],
        )

    def BPB_Media(self):
        """
        This Byte indicates the media descriptor type.

        Returns:
            (int) One of 0xF0, 0xF8, 0xF9, 0xFA, 0xFB, 0xFC, 0xFD, 0xFE,
            or 0xFF. A relic of MS-Dos 1.x and no longer used..
        """
        return self.int_bios_parameter(
            self.bpb["BPB_Media"]["offset"],
            self.bpb["BPB_Media"]["size"],
        )

    def BPB_FATSz16(self):
        """
        The FAT12/FAT16 16-bit count of the number of sectors used by
        one FAT. For FAT32, this field must be 0.

        Returns:
            (int) The FAT12/FAT16 16-bit count of the number of sectors
            used by one FAT.
        """
        return self.int_bios_parameter(
            self.bpb["BPB_FATSz16"]["offset"],
            self.bpb["BPB_FATSz16"]["size"],
        )

    def BPB_SecPerTrk(self):
        """
        Number of sectors per track. Used for 'int 13' io processing only.

        Returns:
            (int) Number of sectors per track.
        """
        return self.int_bios_parameter(
            self.bpb["BPB_SecPerTrk"]["offset"],
            self.bpb["BPB_SecPerTrk"]["size"],
        )

    def BPB_NumHeads(self):
        """
        Number of heads. Used for 'int 13' io processing only.

        Returns:
            (int) Number of heads:
        """
        return self.int_bios_parameter(
            self.bpb["BPB_NumHeads"]["offset"],
            self.bpb["BPB_NumHeads"]["size"],
        )

    def BPB_HiddSec(self):
        """
        Number of hidden sectors. (i.e. the LBA of the beginning of the
        partition.) Used for 'int 13' io processing only.

        Returns:
            (int) Number of hidden sectors:
        """
        return self.int_bios_parameter(
            self.bpb["BPB_HiddSec"]["offset"],
            self.bpb["BPB_HiddSec"]["size"],
        )

    def BPB_TotSec32(self):
        """
        Large sector count. Set if there are more than 65535 sectors in
        the volume, resulting in a value which does not fit in the
         'Number of Sectors' entry at 0x13.

        Returns:
            (int) 32 bit count of the total sectors in the logical
            volume.
        """
        return self.int_bios_parameter(
            self.bpb["BPB_TotSec32"]["offset"],
            self.bpb["BPB_TotSec32"]["size"],
        )

    def BPB_FATSz32(self):
        """
        FAT32 32 bit count of sectors occupied by one FAT. BPB_FATSx16
        must be zero.

        Returns:
            (int) 32 bit count of sectors occupied by one FAT.
        """
        return self.int_bios_parameter(
            self.bpb["BPB_FATSz32"]["offset"],
            self.bpb["BPB_FATSz32"]["size"],
        )
        offset = self.bpb["BPB_FATSz32"]["offset"]
        code = self.sector_data[offset : offset + self.bpb["BPB_FATSz32"]["size"]]
        fat_sz_32 = int.from_bytes(code, "little")
        return fat_sz_32

    def BPB_ExtFlags(self):
        """
        Extended  flags for the file system.
            Bits 0-3: number of active FAT (if bit 7 is 1)
            Bits 4-6: reserved
            Bit 7: one: single active FAT;
               zero: all FATs are updated at runtime
            Bits 8-15: reserved

        Returns:
            (int) 32 bit count of sectors occupied by one FAT.
        """
        return self.int_bios_parameter(
            self.bpb["BPB_ExtFlags"]["offset"],
            self.bpb["BPB_ExtFlags"]["size"],
        )

    def BPB_FSVer(self):
        """
        Filesystem version; high byte is major version, low byte is
        minor version. (Major:Minor)

        Returns:
            (int) Filesystem version
        """
        return self.int_bios_parameter(
            self.bpb["BPB_FSVer"]["offset"],
            self.bpb["BPB_FSVer"]["size"],
        )

    def BPB_RootClus(self):
        """
        First cluster of root directory (usually 2)

        Returns:
            (int) beginning of root directory
        """
        return self.int_bios_parameter(
            self.bpb["BPB_RootClus"]["offset"],
            self.bpb["BPB_RootClus"]["size"],
        )

    def BPB_FSInfo(self):
        """
        First cluster of root directory (usually 2)

        Returns:
            (int) beginning of root directory
        """
        return self.int_bios_parameter(
            self.bpb["BPB_FSInfo"]["offset"],
            self.bpb["BPB_FSInfo"]["size"],
        )

    def BPB_BkBootSec(self):
        """
        Backup boot sector location or 0 or 0xffff if none (usually 6)

        Returns:
            (int) backup boot sector
        """
        return self.int_bios_parameter(
            self.bpb["BPB_BkBootSec"]["offset"],
            self.bpb["BPB_BkBootSec"]["size"],
        )

    def BPB_Reserved(self):
        """
        Reserved, should be all zeros.

        Returns:
            (int) should be zero.
        """
        return self.int_bios_parameter(
            self.bpb["BPB_Reserved"]["offset"],
            self.bpb["BPB_Reserved"]["size"],
        )

    def BS_DrvNum(self):
        """
        Logical Drive Number (for use with INT 13, e.g. 0 or 0x80)

        Returns:
            (int) Drive number
        """
        return self.int_bios_parameter(
            self.bpb["BS_DrvNum"]["offset"],
            self.bpb["BS_DrvNum"]["size"],
        )

    def BS_Reserved1(self):
        """
        Reserved Field

        Returns:
            (int) zero
        """
        return self.int_bios_parameter(
            self.bpb["BS_Reserved1"]["offset"],
            self.bpb["BS_Reserved1"]["size"],
        )

    def BS_BootSig(self):
        """
        Extended signature (0x29) indicates that the three following
        fields (BS_VolID, VolLab, and BS_FilSysType) are present.

        Returns:
            (int) 0x29 indicating the last set of parameters are present.
        """
        return self.int_bios_parameter(
            self.bpb["BS_BootSig"]["offset"],
            self.bpb["BS_BootSig"]["size"],
        )

    def BS_VolID(self):
        return self.int_bios_parameter(
            self.bpb["BS_VolID"]["offset"],
            self.bpb["BS_VolID"]["size"],
        )

    def BS_VolLab(self):
        return self.str_bios_parameter(
            self.bpb["BS_VolLab"]["offset"],
            self.bpb["BS_VolLab"]["size"],
        )

    def BS_FilSysType(self):
        return self.str_bios_parameter(
            self.bpb["BS_FilSysType"]["offset"],
            self.bpb["BS_FilSysType"]["size"],
        )

    def FAT_Sig(self):
        return self.int_bios_parameter(
            self.bpb["FAT_Sig"]["offset"],
            self.bpb["FAT_Sig"]["size"],
        )

    def str_bios_parameter(self, location: int, size: int):
        """
        Get the string parameter from the boot sector bios parameter
        block located in the first set of bytes of the boot sector.

        Parameters:
            location: int - the byte location in the bios parameter block.
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

    def int_bios_parameter(self, location: int, size: int):
        """
        Get the integer parameter from the boot sector bios parameter
        block located in the first set of bytes of the boot sector.

        Parameters:
            location: int - the byte location in the bios parameter block.
            size : int - the number of bytes to retrieve and convert.

        Returns:
            (int) the value of the bios parameter requested.
        """
        byte_code = self.sector_data[location : location + size]
        return int.from_bytes(byte_code, "little")
