Raspberry Pi as a USB Midi Host for Yamaha DGX-520 Electronic Piano

A Raspberry Pi running Raspbian can be configured as a USB Midi host, using the ALSA utilities to connect Midi enabled devices to each other. There are many websites detailing the steps if you Google it.

The main problem I have, is that my Yamaha DGX-520 works for a few seconds, and then the Midi Interface locks up, requiring a reboot to re-enable it. This project is a workaround based on many hours of experimentation. It connects two USB Midi devices as inputs only, and appears very reliable. My coding is not the most efficient, soz, but it may provide ideas for improvement. Hopefully, it will be of interest to someone.

The code is written in Python3, and this file describes the steps necessary to install it as a utility to auto-run in the background at RPi startup.

The Raspberry Pi is an early model, with two USB ports, and wired Ethernet. It is running Raspbian Buster Lite (headless). It hijacks the built in ACT LED to show the running status, and has a pushbutton connected to GPIO to trigger hardware detection, and a method for SD safe shutdown.

INSTALLATION:-

Install Pyusb with ... sudo apt-get install python3-usb

Install RPi.GPIO with ... sudo apt-get install rpi.gpio

Copy midiconnect.service to /etc/systemd/sytem/ (ensure logged in as root for permissions)

Enable service at boot using ... sudo systemctl enable midiconnect.service ... from command line.

Copy midi-connect.py to /home/pi/

Reboot ... Good Luck

The Arduino is connected to an old Wii Drums game pad, the piezo transducers connected directly to the Arduino A/D converter. The code for this will be placed in a seperate repository (eventually).