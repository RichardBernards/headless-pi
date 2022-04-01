#!/usr/bin/env python
import logging
import time
import RPi.GPIO as GPIO
from headless.config import CONFIG


class Button(object):
	def __init__(self, callback):
		self.pin = int(CONFIG['button_gpio_pin'])
		self.pressed = False
		self.last_time_pressed = 0.0
		self.last_pressed_duration = 0.0
		self.callback = callback
		GPIO.setmode(GPIO.BCM)
		GPIO.setup(self.pin, GPIO.IN)
		GPIO.add_event_detect(self.pin, GPIO.BOTH, callback=self.on_button_event)

	def on_button_event(self, channel):
		if GPIO.input(self.pin):
			self.last_pressed_duration = time.time() - self.last_time_pressed
			logging.debug('Button released after '+str(self.last_pressed_duration))
			self.pressed = False
		else:
			logging.debug('Button pressed down')
			self.pressed = True
			self.last_time_pressed = time.time()
		self.callback(not self.pressed, self.last_pressed_duration)
