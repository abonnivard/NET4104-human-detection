#Installation of the required packages
install-esp-idf:
	cd esp-idf
	git checkout v5.0.2
	git submodule update --init --recursive
	./install.sh


csi-recv:
	. csi-recv.sh
