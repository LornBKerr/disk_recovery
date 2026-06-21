"""
Define the boot parameter block values.

This defines the names, offset in the block and size for each entry in
the Boot Parameter Block. This is the FAT 32 version, which is also used
for VFat drives.

File:       bpb.py
Author:     Lorn B Kerr
Copyright:  (c) 2026 Lorn B Kerr
License:    MIT, see file LICENSE
Version:    0.1
"""

file_name = "bpb.py"
ile_version = "0.1"
changes = {
    "0.0": "Project directory structure set",
    "0.1": "VFAST / FAT32 boot parameters block defined",
}


boot_param_block = {
    "BS_JmpBoot": {"offset": 0x00, "size": 3, "type": "code"},
    # Jump over BPB to boot code
    # Allowablle values are:
    #   EB XX 90 ==>  JMP SHORT XX NOP.  ( 3 bytes)
    # where XX is the number of bytes to jump over to reach the
    # code section.
    # or
    #   E9 XXXX ==>  JMP XXXX. (3 bytes)
    # #### #### is a 4-byte (32-bit) relative displacement
    #
    # This jumps over the disk format information (the BPB and EBPB).
    # Since the first sector of the disk is loaded into ram at
    # location 0x0000:0x7c00 and executed, without this jump the
    # processor would attempt to execute data that isn't code. Even
    # for non-bootable volumes, code matching this pattern (or using
    # the E9 jump opcode) is required to be present by Windows,
    # Linux and OS X.
    "BS_OEMName": {"offset": 0x03, "size": 8, "type": "str"},
    # OEM Identifier, the version of DOS being used.
    # The official FAT Specification from Microsoft says that this
    # field is really meaningless and is ignored by MS FAT Drivers,
    # however it does recommend the value "MSWIN4.1" as some 3rd
    # party drivers supposedly check it and  expect it to have that
    # value. Older versions of dos also  report MSDOS5.1,
    # linux-formatted floppy will likely to carry  "mkdosfs" here,
    #  and FreeDOS formatted disks have been observed  to have
    # "FRDOS5.1" here. If the string is less than 8 bytes, it is
    # padded with spaces.
    "BPB_BytesPerSec": {"offset": 0x0B, "size": 2, "type": "int"},
    # bytes per sector, little endian
    "BPB_SectorsPerCluster": {"offset": 0x0D, "size": 1, "type": "int"},
    # Sectors per cluster
    "BPB_RsvdSecCount": {"offset": 0x0E, "size": 2, "type": "int"},
    # Number of reserved sectors. The boot record sectors are
    # included in this value.
    "BPB_NumFats": {"offset": 0x10, "size": 1, "type": "int"},
    # Number of File Allocation Tables
    "BPB_RootEntCnt": {"offset": 0x11, "size": 2, "type": "int"},
    # Number of root directory entries
    "BPB_TotSec16": {"offset": 0x13, "size": 2, "type": "int"},
    # The old 16 bit count of the total sectors in the logical
    # volume. If set to 0, use BPB_TotSec32 must be used. For FAt12
    # and Fat15 volums, use this value, for FAT32 volumns, this value
    # must be 0.
    "BPB_Media": {"offset": 0x15, "size": 1, "type": "int"},
    # This Byte indicates the media descriptor type.
    "BPB_FATSz16": {"offset": 0x16, "size": 2, "type": "int"},
    # Number of sectors per FAT. FAT12/FAT16 only.
    #
    "BPB_SecPerTrk": {"offset": 0x18, "size": 2, "type": "int"},
    # Number of sectors per track.
    #
    "BPB_NumHeads": {"offset": 0x1A, "size": 2, "type": "int"},
    # Number of heads or sides on the storage media.
    "BPB_HiddSec": {"offset": 0x1C, "size": 4, "type": "int"},
    # Number of hidden sectors. (i.e. the LBA of the beginning of
    # the partition.)
    "BPB_TotSec32": {"offset": 0x20, "size": 4, "type": "int"},
    # Large sector count. Set if there are more than 65535 sectors
    # in the volume, resulting in a value which does not fit in the
    # Number of Sectors #entry at 0x13
    "BPB_FATSz32": {"offset": 0x24, "size": 4, "type": "int"},
    # FAT32 32 bit count of sectors occupied by one FAT. BPB_FATSz16
    # must be zero.
    "BPB_ExtFlags": {"offset": 0x28, "size": 2, "type": "int"},
    # A 2-byte field in the FAT32 boot sector, used to store extended
    # flags for the file system.
    # - Bits 0–3: Zero-based number of the active FAT, but only if
    #     mirroring is disabled (Bit 7 is 1).
    # - Bits 4–6: Reserved.
    # - Bit 7: Mirroring flag. If 0, all FATs are mirrored at runtime.
    #     If 1, only one FAT (defined in bits 0-3) is active.
    # - Bits 8-15: reserved
    "BPB_FSVer": {"offset": 0x2A, "size": 2, "type": "int"},
    # Filesystem version; high byte is major version, low byte is
    # minor version.
    "BPB_RootClus": {"offset": 0x2C, "size": 4, "type": "int"},
    # First cluster of root directory (usually 2)
    "BPB_FSInfo": {"offset": 48, "size": 2, "type": "int"},
    # Filesystem information sector number in FAT32 reserved area
    # (usually 1)
    "BPB_BkBootSec": {"offset": 50, "size": 2, "type": "int"},
    # Backup boot sector location or 0 or 0xffff if none (usually 6)
    "BPB_Reserved": {"offset": 52, "size": 12, "type": "int"},
    # Reserved, should be all zeros.
    "BS_DrvNum": {"offset": 64, "size": 1, "type": "int"},
    # Logical Drive Number (for use with INT 13, e.g. 0 or 0x80)
    "BS_Reserved1": {"offset": 65, "size": 1, "type": "int"},
    # Reserved - used to be Current Head (used by Windows NT)
    "BS_BootSig": {"offset": 66, "size": 1, "type": "int"},
    # Extended signature (0x29) Indicates that the three following
    # fields are present.
    "BS_VolID": {"offset": 67, "size": 4, "type": "int"},
    # Serial number of partition
    "BS_VolLab": {"offset": 71, "size": 11, "type": "int"},
    # Volume label
    "BS_FilSysType": {"offset": 82, "size": 8, "type": "str"},
    # Filesystem type, should be "FAT32   "
    "FAT_Sig": {"offset": 0x1FE, "size": 2, "type": "int"},
    # FAT signature,  Should always be at bytes 511 and 512 of the
    # fat sector.
}
