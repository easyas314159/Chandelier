#!/usr/bin/env python
# encoding: utf-8
import RPi.GPIO as GPIO
from pca9685 import PCA9685

class rgbled:
	def __init__(self, pwm, pin_r, pin_g, pin_b):
		self._pwm = pwm

		self._r = pin_r
		self._g = pin_g
		self._b = pin_b

	def __del__(self):
		self.stop()

	def set(self, r, g, b):
		self._pwm.set(self._r, 0, r)
		self._pwm.set(self._g, 0, g)
		self._pwm.set(self._b, 0, b)
