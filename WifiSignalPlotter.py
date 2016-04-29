## 	WifiSignalPlotter.py
#		A quick script I've thrown together to get more familiar with Python
#		and to check the difference in signal level between two Wifi adaptors

import matplotlib.pyplot as plt
import subprocess
import re
import time
import numpy as np

plt.ion

fig = plt.figure()
ax  = fig.add_subplot(111)

t = time.time()

avg = np.empty(shape=(2,0))
std = np.empty(shape=(2,0))

times = np.empty(shape=(0))

#avg = []
#avg.append([])
#avg.append([])
#std = []
#std.append([])

while True:

	#subprocess.call(["ls", "-l"])
	#subprocess.call("iwconfig")	

	dataArray = []

	for a in range(0,100):	#  x in [beginning,end)
		
		p = subprocess.Popen("iwconfig", stdout=subprocess.PIPE, stderr=subprocess.PIPE)

		out = p.stdout.read().decode()
		#repr(out)

		
		#m = re.search('(wlan[0-9]+)[.\n]*?Signal level=(-[0-9]+) dBm',out,re.DOTALL)
		#m = re.search('(wlan[0-9]+).*?Signal level=(-[0-9]+) dBm',out,re.DOTALL)

		m = re.findall('(wlan[0-9]+).*?Signal level=(-[0-9]+) dBm',out,re.DOTALL)

		
		p.communicate();
		elapsed = time.time() - t;
		#print(out)
		#print(m)
		#print(len(m))

		dataArray.append(m);

		#print(m[0][0])
		#print(elapsed)

		plt.pause(0.1)

	counts = [0,0]
	#sortedData   = {}
	sortedData   = []
	sortedData.append([])
	sortedData.append([])
	for dataTuples in dataArray:
		for data in dataTuples:
			#print(data)
			if data[0] == 'wlan0':
				currentCount = counts[0]
				#sortedData[0,currentCount] = data[1];
				sortedData[0].append(data[1])
				counts[0] += 1
			elif data[0] == 'wlan1':
				currentCount = counts[1]
				#sortedData[1,currentCount] = data[1];
				sortedData[1].append(data[1])
				counts[1] += 1
			else:
				raise Exception('reached else of if statement')

	numArray = []
	numArray.append([])
	numArray.append([])
	index = 0;
	for dataSet in sortedData:
		for sdata in dataSet:
			#print(int(sdata))
			numArray[index].append(int(sdata))
		index += 1



	lineSet = []
	lineSet.append('b-')
	lineSet.append('g-')
	index = 0;
	avgCurrent = np.zeros((2,1))
	stdCurrent = np.zeros((2,1))
	for numSet in numArray:
		avgCurrent[index] = np.mean(numSet)
		stdCurrent[index] = np.std(numSet)

		#avg.append(avgCurrent)
		#std.append(stdCurrent)
		#plt.scatter(elapsed,avgCurrent)
		#plt.errorbar(elapsed,avgCurrent, yerr=stdCurrent, fmt=lineSet[index])
		index += 1

	print(avgCurrent)
	print(stdCurrent)

	avg = np.append(avg,avgCurrent,axis=1)
	std = np.append(std,stdCurrent,axis=1)
	#print(avg[0,:].shape)
	#print(avg)
	#print(std[0,:].shape)
	#print(std)

	times = np.append(times,elapsed)
	#print(times.shape)
	p#rint(times)

	ax.clear()
	plt.xlabel('Time [s]')
	plt.ylabel('Signal Level [dBm]')
	plt.errorbar(times[:],avg[0,:], yerr=std[0,:], label="wlan0 (usb)")
	plt.errorbar(times[:],avg[1,:], yerr=std[1,:], label="wlan1 (internal)")
	plt.legend()
	print("\n\n")

	plt.pause(1)
	
			#print(sum(dataSet)/len(dataSet))
	#print(len(dataArray))
	# avgArray = []
	# count = 0;
	# for b in dataArray:
	
	# avg = 	
	# avgArray.append()

	# for i in m:
	# 	#print(i)
	# 	plt.scatter(elapsed,i[1])