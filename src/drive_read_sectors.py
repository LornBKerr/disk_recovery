"""
Read one or more raw sectors from to a data drive.

This is for Linux systems. Admin rights are required.

File:       drive_read.py
Author:     Lorn B Kerr
Copyright:  (c) 2025 Lorn B Kerr
License:    MIT, see file LICENSE
Version:    0.1
"""

import os
import sys

sector: list = []

def read_sector_unix(drive_path, start_sector, number_sectors):
    """
    Reads 'number_sectors' starting at 'start_sector' from a data drive.
    
    Parameters:
        drive_path (str) - The unix path to the drive, generally in the
            form '/dev/sd?#/' where the "?" is the drive a letter 
            starting with 'a' and the # is an optional number starting 
            with 0. If the drive number is omitted, the boot sector area
            is accessable.
    """
    sector_size = 512
    sector_data = []
    try:
        with open(drive_path, "rb") as f:
            f.seek(start_sector * sector_size)
            sector_data = f.read(number_sectors * sector_size)
            return sector_data

    except PermissionError:
        print("Permission denied. Run as root/administrator.")
        return None

    except FileNotFoundError:
        print(f"Disk path not found: {drive_path}")
        return None

    except Exception as e:
        print(f"An error occurred: {e}")
        return None

sector = read_sector_unix(sys.argv[1], int(sys.argv[2]), int(sys.argv[3]))
print(sector)

