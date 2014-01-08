#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  untitled.py
#  
#  Copyright 2014 Dino <dino@Dracon>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  

from pylab import *
import math

def main():
	
	dat = open("/home/dino/git/easypass/data/3-gram-noshift-cv-1.txt","r")
	podatci = []
	for line in dat:
		s = [float(i) for i in line.split()]
		print s
		podatci.append(s)
	
	epoch1 = [0,0,0,0,0]
	epoch2 = [0,0,0,0,0]
	epoch3 = [0,0,0,0,0]
	num1 = [0,0,0,0,0]
	num2 = [0,0,0,0,0]
	num3 = [0,0,0,0,0]
	epo1 = [0,0,0]
	epo2 = [0,0,0]
	epo3 = [0,0,0]
	X = [0.001,0.005,0.01,0.1,0.5]
	X2 = [10, 20, 30]
	for item in podatci:
		if item[0] == 10:
			if item[2] == 200:
				epo1[0] += item[4]
			elif item[2] == 300:
				epo2[0] += item[4]
			elif item[2] == 400:
				epo3[0] += item[4]
		elif item[0] == 20:
			if item[2] == 200:
				epo1[1] += item[4]
			elif item[2] == 300:
				epo2[1] += item[4]
			elif item[2] == 400:
				epo3[1] += item[4]
		elif item[0] == 30:
			if item[2] == 200:
				epo1[2] += item[4]
			elif item[2] == 300:
				epo2[2] += item[4]
			elif item[2] == 400:
				epo3[2] += item[4]
		if (item[3] == 0.001):
			if (item[0] == 10):
				num1[0] += item[4]
			elif (item[0] == 20):
				num2[0] += item[4]
			elif (item[0] == 30):
				num3[0] += item[4]
			if (item[2] == 200):
				epoch1[0] += item[4]
			elif (item[2] == 300):
				epoch2[0] += item[4]
			elif (item[2] == 400):
				epoch3[0] += item[4]
		elif (item[3] == 0.005):
			if (item[0] == 10):
				num1[1] += item[4]
			elif (item[0] == 20):
				num2[1] += item[4]
			elif (item[0] == 30):
				num3[1] += item[4]
			if (item[2] == 200):
				epoch1[1] += item[4]
			elif (item[2] == 300):
				epoch2[1] += item[4]
			elif (item[2] == 400):
				epoch3[1] += item[4]
		elif (item[3] == 0.01):
			if (item[0] == 10):
				num1[2] += item[4]
			elif (item[0] == 20):
				num2[2] += item[4]
			elif (item[0] == 30):
				num3[2] += item[4]
			if (item[2] == 200):
				epoch1[2] += item[4]
			elif (item[2] == 300):
				epoch2[2] += item[4]
			elif (item[2] == 400):
				epoch3[2] += item[4]
		elif (item[3] == 0.1):
			if (item[0] == 10):
				num1[3] += item[4]
			elif (item[0] == 20):
				num2[3] += item[4]
			elif (item[0] == 30):
				num3[3] += item[4]
			if (item[2] == 200):
				epoch1[3] += item[4]
			elif (item[2] == 300):
				epoch2[3] += item[4]
			elif (item[2] == 400):
				epoch3[3] += item[4]
		elif (item[3] == 0.5):
			if (item[0] == 10):
				num1[4] += item[4]
			elif (item[0] == 20):
				num2[4] += item[4]
			elif (item[0] == 30):
				num3[4] += item[4]
			if (item[2] == 200):
				epoch1[4] += item[4]
			elif (item[2] == 300):
				epoch2[4] += item[4]
			elif (item[2] == 400):
				epoch3[4] += item[4]
	for i in range(5):
		epoch1[i] /= 3
		epoch2[i] /= 3
		epoch3[i] /= 3
		num1[i] /= 3
		num2[i] /= 3
		num3[i] /= 3
	for i in range(3):
		epo1[i] /=5
		epo2[i] /=5
		epo3[i] /=5
	
	plot(X2,epo1,label="epochs=200")
	plot(X2,epo2,label="epochs=300")
	plot(X2,epo3,label="epochs=400")
	xlabel("size")
	#xscale("log")
	ylabel("error MSE")
	
	legend(loc='upper left')
	show()
			
	return 0

if __name__ == '__main__':
	main()

