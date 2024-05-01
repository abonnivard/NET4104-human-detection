cd esp-idf
. ./export.sh

cd ../esp-csi/examples/esp-radar/console_test
idf.py set-target esp32s3


#port à changer
idf.py flash -b 921600 -p /dev/cu.usbserial-2130