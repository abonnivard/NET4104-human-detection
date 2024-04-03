cd esp-idf
#./install.sh
. ./export.sh

cd ../csi_send
idf.py set-target esp32s3
idf.py flash -b 921600 -p /dev/ttyUSB0 monitor