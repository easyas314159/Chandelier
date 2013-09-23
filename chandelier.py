import logging
import time
import signal

import RPi.GPIO as GPIO
from daemon import runner

frequency = 50

class App():
	def __init__(self):
		self.stdin_path = '/dev/null'
		self.stdout_path = '/dev/tty'
		self.stderr_path = '/dev/tty'
		self.pidfile_path =  '/var/run/chandelier/chandelier.pid'
		self.pidfile_timeout = 5

	def run(self):
		GPIO.setwarnings(False)

		GPIO.setmode(GPIO.BOARD)
		GPIO.setup(11, GPIO.OUT)
		GPIO.setup(13, GPIO.OUT)
		GPIO.setup(15, GPIO.OUT)

		self.pr = GPIO.PWM(13, frequency)
		self.pg = GPIO.PWM(15, frequency)
		self.pb = GPIO.PWM(11, frequency)

		self.pr.start(100.0)
		self.pg.start(100.0)
		self.pb.start(100.0)

		while True:
			pass

	def shutdown(signal, frame):
		GPIO.cleanup()
		sys.exit(0)

daemon_runner = runner.DaemonRunner(App())
#This ensures that the logger file handle does not get closed during daemonization
#daemon_runner.daemon_context.files_preserve=[handler.stream]
daemon_runner.do_action()
