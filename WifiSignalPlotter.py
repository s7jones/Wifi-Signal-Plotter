# WifiSignalPlotter.py
#	A quick script I've thrown together to get more familiar with Python
#	and to check the difference in signal level between two Wifi adaptors

""" Produces a plot of WiFi strength """

import subprocess
import re
import time
import platform
import matplotlib.pyplot as plt
import numpy as np

plt.ion

fig = plt.figure()
ax = fig.add_subplot(111)

t = time.time()

avg = np.empty(shape=(2, 0))
std = np.empty(shape=(2, 0))

times = np.empty(shape=(0))

while True:

	dataArray = []

	for a in range(0, 100):	#  x in [beginning, end)

		if platform.system() == 'Linux':
			p = subprocess.Popen("iwconfig", stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		elif platform.system() == 'Windows':
			p = subprocess.Popen("netsh wlan show interfaces", stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		else:
			raise Exception('reached else of if statement')
		out = p.stdout.read().decode()

		if platform.system() == 'Linux':
			m = re.findall('(wlan[0-9]+).*?Signal level=(-[0-9]+) dBm', out, re.DOTALL)
		elif platform.system() == 'Windows':
			m = re.findall('Name.*?:.*?([A-z0-9 ]*).*?Signal.*?:.*?([0-9]*)%', out, re.DOTALL)
		else:
			raise Exception('reached else of if statement')

		p.communicate()
		elapsed = time.time() - t

		dataArray.append(m)


		plt.pause(0.1)

	counts = [0, 0]
	sortedData = []
	sortedData.append([])
	sortedData.append([])
	for dataTuples in dataArray:
		for data in dataTuples:
			if data[0] == 'wlan0':
				currentCount = counts[0]
				sortedData[0].append(data[1])
				counts[0] += 1
			elif data[0] == 'wlan1':
				currentCount = counts[1]
				sortedData[1].append(data[1])
				counts[1] += 1
			else:
				raise Exception('reached else of if statement')

	numArray = []
	numArray.append([])
	numArray.append([])
	index = 0
	for dataSet in sortedData:
		for sdata in dataSet:
			numArray[index].append(int(sdata))
		index += 1



	lineSet = []
	lineSet.append('b-')
	lineSet.append('g-')
	index = 0
	avgCurrent = np.zeros((2, 1))
	stdCurrent = np.zeros((2, 1))
	for numSet in numArray:
		avgCurrent[index] = np.mean(numSet)
		stdCurrent[index] = np.std(numSet)
		index += 1

	print(avgCurrent)
	print(stdCurrent)

	avg = np.append(avg, avgCurrent, axis=1)
	std = np.append(std, stdCurrent, axis=1)

	times = np.append(times, elapsed)

	ax.clear()
	plt.xlabel('Time [s]')
	plt.ylabel('Signal Level [dBm]')
	plt.errorbar(times[:], avg[0, :], yerr=std[0, :], label="wlan0 (usb)")
	plt.errorbar(times[:], avg[1, :], yerr=std[1, :], label="wlan1 (internal)")
	plt.legend()
	print("\n\n")

	plt.pause(1)
