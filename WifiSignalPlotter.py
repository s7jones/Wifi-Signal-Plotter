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

CONST_TIME_INTERVAL = 10
CONST_NUM_SAMPLES = 100
MEASURING_ERROR_WINDOWS = 0.5
MEASURING_ERROR_LINUX = 0.5

def main():
	t, times, avg, err, interfaceDict = initialize_data()
	fig, ax = initialize_plot()
	while True:
		times, avg, err, interfaceDict = get_data(t, times, avg, err, interfaceDict)
		update_plot(fig, ax, times, avg, err, interfaceDict)
		plt.pause(1)

def initialize_data():
	interfaceDict = dict()
	t = time.time()
	m = read_data_from_cmd()
	interfaceDict = sort_regex_results(m, interfaceDict)
	times = np.empty(shape=(0))
	avg = np.empty(shape=(len(interfaceDict), 0))
	err = np.empty(shape=(len(interfaceDict), 0))
	return t, times, avg, err, interfaceDict

def initialize_plot():
	plt.ion()
	fig, ax = plt.subplots()
	return fig, ax


def update_plot(fig, ax, times, avg, err, interfaceDict):
	ax.clear()
	ax.set_title('Wifi Signal over Time')
	plt.xlabel('Time [s]')
	if platform.system() == 'Linux':
		plt.ylabel('Signal Level [dBm]')
	elif platform.system() == 'Windows':
		plt.ylabel('Signal Level [%]')
	else:
		raise Exception('reached else of if statement')
	for key, value in interfaceDict.items():
		plt.errorbar(times[:], avg[value, :], yerr=err[value, :], label=key)
	plt.legend()
	print('\n\n')
	plt.pause(0.0001)
	plt.show()


def get_data(t, times, avg, err, interfaceDict):
	dataArray = []
	for a in range(0, CONST_NUM_SAMPLES):	#  x in [beginning, end)
		m = read_data_from_cmd()
		elapsed = time.time() - t
		interfaceDict = sort_regex_results(m, interfaceDict)
		dataArray.append(m)
		time.sleep(CONST_TIME_INTERVAL/CONST_NUM_SAMPLES)

	counts = np.zeros(len(interfaceDict))

	sortedData = []
	for i in range(0, len(interfaceDict)):
		sortedData.append([])

	if len(sortedData) != len(interfaceDict):
		raise Exception('data table and number of devices not in agreement')

	for dataTuples in dataArray:
		for data in dataTuples:
			switchResult = interfaceDict.get(data[0])
			#currentCount = counts[switchResult]
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

	if platform.system() == 'Linux':
		measuringError = MEASURING_ERROR_LINUX
	elif platform.system() == 'Windows':
		measuringError = MEASURING_ERROR_WINDOWS
	else:
		raise Exception('reached else of if statement')

	index = 0
	avgCurrent = np.zeros((len(interfaceDict), 1))
	errCurrent = np.zeros((len(interfaceDict), 1))
	for numSet in numArray:
		avgCurrent[index] = np.mean(numSet)
		combinedErr = np.sqrt(np.std(numSet)**2 + measuringError**2)
		errCurrent[index] = combinedErr
		index += 1

	avg = np.append(avg, avgCurrent, axis=1)
	err = np.append(err, errCurrent, axis=1)

	times = np.append(times, elapsed)

	return times, avg, err, interfaceDict

def read_data_from_cmd():
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

	return m

def sort_regex_results(m, interfaceDict):
	#if type(m) is not list:
	#	raise Exception('not a list')
	for mTuple in m:
		if type(mTuple) is not tuple:
			raise Exception('not a tuple')
		if len(mTuple) != 2:
			raise Exception('number of regex matches not 2')
		if len(mTuple) % 2 != 0:
			# useful if the regex results for multiple interfaces is in a single tuple
			raise Exception('number of regex matches not divisible by 2')
		interfaceName = mTuple[0]
		if interfaceName not in interfaceDict:
			interfaceDict[interfaceName] = len(interfaceDict)

	return interfaceDict

if __name__ == "__main__":
	main()
	