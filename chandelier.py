import logging
import time

import RPi.GPIO as GPIO
from daemon import runner

class App():
	def __init__(self):
		self.stdin_path = '/dev/null'
		self.stdout_path = '/dev/tty'
		self.stderr_path = '/dev/tty'
		self.pidfile_path =  '/var/run/chandelier/chandelier.pid'
		self.pidfile_timeout = 5

	def __del__(self):
		GPIO.cleanup()

	def run(self):
		GPIO.setmode(GPIO.BOARD)
		GPIO.setup(11, GPIO.OUT)
		GPIO.setup(13, GPIO.OUT)
		GPIO.setup(15, GPIO.OUT)

		while True:
			pass

daemon_runner = runner.DaemonRunner(app)
#This ensures that the logger file handle does not get closed during daemonization
#daemon_runner.daemon_context.files_preserve=[handler.stream]
daemon_runner.do_action()