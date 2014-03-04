PiforceTools
============

Piforce Tools drives a Raspberry Pi with Adafruit LCD Plate and interfaces with debugmode's triforce tools to load a NetDIMM board with binaries for a Triforce, Naomi, or Chihiro arcade system.  

## Usage

Left/Right buttons determine Game mode or Command mode respectively.  Up/Down navigate items within a mode.  Select button will select the item being displayed.  In Command mode, the following commands can be used:

1. Shutdown - To prevent boot failures, make sure you select Shutdown and wait for all lights to go out (except the red one) before removing power.
2. Restart - To force a restart
3. Enable DHCP - To switch back to a normal DHCP configuration, select this, and reboot the Pi.
4. Enable Static - To switch back to a static configuration, select this, and reboot the Pi
5. Ping Netdimm - To test if the Netdimm is reachable via a ping

## Getting Started

You will need the following items to use Piforce Tools:

1. A Raspberry Pi - http://www.raspberrypi.org/ 
2. An SD Card imaged with Raspbian - http://www.raspberrypi.org/downloads
3. An assembled Adafruit 16x2 LCD Plate - http://learn.adafruit.com/adafruit-16x2-character-lcd-plus-keypad-for-raspberry-pi
4. A Naomi, Triforce, or Chihiro arcade system.
5. A Netdimm with a zero-key security PIC installed.  I cannot provide links for this, but a modicum of Google-fu will get you what you need.  The netdimm will need to be configured in static mode with an IP address of 192.168.1.2, netmask of 255.255.255.0, and gateway of 192.168.1.1.
6. A crossover cable

## Installation

Now you are finally ready to install Piforce Tools.

1. Use aptitude to install the following packages:

    ```
    sudo apt-get install python-smbus
    sudo apt-get install python-crypto
    ```

2. Use git to clone piforce tools repo to your pi:

    ```
    cd /home/pi
    git clone https://github.com/capane-us/piforcetools.git
    cd piforcetools
    chmod u+x install.sh
    sudo ./install.sh
    ```

    After you install Piforce Tools, on the next boot, your Pi will be configured to have a static assignment of 192.168.1.1.

3. Copy roms you want to load to /home/pi/roms.  You can use scp, ftp, or wget to get them into this directory, or you can mount a USB drive and copy them.

4. (Optional) Edit piforcetools.py if your roms have different files names, or if you want to change the display name.

5. Reboot

If everything worked, after about 20 seconds you should see the LCD turn on and display the Piforce Tools splash message.  

## Troubleshooting
I provide this script without warranty, and its not feasible to provide support to everyone, but I want to at least provide some troubleshooting steps 

* **LCD powers on, but no text is displayed.** Make sure you adjust the contrast of the LCD Plate.  
* **LCD does not power on** This could be several different things.  First make sure the LCD Plate is assembled correctly by following the usage instructions on Adafruit's product page.  Run the python script provided there and confirm the LCD Plate works.  Double check your solder work.  Depending on your revision of your Raspberry Pi, you may need to change any lines of the Piforce Tools script to specify the bus number when instantiating the LCD Plate object.  For example, change lcd = Adafruit_CharLCDPlate() to lcd = Adafruit_CharLCDPlate(busnum = 0) for a Rev 1 Pi.
* **NO GAMES FOUND! message is displayed** Make sure your roms are in the /home/pi/roms directory and that the filenames match those specified in the piforcetools.py script. 
* **I keep getting Connect Failed! when I try to send a game** Make sure your target device has been configured to be at 192.168.1.2.

## Credit

This could not be done without debugmode's triforce tools script.  All the heavy lifting was done by him, I just made an easy to use interface for his work.  Also shoutout to darksoft for his killer Atomiswave conversions.
