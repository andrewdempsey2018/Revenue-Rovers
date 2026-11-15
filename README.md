# Revenue Rovers

Demonstration of electronics and software development for students

# Link to Repo

Scan this QR code to access the code!

![alt text](image.png)

# Pico microcontroller boards
Raspberry Pi Pico is a development board that uses Raspberry Pi microcontrollers (RP2040 or RP2350). A Raspberry Pi Pico is programmed using MicroPython, C, or C++ and, unlike other Raspberry Pi devices, doesn’t run Linux or support removable storage. Instead, Raspberry Pi Pico is programmed by flashing binaries to the on-board flash memory.

# Raspberry Pi Pico Setup
To update the firmware on a Raspberry Pi Pico (such as MicroPython or CircuitPython), use the official MicroPython Download Page to grab the .uf2 file for your specific model (Pico, Pico W, Pico 2, or Pico 2 W) and drag-and-drop it onto the device.

1. Download the Firmware: Go to the MicroPython Download Page or your preferred firmware provider (like CircuitPython) to download the .uf2 file matching your board.
2. Enter Bootloader Mode: Press and hold the BOOTSEL button on your Raspberry Pi Pico while plugging the USB cable into your computer.
3. Release BOOTSEL: Once plugged in, release the button. The Pico will mount as a mass storage drive named RPI-RP2 (or RP2350 for Pico 2).
4. Copy the File: Drag and drop the downloaded .uf2 file directly into the RPI-RP2 drive.
5. Auto-Reboot: The Pico will automatically flash the new firmware and restart.

# Steps to Wipe the Pico
1. Download the nuke file: Get the flash_nuke.uf2 file from Raspberry Pi.
2. Enter Bootloader Mode: Disconnect the Pico from your computer. Press and hold the BOOTSEL button on the board, and while holding it down, plug the USB cable into your computer.
3. Open the Drive: Release the BOOTSEL button once it is plugged in. The Pico will appear on your computer as a mass storage device drive named RPI-RP2.
4. Copy the File: Drag and drop the flash_nuke.uf2 file directly into the RPI-RP2 drive.
5. Wait for Completion: The Pico will run the nuke script, clear its entire flash memory, and automatically reboot. After about 10 seconds, it will remount as a blank mass storage device.
Once wiped, you can drag and drop a fresh firmware file (such as MicroPython or CircuitPython) onto the drive to start clean.

# Thonny
Thonny is a free, lightweight Python Integrated Development Environment (IDE) built specifically for students. Developed at the University of Tartu in Estonia, it strips away the overwhelming clutter of professional editors and bundles its own copy of Python so you can start coding immediately.

It connects directly over USB to microcontrollers like the Raspberry Pi Pico or ESP32, making it a go-to tool for basic electronics and robotics.

Get it here:

https://thonny.org/