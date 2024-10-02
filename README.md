
---

# MW2012 PS3 to PC Endian Converter

## Overview
This tool converts Genesis Objects and Types from *Need for Speed: Most Wanted (2012)* on PlayStation 3 to PC by handling endian differences

## Features
- **Endian Conversion**: Correctly converts Select PS3 Genesis Objects and Types to PC format
- **Simple Usage**: Easy to use GUI with Log.

## How to Download
1. Download the latest Release
2. Unzip and Run main.exe

## How to Build Project
1. Clone the repository.
   ```bash
   git clone https://github.com/peterlototsky/MW2012-PS3-To-PC-Endian-Converter.git
   ```
2. Setup Venv:
   cd to folder
   ```bash
   python3 -m venv .venv     
   ```
3. Install Packages:
   cd to project folder
   ```bash
   pip install pyqt5  
   ```
4. Run pyinstaller
   ```bash
   pyinstaller main.py
   ```
   > **Note:** Make sure that python is installed and is on the system path

## Requirements
- Python 3.12.x

---
