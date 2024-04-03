cd esp-idf
#./install.sh
. ./export.sh

cd ../csi_send
idf.py set-target esp32s3

#remplace /dev/ttyUSB0 par le port de votre ESP32S3
idf.py flash -b 921600 -p /dev/ttyUSB0 monitor