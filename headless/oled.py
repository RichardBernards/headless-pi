#!/usr/bin/env python
import logging
import busio
import adafruit_ssd1306
from board import SCL, SDA
from PIL import Image, ImageDraw, ImageFont


class Oled128x32(object):
	def __init__(self):
		self.width = 128
		self.height = 32

		self.i2c = busio.I2C(SCL, SDA)
		self.screen = adafruit_ssd1306.SSD1306_I2C(self.width, self.height, self.i2c)
		self.screen.rotation = 2
		self.screen.fill(0)

		self.image = Image.new("1", (self.width, self.height))
		self.draw = ImageDraw.Draw(self.image)

		self.font = ImageFont.load_default()

		self.powered = True

	def paint(self):
		self.screen.image(self.image)
		self.screen.show()

	def clear(self):
		self.draw.rectangle((0, 0, self.width, self.height), outline=0, fill=0)
		self.paint()

	def poweroff(self):
		self.clear()
		self.screen.poweroff()
		self.powered = False

	def poweron(self):
		self.screen.poweron()
		self.clear()
		self.powered = True
