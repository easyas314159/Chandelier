import logging
import time
import signal
import urllib2
import base64
import os
import json

import RPi.GPIO as GPIO
from daemon import runner

from rgbled import rgbled

username = "chandelier"
password = "porcelain"

key = "%2B16475600832"
source = "https://medalta.webscript.io/next?from=" + key

frequency=50
fade_time=5.0
fade_steps=60
pause=5.0

class App():
	def __init__(self):
		self.stdin_path = '/dev/null'
		self.stdout_path = '/dev/tty'
		self.stderr_path = '/dev/tty'
		self.pidfile_path =  '/var/run/chandelier/chandelier.pid'
		self.pidfile_timeout = 5

	def run(self):
		request = urllib2.Request(source)
		auth = base64.encodestring('%s:%s' % (username, password)).replace('\n', '')
		request.add_header("Authorization", "Basic %s" % auth)

		GPIO.setwarnings(False)
		GPIO.setmode(GPIO.BOARD)

		curr_r = 100.0
		curr_g = 100.0
		curr_b = 100.0

		led = rgbled(13, 15, 11, frequency)
		led.ChangeDutyCycle(100.0, 100.0, 100.0)

		while True:
			try:
				data = urllib2.urlopen(request)
				data = json.load(data)

				next_r = 100.0 * (1.0 - data["rgb"]["red"] / 255.0)
				next_g = 100.0 * (1.0 - data["rgb"]["green"] / 255.0)
				next_b = 100.0 * (1.0 - data["rgb"]["blue"] / 255.0)

				curr_r = next_r
				curr_g = next_g
				curr_b = next_b

				led.ChangeDutyCycle(curr_r, curr_g, curr_b)
			except:
				pass

			time.sleep(pause)

	def shutdown(signal, frame):
		GPIO.cleanup()
		sys.exit(0)

daemon_runner = runner.DaemonRunner(App())
#This ensures that the logger file handle does not get closed during daemonization
#daemon_runner.daemon_context.files_preserve=[handler.stream]
daemon_runner.do_action()
