#!/usr/bin/env python
# encoding: utf-8
import RPi.GPIO as GPIO

class rgbled:
	def __init__(self, pin_r, pin_g, pin_b, freq = 256):
		GPIO.setup(pin_r, GPIO.OUT)
		GPIO.setup(pin_g, GPIO.OUT)
		GPIO.setup(pin_b, GPIO.OUT)

		self.r = GPIO.PWM(pin_r, freq)
		self.g = GPIO.PWM(pin_g, freq)
		self.b = GPIO.PWM(pin_b, freq)

	def __del__(self):
		self.stop()

	def stop(self):
		self.r.stop()
		self.g.stop()
		self.b.stop()

	def start(self, r = 0.0, g = 0.0, b = 0.0):
		self.r.start(r)
		self.g.start(g)
		self.b.start(b)

	def ChangeFrequency(self, freq):
		self.r.ChangeFrequency(freq)
		self.g.ChangeFrequency(freq)
		self.b.ChangeFrequency(freq)

	def ChangeDutyCycle(self, r = 0.0, g = 0.0, b = 0.0):
		self.r.ChangeDutyCycle(r)
		self.g.ChangeDutyCycle(g)
		self.b.ChangeDutyCycle(b)