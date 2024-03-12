install enviroonment :
	python3 -m venv .env && pip install -r requirements.txt && pip install --upgrade pip && source .env/bin/activate


erase esp32 S3: #Make sure to change the port to the correct one
	esptool.py --port /dev/ttyUSB0 erase_flash


flash esp32 S3: #Make sure to change the port and the .bin name to the correct one
	#link to download the .bin file: https://micropython.org/download/ESP32_GENERIC_S3/
	esptool.py --chip esp32 --port /dev/ttyUSB0 write_flash -z 0x1000 esp32-idf3-20200902-v1.13.bin

ampy command : #Make sure to change the port to the correct one
	ampy --port /dev/ttyUSB0 ls


#You can use all the following commands :
# ampy --port /dev/ttyUSB0 put namefile.py to send a file into the esp32
# ampy --port /dev/ttyUSB0 get namefile.py to get a file from the esp32
# ampy --port /dev/ttyUSB0 run namefile.py to run a file from the esp32
# ampy --port /dev/ttyUSB0 rm namefile.py to remove a file from the esp32
# ampy --port /dev/ttyUSB0 mkdir namefile.py to create a directory in the esp32
# ampy --port /dev/ttyUSB0 rmdir namefile.py to remove a directory from the esp32
# ampy --port /dev/ttyUSB0 reset to reset the esp32