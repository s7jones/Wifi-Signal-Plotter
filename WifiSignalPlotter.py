# WifiSignalPlotter.py
#	A quick script I've thrown together to get more familiar with Python
#	and to check the difference in signal level between two Wifi adaptors

""" Produces a plot of WiFi strength """

import subprocess
import re
import time
import matplotlib.pyplot as plt
import numpy as np

CONST_TIME_INTERVAL = 10
CONST_NUM_SAMPLES = 100

plt.ion

fig = plt.figure()
ax = fig.add_subplot(111)

t = time.time()

arrayCreation = False

times = np.empty(shape=(0))

interfaceDict = dict()
interfaceCount = 0

while True:

	dataArray = []

	for a in range(0, CONST_NUM_SAMPLES):	#  x in [beginning, end)
		p = subprocess.Popen("iwconfig", stdout=subprocess.PIPE, stderr=subprocess.PIPE)

		out = p.stdout.read().decode()

		m = re.findall('(wlan[0-9]+).*?Signal level=(-[0-9]+) dBm', out, re.DOTALL)
		p.communicate()
		elapsed = time.time() - t

		if type(m) is not list:
			raise Exception('not a list')
		for mTuple in m:
			if type(mTuple) is not tuple:
				raise Exception('not a tuple')
			if len(mTuple) != 2:
				raise Exception('number of regex matches not 2')
			if len(mTuple) % 2 != 0: # useful if the regex results for multiple interfaces is in a single tuple
				raise Exception('number of regex matches not divisible by 2')
			interfaceName = mTuple[0]
			if interfaceName not in interfaceDict:
				interfaceDict[interfaceName] = interfaceCount
				interfaceCount += 1

		dataArray.append(m)
		time.sleep(CONST_TIME_INTERVAL/CONST_NUM_SAMPLES)

	counts = np.zeros(len(interfaceDict))

	sortedData = []
	for i in range(0, len(interfaceDict)):
		sortedData.append([])

	if len(sortedData) != interfaceCount:
		raise Exception('data table and number of devices not in agreement')

	for dataTuples in dataArray:
		for data in dataTuples:
			switchResult = interfaceDict.get(data[0])
			currentCount = counts[switchResult]
			sortedData[switchResult].append(data[1])
			counts[switchResult] += 1


	numArray = []
	for i in range(0, len(interfaceDict)):
		numArray.append([])

	index = 0
	for dataSet in sortedData:
		for sdata in dataSet:
			numArray[index].append(int(sdata))
		index += 1

	if 'avg' not in locals():
		avg = np.empty(shape=(len(interfaceDict), 0))

	if 'std' not in locals():
		std = np.empty(shape=(len(interfaceDict), 0))

	index = 0
	avgCurrent = np.zeros((len(interfaceDict), 1))
	stdCurrent = np.zeros((len(interfaceDict), 1))
	for numSet in numArray:
		avgCurrent[index] = np.mean(numSet)
		stdCurrent[index] = np.std(numSet)
		index += 1

	avg = np.append(avg, avgCurrent, axis=1)
	std = np.append(std, stdCurrent, axis=1)

	times = np.append(times, elapsed)

	ax.clear()
	plt.xlabel('Time [s]')
	plt.ylabel('Signal Level [dBm]')
	for key, value in interfaceDict.items():
		plt.errorbar(times[:], avg[value, :], yerr=std[value, :], label=key)
	plt.legend()
	print('\n\n')

	plt.pause(1)
