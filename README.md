# Wifi-Signal-Plotter
Simple example Python script for comparing Wifi Signal strength between Wifi adaptors in Linux or Windows.

<img src="ExamplePlotInLinux.png" height="250">

How to run:
  - From Python Shell:
  ```python
  >>> import WifiSignalPlotter
  >>> WifiSignalPlotter.main()
  ```
  - Windows:
  ```
  python.exe WifiSignalPlotter.py
  ```
  - Linux (Ubuntu/Linux Mint):
  ```
  chmod +x WifiSignalPlotter.py
  python3.5 WifiSignalPlotter.py
  ```

Tested on: 
  - Windows and Linux.
  - Python 3.4/3.5.

Requirements:
  - subprocess module.
  - numpy and matplotlib libraries.
