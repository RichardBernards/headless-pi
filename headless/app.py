import headless.oled as oled
import headless.ui as ui
import headless.config as config
from headless.config import CONFIG

import logging
import time
import subprocess
import psutil

UPDATE_RATE = float(config.get('update_rate_hz'))



class SleepTimer(object):
	def __init__(self, sleep_after_seconds):
		self.sleep_after_seconds = sleep_after_seconds
		self.sleeptime = None
		self.sleeping = False

	def shouldsleep(self):
		return time.time() > self.sleeptime

	def resetsleep(self):
		self.sleeptime = time.time() + self.sleep_after_seconds

	def sleep(self):
		logging.info('Going to sleep')
		#turn off oled
		self.sleeping = True
		global UPDATE_RATE
		UPDATE_RATE = float(CONFIG['update_rate_sleep_hz'])

	def wakeup(self):
		logging.info('Waking up')
		#turn on oled
		self.sleeping = False
		global UPDATE_RATE
		UPDATE_RATE = float(CONFIG['update_rate_hz'])

	def update_sleep(self):
		if not self.sleeping and self.shouldsleep():
			self.sleep()
		elif self.sleeping and not self.shouldsleep():
			self.wakeup()
			self.resetsleep()


class HeadlessPiApp(object):
	def __init__(self):
		self.sleeptimer = SleepTimer(CONFIG['sleep_after_seconds'])
		self.oled = oled.Oled128x32()

	def show_network_info(self):
		logging.info('Showing network information on screen')
		hostname = subprocess.check_output("hostname", shell = True)
		ip = subprocess.check_output("hostname -I | cut -d\' \' -f1", shell = True)
		ui.show_two_lines(self.oled, "h: "+hostname.decode('UTF-8'), "ip:"+ip.decode('UTF-8'))

	def show_usage_info(self):
		svmem = psutil.virtual_memory()
		partitions = psutil.disk_partitions()
		partition_usage = psutil.disk_usage(partitions[0].mountpoint)
		cpu = f"{psutil.cpu_percent()}%"
		disk = f"{partition_usage.used}"
		mem = f"{svmem.percent}%"
		ui.show_two_lines(self.oled, "C:"+cpu+" D:"+disk, "M:"+mem)

	def run(self):
		try:
			self.sleeptimer.resetsleep()
			self.oled = oled.Oled128x32()
			self.show_network_info()

			while True:
				self.sleeptimer.update_sleep()
				#trigger_key_events()
				time.sleep(1.0 / UPDATE_RATE)
		finally:
			self.oled.poweroff()
