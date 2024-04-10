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

gui-python:
	cd esp-csi/examples/console_test/tools
    # Install python related dependencies
	pip install -r requirements.txt
    # Graphical display
	python esp_csi_tool.py -p /dev/ttyUSB1
