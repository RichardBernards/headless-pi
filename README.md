# headless-pi
Python application to show useful information on tiny OLED screen for a headless Raspberry Pi.

## Introduction
Python code is intended to be ran on a Raspberry Pi with a 128x32 small oled display connected to it over i2c. A pulse button connected to a GPIO pin can be used to cycle through the screens and to reboot or shutdown (halt) the Raspberry Pi.

## Features
* View networking information (hostname and ip-address) on oled-screen
* View usage information (cpu%, disk usage, memory usage) on oled-screen
* Reboot (invokes `sudo reboot now` using 5 seconds press when in the correct menu-state
* Shutdown (invokes `sudo shutdown now` using 10 seconds press when in the correct menu-state
* Sleep timeout of 15 seconds (oled screen will poweroff after this time and wake up whenever the button is pressed again
* All timeouts listed above are configurable in the config.json file

## Dependencies
This piece of code depends on:
* [Adafruit CircuitPython SSD1305](https://github.com/adafruit/Adafruit_CircuitPython_SSD1306/)

## Installing on Raspberry PI
Clone repository, make sure you have python3, pip for python3, python3-pil, python-smbus and i2ctools installed, than install pip dependencies and lastly supply file with execution permissions:
```
git clone https://github.com/RichardBernards/headless-pi.git
sudo apt-get install python3  pyhon3-pip python3-pil python-smbus i2ctools
cd headless-pi
sudo pip install -r requirements.txt
chmod a+x headless-pi.py
```

## Usage Example
```
./headless-pi.py
```
You can use `Ctrl + C` to exit. This will also power off the oled display

## Contributing
Contributions are welcome! Please use the issues or feature requests functionality of GitHub.
