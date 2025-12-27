**Disk Recovery**

A simple minded program to (_hopefully_) recover some files from a crashed disk.

The backup drive crashed. Time for panic!!!

This happened to me. So, having lots of time (old and retired) and a great reluctance to spend money a anything.

**CAUTION: USE AT YOUR OWN RISK.! NO WARRANTIES. NO GUARANTEES,**

**NO OBLIGATIONS ON MY PART.**

This program reads and writes raw sectors from/to the drive. Admin rights are required.

The result of the crash ended up with a disk that appeared to be total empty. It was visible in the directory listing as an empty drive.

This program is intended to let me go into the raw disk contents and look at the various sectors to see what can be done. The eventual goal is to recover as many of the files and documents as possible. It would be nice if I can repair the disk so it is accessible by mounting it. We'll see what can be done.

The program is written in Python, using version 3.14.2 or later. It is primarily set to work on Linux, in my case Fedora, As I go through the development, I will periodically check its function on Windows 11, but that is not a primary goal.

On starting up the program, we get the opening screen,

<img src="/images/opening-screen.png" alt="Opening Screenshot" style="height: 100px; width:100px;"/>

This lists the available usb drives. Any NVMe system drives, which may show up as usb drives are excluded. Selecting one of the drives will show a number of additional tabs and open the Boot Parameter Table tab.

As I proceed through the program development, I will update this page.
