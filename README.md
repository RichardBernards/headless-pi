# headless-pi
Python application to show useful information on tiny OLED screen for a headless Raspberry Pi.

## Introduction
Python code is intended to be ran on a Raspberry Pi with a 128x32 small oled display connected to it over i2c. A pulse button connected to a GPIO pin can be used to cycle through the screens and to reboot or shutdown (halt) the Raspberry Pi.

## Features
* View networking information (hostname and ip-address) on oled-screen
* View usage information (cpu%, disk usage, memory usage) on oled-screen
* Reboot (invokes `sudo reboot now` using 5 seconds press when in the correct menu-state (no worries, a progressbar will tell you when to let go)
* Shutdown (invokes `sudo shutdown now` using 10 seconds press when in the correct menu-state (no worries, a progressbar will tell you when to let go)
* Ability to use your own font on the screen (ttf)
* Sleep timeout of 15 seconds (oled screen will poweroff after this time
* All timeouts listed above are configurable at top of script
* Set `VERBOSE = True` if you want more verbose output on the commandline

## Dependencies
This piece of code depends on:
* [Adafruit CircuitPython SSD1305](https://github.com/adafruit/Adafruit_CircuitPython_SSD1306/)

## Installing on Raspberry PI
TBD

## Usage Example
TBD

## Contributing
Contributions are welcome! Please use the issues or feature requests functionality of GitHub.
