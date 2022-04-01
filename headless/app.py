import headless.oled as oled
import headless.button as button
import headless.ui as ui
import headless.config as config
from headless.config import CONFIG

import logging
import time
import subprocess
import psutil

UPDATE_RATE = float(config.get('update_rate_hz'))



class SleepTimer(object):
	def __init__(self, sleep_after_seconds, sleep_callback, wakeup_callback):
		self.sleep_after_seconds = sleep_after_seconds
		self.sleeptime = None
		self.sleeping = False
		self.sleep_callback = sleep_callback
		self.wakeup_callback = wakeup_callback

	def shouldsleep(self):
		return time.time() > self.sleeptime

	def resetsleep(self):
		self.sleeptime = time.time() + self.sleep_after_seconds

	def sleep(self):
		logging.info('Going to sleep')
		self.sleep_callback()
		self.sleeping = True
		global UPDATE_RATE
		UPDATE_RATE = float(CONFIG['update_rate_sleep_hz'])

	def wakeup(self):
		logging.info('Waking up')
		self.wakeup_callback()
		self.sleeping = False
		global UPDATE_RATE
		UPDATE_RATE = float(CONFIG['update_rate_hz'])

	def update_sleep(self):
		if not self.sleeping and self.shouldsleep():
			self.sleep()
		elif self.sleeping and not self.shouldsleep():
			self.wakeup()
			self.resetsleep()

class ActionTimer(object):
	def __init__(self, name, action_after_seconds, callback):
		self.name = name
		self.action_after_seconds = action_after_seconds
		self.actiontime = None
		self.waiting = False
		self.callback = callback

	def clear(self):
		logging.debug('Clearing ActionTimer '+self.name)
		self.waiting = False
		self.actiontime = None

	def reset(self):
		logging.debug('Resetting ActionTimer '+self.name)
		self.actiontime = time.time() + self.action_after_seconds
		self.waiting = True

	def shoulddoaction(self):
		return time.time() > self.actiontime

	def doaction(self):
		logging.debug('Doing action on timer '+self.name)
		self.waiting = False
		self.callback()

	def update(self):
		logging.debug('Updating ActionTimer '+self.name)
		if self.waiting and self.shoulddoaction():
			self.doaction()

	def __del__(self):
		logging.debug('Deleted ActionTimer '+self.name)


class HeadlessPiApp(object):
	def __init__(self):
		self.oled = oled.Oled128x32()
		self.button = button.Button(self.check_button_event)
		self.sleeptimer = SleepTimer(CONFIG['sleep_after_seconds'], self.oled.poweroff, self.oled.poweron)
		self.reboottimer = ActionTimer('reboot', CONFIG['reboot_timeout_seconds'], self.reboot)
		self.shutdowntimer = ActionTimer('shutdown', CONFIG['shutdown_timeout_seconds'], self.shutdown)
		self.menustate = 0

	def show_network_info(self):
		logging.info('Showing network information on screen')
		hostname = subprocess.check_output("hostname", shell = True)
		ip = subprocess.check_output("hostname -I | cut -d\' \' -f1", shell = True)
		ui.show_two_lines(self.oled, "h: "+hostname.decode('UTF-8'), "ip:"+ip.decode('UTF-8'))

	def show_usage_info(self):
		logging.info('Showing usage information on screen')
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
			self.paint_menu()

			while True:
				self.sleeptimer.update_sleep()
				self.reboottimer.update()
				self.shutdowntimer.update()
				time.sleep(1.0 / UPDATE_RATE)

		except KeyboardInterrupt:
			self.haltexecution()

		finally:
			self.oled.poweroff()


	def check_button_event(self, released, duration):
		self.sleeptimer.resetsleep()
		if duration > float(int(CONFIG['button_delay_milliseconds'])/1000):
			if released:
				self.menustate += 1
				self.paint_menu()
				self.reboottimer.clear()
				self.shutdowntimer.clear()
			else:
				if self.menustate == 2:
					if not self.reboottimer.waiting:
						self.reboottimer.reset()
				elif self.menustate == 3:
					if not self.shutdowntimer.waiting:
						self.shutdowntimer.reset()


	def paint_menu(self):
		logging.debug('Painting menu')
		if self.menustate > 3:
			self.menustate = 0
		elif self.menustate < 0:
			self.menustate = 3

		if self.menustate == 0:
			self.show_network_info()
		elif self.menustate == 1:
			self.show_usage_info()
		elif self.menustate == 2:
			ui.show_line(self.oled, "REBOOT")
		elif self.menustate == 3:
			ui.show_line(self.oled, "SHUTDOWN")
		else:
			logging.warning('Unknown menustate '+self.menustate)


	def reboot(self):
		logging.warning('Rebooting now')
		subprocess.Popen("sudo reboot now", shell = True)
		self.haltexecution()

	def shutdown(self):
		logging.warning('Shutting down now')
		subprocess.Popen("sudo shutdown -h now", shell = True)
		self.haltexecution()

	def haltexecution(self):
		self.oled.poweroff()
		del self.reboottimer
		del self.shutdowntimer
		exit()
