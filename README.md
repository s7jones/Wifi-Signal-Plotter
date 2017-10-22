# Wifi-Signal-Plotter
Simple example Python script for comparing Wifi Signal strength between Wifi adaptors in Linux, Windows, or Mac <sup>1</sup>.

<img src="ExamplePlotInLinux.png" height="250">

Tested on Python 3.4/3.5

Requirements:
  - subprocess module
  - numpy and matplotlib libraries

Footnotes:
  1. Mac support is untested. It will plot one interface using the airport command and will identify that interface with the SSID of the Wifi network it is connected to.