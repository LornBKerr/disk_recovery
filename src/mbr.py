"""
Structures to define parameters of the bios.

Only VFat type drives are handled.

File:       boot_parameters.py
Author:     Lorn B Kerr
Copyright:  (c) 2026 Lorn B Kerr
License:    MIT, see file LICENSE
Version:    0.0
"""

# The boot parameter block definition. Each entry has the form:
#    name: {offset (bytes), size: (bytes), value ( 0 (integers) or "" (strings)}
#    ...
#all entries initialized to 0 or "".
    
boot_param_block = {
    "BS_JmpBoot":
        {"offset": 0x00, "size": 3, "value": ""},   
        # Short jump to boot code

    "BS_OEMName":
        {"offset": 0x03, "size": 8, "value": ""},   
        # OEM Identifier

     "BPB_BytesPerSec":
        {"offset": 0x0B, "size": 2, "value": 0},    
        # bytes per sector, little endian 

    "BPB_SectorPerCluster":
        {"offset": 0x0D, "size": 1, "value": 0},   
         # Sectors per cluster
    
    "BPB_RsvdSecCount":
        {"offset": 0x0E, "size": 2, "value": 0},    
        # Number of reserved sectors.

    "BPB_numFats":
        {"offset": 0x10, "size": 1, "value": 0},    
        # Number of File Allocation Tables

    "BPB_RootEntCnt":
        {"offset": 0x11, "size": 2, "value": 0},    
        # Number of root directory entries 

    "BPB_TotSec16":
        {"offset": 0x13, "size": 2, "value": 0},
        # The total sectors in the logical volume

    "BPB_TotSec16":
        {"offset": 0x15, "size": 1, "value": 0},
        # This Byte indicates the media descriptor type.

    "BPB_Media":
        {"offset": 0x15, "size": 1, "value": 0},
        # This Byte indicates the media descriptor type.

    "BPB_FATSz16":
        {"offset": 0x16, "size": 2, "value": 0},
        # Number of sectors per FAT. FAT12/FAT16 only.

    "BPB_SecPerTrk":
        {"offset": 0x18, "size": 2, "value": 0},
        # Number of sectors per track.

    "BPB_NumHeads":
        {"offset": 0x1A, "size": 2, "value": 0},
        # Number of heads or sides on the storage media.

    "BPB_HiddSec":
        {"offset": 0x1C, "size": 4, "value": 0},
        # Number of hidden sectors. (i.e. the LBA of the beginning of the partition.)

    "BPB_TotSec32":
        {"offset": 0x20, "size": 4, "value": 0},
       # Large sector count. Set if there are more than 65535 sectors

 	"FAT_Sig":
 	    {"offset": 0x1FE, "size": 2, "value": 0xAA55 },	
 	    # Bootable partition signature 0xAA55. 
}


##32 	0x20 	4 	Large sector count. This field is set if there are more than 65535 #sectors in the volume, resulting in a value which does not fit in the Number of Sectors #entry at 0x13. 
##36 	0x024 	1 	Drive number. The value here should be identical to the value returned #by BIOS interrupt 0x13, or passed in the DL register; i.e. 0x00 for a floppy disk and 0x80 #for hard disks. This number is useless because the media is likely to be moved to another #machine and inserted in a drive with a different drive number.
##37 	0x025 	1 	Flags in Windows NT. Reserved otherwise.
##38 	0x026 	1 	Signature (must be 0x28 or 0x29).
##39 	0x027 	4 	VolumeID 'Serial' number. Used for tracking volumes between computers. #You can ignore this if you want.
##43 	0x02B 	11 	Volume label string. This field is padded with spaces.
##54 	0x036 	8 	System identifier string. This field is a string representation of the #FAT file system type. It is padded with spaces. The spec says never to trust the contents #of this string for any use.
##62 	0x03E 	448 	Boot code.
#
##########################
#
##0 	0x00 	3 	The first three bytes EB 3C 90 disassemble to JMP SHORT 3C NOP. (The 3C #value may be different.) The reason for this is to jump over the disk format information #(the BPB and EBPB). Since the first sector of the disk is loaded into ram at location #0x0000:0x7c00 and executed, without this jump, the processor would attempt to execute data #that isn't code. Even for non-bootable volumes, code matching this pattern (or using the #E9 jump opcode) is required to be present by both Windows and OS X. To fulfil this #requirement, an infinite loop can be placed here with the bytes EB FE 90.
##
##3 	0x03 	8 	OEM identifier. The first 8 Bytes (3 - 10) is the version of DOS being #used. The next eight Bytes 29 3A 63 7E 2D 49 48 and 43 read out the name of the version. #The official FAT Specification from Microsoft says that this field is really meaningless #and is ignored by MS FAT Drivers, however it does recommend the value "MSWIN4.1" as some #3rd party drivers supposedly check it and expect it to have that value. Older versions of #dos also report MSDOS5.1, linux-formatted floppy will likely to carry "mkdosfs" here, and #FreeDOS formatted disks have been observed to have "FRDOS5.1" here. If the string is less #than 8 bytes, it is padded with spaces.
##
##11 	0x0B 	2 	The number of Bytes per sector (remember, all numbers are in the #little-endian format).
##
##13 	0x0D 	1 	Number of sectors per cluster.
##
##14 	0x0E 	2 	Number of reserved sectors. The boot record sectors are included in #this value.
##
##16 	0x10 	1 	Number of File Allocation Tables (FAT's) on the storage media. Often #this value is 2.
##
##17 	0x11 	2 	Number of root directory entries (must be set so that the root #directory occupies entire sectors).
##
##19 	0x13 	2 	The total sectors in the logical volume. If this value is 0, it means #there are more than 65535 sectors in the volume, and the actual count is stored in the #Large Sector Count entry at 0x20.
##
##21 	0x15 	1 	This Byte indicates the media descriptor type.
##
##22 	0x16 	2 	Number of sectors per FAT. FAT12/FAT16 only.
##
##24 	0x18 	2 	Number of sectors per track.
##
##26 	0x1A 	2 	Number of heads or sides on the storage media.
##
##28 	0x1C 	4 	Number of hidden sectors. (i.e. the LBA of the beginning of the #partition.)
##
##32 	0x20 	4 	Large sector count. This field is set if there are more than 65535 #sectors in the volume, resulting in a value which does not fit in the Number of Sectors #entry at 0x13. 
##
##
##
##510 	0x1FE 	2 	Bootable partition signature 0xAA55. 
#
