#Installation of the required packages
install-esp-idf:
	git submodule add https://github.com/espressif/esp-idf.git
	cd esp-idf
	git submodule update --init --recursive
	./install.sh


csi-recv:
	. csi-recv.sh

csi-send:
	. csi-send.sh
