"""
Define the filesystem info block values.

This defines the names, offset in the block and size for each entry in
the FileSystem info Block. This is the FAT 32 version, which is also used
for VFat drives.

File:       fsi.py
Author:     Lorn B Kerr
Copyright:  (c) 2026 Lorn B Kerr
License:    MIT, see file LICENSE
Version:    0.1
"""

file_name = "fsi.py"
ile_version = "0.1"
changes = {
    "0.0": "Project directory structure set",
    "0.1": "VFAT / FAT32 filesystem info block defined",
}


fsi_block = {
    "FSI_LeadSig": {"offset": 0, "size": 4, "type": "int"},
    # Value = 0x41615252. Used to validate the beginning of the FSI block.

    "FSI_Reserved1": {"offset": 4, "size": 480, "type": "int"},
    # Reserved; required to be set to all 0's.

    "FSI_StructSig": {"offset": 484, "size": 4, "type": "int"},
    # Value = 0x61417272. Additional signature validating integrity of
    # FileSystem info block.

    "FSI_Free_Count": {"offset": 488, "size": 4, "type": "int"},
    # The last known free cluster count on the volumn.
    # Value 0xFFFFFFFF indicates free count not known.

    "FSI_Nxt_Free": {"offset": 492, "size": 4, "type": "int"},
    # Hint for cluster number to start looking for the next free cluster. 
    # If 0xFFFFFFFF, there is no hint, start at cluster 2.

    "FSI_Reserved2": {"offset": 496, "size": 12, "type": "int"},
    # Reserved; required to be set to all 0's.

    "FSI_Trail_Sig": {"offset": 508, "size": 4, "type": "int"},
    # Value = 0xAA550000. Used to validate the ending of the FSI block.
}
