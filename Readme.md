Raspberry Pi as a USB Midi Host for Yamaha DGX-520 Electronic Piano

A Raspberry Pi running Raspbian can be configured as a USB Midi host, using the ALSA utilities to connect Midi enabled devices to each other. There are many websites detailing the necessary steps.

The main problem with this method is that the Yamaha DGX-520 works for a few seconds, and then the Midi Interface locks up, requiring a reboot to re-enable it. This project is an alternative based on many hours of experimentation. It connects two USB Midi devices as inputs to the DGX-520 (no output required), and appears very reliable. The code is probably not the most efficient or pretty, soz, but it may provide ideas for a similar project.

The code is written in Python3, and is installed as a background service to auto-run at RPi startup.

The Raspberry Pi is an early model (two USB ports, wired Ethernet) running Raspbian Buster Lite (headless). It is intended to run with no monitor or ethernet connected, so the built in ACT LED is hijacked to show the running status, and there is a pushbutton connected to GPIO to trigger hardware detection, and a method for SD safe shutdown.

INSTALLATION:-

Install Pyusb with ... sudo apt-get install python3-usb

Install RPi.GPIO with ... sudo apt-get install rpi.gpio

Copy midiconnect.service to ... /etc/systemd/sytem/ ... (ensure logged in as root for permissions)

Enable service at boot using ... sudo systemctl enable midiconnect.service ... from command line.

Copy midi-connect.py to /home/pi/ ... (ensure file has root ownership, otherwise it will throw permission exceptions)

Reboot ... Good Luck

The Arduino mentioned in the code is a Uno clone connected to an old Wii Drums game pad. The drum pad piezo transducers are connected to the Arduino A/D converter. The Uno USB Interface uController has been re-flashed with the MocoLUFA dual Midi/Serial firmware. The code for this project will be placed in a seperate repository (eventually).
