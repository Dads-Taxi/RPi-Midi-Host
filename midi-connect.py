import os, usb.core, usb.util
import RPi.GPIO as GPIO
from time import monotonic


# FUNCTION DEFINITIONS

def dettachmocolufa():
   global mococfg, mocointf, mocobintf, mocoepin, mocoepout
   mococfg = mocolufa [0]
   mocointf = mococfg[(1,0)]
   mocobintf = mocointf.bInterfaceNumber
   mocoepin = mocointf[1]
   mocoepout = mocointf[0]

   if mocolufa.is_kernel_driver_active(0):
      mocolufa.detach_kernel_driver(0)
      #print("MocoLUFA kernel driver interface 0 detached")

   if mocolufa.is_kernel_driver_active(mocobintf):
      mocolufa.detach_kernel_driver(mocobintf)
      #print("MocoLUFA kernel driver interface", mocobintf, "detached")
      usb.util.claim_interface(mocolufa, mocobintf)


def dettachyamaha():
   global dgxcfg, dgxintf, dgxbintf, dgxepin, dgxepout
   dgxcfg = yamaha[0]
   dgxintf = dgxcfg[(0,0)]
   dgxbintf = dgxintf.bInterfaceNumber
   dgxepin = dgxintf[0]
   dgxepout = dgxintf[1]

   if yamaha.is_kernel_driver_active(dgxbintf):
      yamaha.detach_kernel_driver(dgxbintf)
      #print("Yamaha kernel driver interface", dgxbintf, "detached")
      usb.util.claim_interface(yamaha, dgxbintf)


def dettachmidiplus():
   global mkbcfg, mkbintf, mkbbintf, mkbepin, mkbepout
   mkbcfg = midiplus[0]
   mkbintf = mkbcfg[(0,0)]
   mkbbintf = mkbintf.bInterfaceNumber
   mkbepin = mkbintf[1]
   mkbepout = mkbintf[0]

   if midiplus.is_kernel_driver_active(mkbbintf):
      midiplus.detach_kernel_driver(mkbbintf)
      #print("Midiplus kernel driver interface", mkbbintf, "detached")
      usb.util.claim_interface(midiplus, mkbbintf)


def scanfordevices():
   global mocolufa, arduino, yamaha, adapter, midiplus
   global mocolufadetected, arduinodetected, yamahadetected, adapterdetected, midiplusdetected

   mocolufa = usb.core.find(idVendor=0x03eb, idProduct=0x2048)  # MocoLUFA Midi
   arduino = usb.core.find(idVendor=0x2341, idProduct=0x0001)  # Arduino Serial
   yamaha = usb.core.find(idVendor=0x0499, idProduct=0x1039)  # DGX-520
   adapter = usb.core.find(idVendor=0x0a92, idProduct=0x1010)  # USB to Midi Adapter
   midiplus = usb.core.find(idVendor=0x0ccd, idProduct=0x0035)  # Midiplus 61 Keyboard

   if mocolufa == None:
      mocolufadetected = False
   else:
      if not mocolufadetected:
         print("MocoLUFA detected")
         dettachmocolufa()
         mocolufadetected = True

   if arduino == None:
      arduinodetected = False
   else:
      if not arduinodetected:
         print("Arduino Serial detected")
         arduinodetected = True

   if yamaha == None:
      yamahadetected = False
   else:
      if not yamahadetected:
         print("DGX-520 detected")
         dettachyamaha()
         yamahadetected = True

   if adapter == None:
      adapterdetected = False
   else:
      if not adapterdetected:
         print("USB Midi Adapter detected")
         adapterdetected = True

   if midiplus == None:
      midiplusdetected = False
   else:
      if not midiplusdetected:
         print("Midiplus Keyboard detected")
         dettachmidiplus()
         midiplusdetected = True



# MAIN PROGRAM

# disable the operating system control of ACT led
os.system("echo gpio | sudo tee /sys/class/leds/led0/trigger")

# setup GPIO interface
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Setup GPIO 16 connected to ACT LED
GPIO.setup(16, GPIO.OUT)

# Setup GPIO 7 (pin pair next to yellow audio socket)
# internal pullup enabled, connect n/o pushbutton across pins
GPIO.setup(7, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# ACT LED control variables
ledontime = 1
ledofftime = 0.5
ledtoggle = False
ledstart = 0

# Shutdown timer control variables
rbtwaittime = 3
shdwaittime = 6
shdenable = False
showshdmessage = True
shdstart = 0

# Device detection control variables
enablescan = True
mocolufadetected = False
arduinodetected = False
yamahadetected = False
adapterdetected = False
midiplusdetected = False


while True:    # continuous loop

   if enablescan:
      scanfordevices()
      enablescan = False
   else:

      if mocolufadetected:   # Drumkit Midi to DGX-520
         try:
            mocodata = mocoepin.read(mocoepin.wMaxPacketSize, 1)
         except usb.core.USBError as mocoerror:
            if mocoerror.args[0] == 32 or mocoerror.args[0] == 19:
               print("Drumkit has been disconnected")
               mocolufadetected = False
         else:
            # DGX-520 requires all 64 bytes in every transfer
            if len(mocodata) < 0x40:
               for i in range(len(mocodata), 0x40):
                  mocodata.append(0)
            if yamahadetected:
               dgxepout.write(mocodata)

      if yamahadetected:   # DGX-520, continually polling enables Midi to work without locking up
         try:
            dgxdata = dgxepin.read(dgxepin.wMaxPacketSize, 1)
         except usb.core.USBError as dgxerror:
            if dgxerror.args[0] == 32 or dgxerror.args[0] == 19:
               print("DGX-520 has been disconnected")
               yamahadetected = False

      if midiplusdetected:   # Midiplus Keyboard to DGX-520
         try:
            mkbdata = mkbepin.read(mkbepin.wMaxPacketSize, 1)
         except usb.core.USBError as mkboerror:
            if mkboerror.args[0] == 32 or mkboerror.args[0] == 19:
               print("Midiplus Keyboard has been disconnected")
               midiplusdetected = False
         else:
            # Midiplus Keyboard supplies 64 bytes which satisfies DGX-520 requirements
            if yamahadetected:
               dgxepout.write(mkbdata)


   # monitor GPIO 7 for button press
   if GPIO.input(7):
      ledontime = 2
      ledofftime = 1
      shdenable = False
   else:                 # button pressed
      ledontime = 0.1
      ledofftime = 0.1
      shdenable = True


   # ACT LED control
   if ledtoggle:
      if monotonic() - ledstart > ledontime:
         ledstart = monotonic()
         ledtoggle = False
         GPIO.output(16,GPIO.HIGH)
   else:
      if monotonic() - ledstart > ledofftime:
         ledstart = monotonic()
         ledtoggle = True
         GPIO.output(16,GPIO.LOW)


   # Shutdown control and USB device scan enable
   if shdenable:
      if showshdmessage:
         print("SHUTTING DOWN IN", shdwaittime, "SECONDS")
         enablescan = True
         showshdmessage = False
      if monotonic() - shdstart > shdwaittime:
         os.system("sudo shutdown -h now")
   else:
      shdstart = monotonic()
      if not showshdmessage:
         print("SHUTDOWN CANCELLED")
      showshdmessage = True


# END OF PROGRAM
