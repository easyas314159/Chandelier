import logging
import time
import signal
import urllib
import urllib2
import base64
import os
import json
import atexit
import sys
import traceback

import RPi.GPIO as GPIO
from daemon import runner
from pca9685 import PCA9685
from rgbled import rgbled

import ConfigParser

cfg=ConfigParser.ConfigParser()
cfg.read("/etc/chandelier")

key = cfg.get("AUTH", "key")
username = cfg.get("AUTH", "username")
password = cfg.get("AUTH", "password")

key = urllib.quote(key)
source = "https://medalta.webscript.io/next?from=" + key
config = "https://medalta.webscript.io/config"

rate_reconfig = 60.0

def remap(v, fromLo, fromHi, toLo, toHi):
	return (toHi - toLo) * (v - fromLo) / (fromHi - fromLo) + toLo

def shutdown(app):
	app.shutdown()
	pass

class App():
	def __init__(self):
		self.stdin_path = '/dev/null'
		self.stdout_path = '/dev/null'
		self.stderr_path = '/dev/null'
		self.pidfile_path =  '/var/run/chandelier.pid'
		self.pidfile_timeout = 5

		self.last_config = 0.0

	def run(self):
		try:
			self.wrapper()
		except Exception as ex:
			logger.error(ex)

	def wrapper(self):
		logger.info("Starting")
		self.configure()

		request = urllib2.Request(source)
		auth = base64.encodestring('%s:%s' % (username, password)).replace('\n', '')
		request.add_header("Authorization", "Basic %s" % auth)

		GPIO.setwarnings(False)
		GPIO.setmode(GPIO.BOARD)

		GPIO.setup(11, GPIO.OUT)
		self._pwm = PCA9685(0x40, 11)
		self._pwm.frequency(10000)
		self._pwm.enable(True)

		self.curr_r = 0xfff
		self.curr_g = 0xfff
		self.curr_b = 0xfff

		self.led = rgbled(self._pwm, 1, 2, 0)
		self.led.set(0xfff, 0xfff, 0xfff)

		atexit.register(shutdown, self)
		while True:
			try:
				data = urllib2.urlopen(request)
				data = json.load(data)

				logger.info(data)

				next_r = 1.0 - data["rgb"]["red"] / 255.0
				next_g = 1.0 - data["rgb"]["green"] / 255.0
				next_b = 1.0 - data["rgb"]["blue"] / 255.0

				next_r *= 0xfff
				next_g *= 0xfff
				next_b *= 0xfff

				elapsed = time.time() - self.last_config
				if elapsed > rate_reconfig:
					self.configure()

				self.fade(next_r, next_g, next_b)
			except urllib2.HTTPError:
				pass
			except urllib2.URLError:
				pass
			except Exception as ex:
				logger.error(ex)

			time.sleep(self.hold_time)

	def fade(self, next_r, next_g, next_b):
		fade_steps = min(511, max( \
			abs(self.curr_r - next_r), \
			abs(self.curr_g - next_g), \
			abs(self.curr_b - next_b)))

		fade_delay = float(self.fade_time) / float(fade_steps)

		for x in range(1, int(fade_steps) + 1, 1):
			self.led.set( \
				remap(x, 0, fade_steps, self.curr_r, next_r), \
				remap(x, 0, fade_steps, self.curr_g, next_g), \
				remap(x, 0, fade_steps, self.curr_b, next_b))

		self.curr_r = next_r
		self.curr_g = next_g
		self.curr_b = next_b

	def configure(self):
		try:
			data = urllib2.urlopen(config)
			data = json.load(data)

			logger.info( "Updating configuration" )

			self.frequency = data["frequency"]
			self.fade_time = data["fade_time"]
			self.hold_time = data["hold_time"]

			self.last_config = time.time()
		except Exception as ex:
			logger.warning(ex)

		if self.frequency < 1.0:
			self.frequency = 1000.0
		if self.fade_time < 0.0:
			self.fade_time = 10.0
		if self.hold_time < 0.0:
			self.hold_time = 0.0

	def shutdown(self):
            logger.info("Shutting down")
            self.led.stop()
            GPIO.cleanup()

logger = logging.getLogger("Chandelier")
logger.setLevel(logging.INFO)

formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
handler = logging.FileHandler("/var/log/chandelier/chandelier.log")
handler.setFormatter(formatter)
logger.addHandler(handler)

#try:
daemon_runner = runner.DaemonRunner(App())
daemon_runner.daemon_context.files_preserve=[handler.stream]
daemon_runner.do_action()
#except Exception as ex:
#    logger.error(traceback.format_stack(ex))
