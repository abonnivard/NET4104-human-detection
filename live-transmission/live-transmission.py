import sys
import csv
import re
import argparse
import pandas as pd

import serial
from os import path
from os import mkdir
from io import StringIO

from PyQt5.Qt import *
from pyqtgraph import PlotWidget
from PyQt5 import QtCore
import pyqtgraph as pq

from PyQt5.QtCore import QDate, QDate, QTime, QDateTime

import threading
import base64
import time
from datetime import datetime
from multiprocessing import Process, Queue

from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
# from PyQt5.QtChart import QChart, QLineSeries,QValueAxis

from scipy import signal
import signal as signal_key
# Paramètres de la connexion série
port = '/dev/cu.usbserial-2130'  # Modifier en fonction du port utilisé par votre ESP32S3
baudrate = 115200  # Vitesse de communication de votre ESP32S3

# Commande pour démarrer la capture CSI
start_capture_command = b'START_CAPTURE\r\n'

CSI_DATA_COLUMNS_NAMES = ["type", "seq", "timestamp", "taget_seq", "taget", "mac", "rssi", "rate", "sig_mode", "mcs",
                          "cwb", "smoothing", "not_sounding", "aggregation", "stbc", "fec_coding","sgi", "noise_floor",
                          "ampdu_cnt", "channel_primary", "channel_secondary", "local_timestamp", "ant", "sig_len",
                          "rx_state", "len", "first_word_invalid", "data"]

CSI_DATA_TARGETS = ["unknown", "train", "none", "someone", "static", "move", "front",
                    "after", "left", "right", "go", "jump", "sit down", "stand up", "climb up", "wave", "applause"]
RADAR_DATA_COLUMNS_NAMES = ["type", "seq", "timestamp", "waveform_wander", "waveform_wander_threshold",
                            "someone_status", "waveform_jitter", "waveform_jitter_threshold", "move_status"]
DEVICE_INFO_COLUMNS_NAMES = ["type", "seq", "timestamp", "mac", "rssi", "rate", "sig_mode", "mcs",
                             "cwb", "smoothing", "not_sounding", "aggregation", "stbc", "fec_coding","sgi", "noise_floor",
                             "ampdu_cnt", "channel_primary", "channel_secondary", "local_timestamp", "ant", "sig_len",
                             "rx_state", "len", "first_word_invalid", "data"]

def serial_handle(queue_read, queue_write, port):
    try:
        ser = serial.Serial(port=port, baudrate=2000000,
                            bytesize=8, parity='N', stopbits=1, timeout=0.1)
    except Exception as e:
        #print(f"serial_handle: {e}")
        data_series = pd.Series(index=['type', 'data'],
                                data=['FAIL_EVENT', "Failed to open serial port"])
        queue_read.put(data_series)
        sys.exit()
        return

    print("open serial port: ", port)

    # Wait a second to let the port initialize
    ser.flushInput()

    folder_list = ['log', 'data']
    for folder in folder_list:
        if not path.exists(folder):
            mkdir(folder)

    data_valid_list = pd.DataFrame(columns=['type', 'columns_names', 'file_name', 'file_fd', 'file_writer'],
                                   data=[["CSI_DATA", CSI_DATA_COLUMNS_NAMES, "log/csi_data.csv", None, None],
                                         ["RADAR_DADA", RADAR_DATA_COLUMNS_NAMES, "log/radar_data.csv", None, None],
                                         ["DEVICE_INFO", DEVICE_INFO_COLUMNS_NAMES, "log/device_info.csv", None, None]])

    for data_valid in data_valid_list.iloc:
        data_valid['file_fd'] = open(data_valid['file_name'], 'w')
        data_valid['file_writer'] = csv.writer(data_valid['file_fd'])
        data_valid['file_writer'].writerow(data_valid['columns_names'])

    log_data_writer = open("log/log_data.txt", 'w+')
    taget_last = 'unknown'
    taget_seq_last = 0

    time.sleep(0.01)

    while True:
        if not queue_write.empty():
            command = queue_write.get()

            if command == "exit":
                sys.exit()
                break

            command = command + "\r\n"
            ser.write(command.encode('utf-8'))
            #print(f"{datetime.now()}, serial write: {command}")
            continue
        try:
            #print(str(ser.readline()))
            strings = str(ser.readline())
            if not strings:
                continue
        except Exception as e:
            data_series = pd.Series(index=['type', 'data'],
                                    data=['FAIL_EVENT', "Failed to read serial"])
            queue_read.put(data_series)
            sys.exit()

        strings = strings.lstrip('b\'').rstrip('\\r\\n\'')
        if not strings:
            continue

        for data_valid in data_valid_list.iloc:
            index = strings.find(data_valid['type'])
            if index >= 0:
                strings = strings[index:]
                csv_reader = csv.reader(StringIO(strings))
                data = next(csv_reader)

                if len(data) == len(data_valid['columns_names']):
                    data_series = pd.Series(
                        data, index=data_valid['columns_names'])

                    try:
                        datetime.strptime(
                            data_series['timestamp'], '%Y-%m-%d %H:%M:%S.%f')
                    except Exception as e:
                        data_series['timestamp'] = datetime.now().strftime(
                            '%Y-%m-%d %H:%M:%S.%f')[:-3]
                        # print(e)

                    if data_series['type'] == 'CSI_DATA':
                        try:
                            # csi_raw_data = json.loads(data_series['data'])
                            csi_raw_data = base64_decode_bin(
                                data_series['data'])
                            if len(csi_raw_data) != int(data_series['len']):
                                # if len(csi_raw_data) != 104 and len(csi_raw_data) != 216 and len(csi_raw_data) != 328 and len(csi_raw_data) != 552:
                                print(
                                    f"CSI_DATA, expected: {data_series['len']}, actual: {len(csi_raw_data)}")
                                break
                        except Exception as e:
                            print(
                                f"json.JSONDecodeError: {e}, data: {data_series['data']}")
                            break

                        data_series['data'] = csi_raw_data
                        print(data_series['data'])
                        print(len(data_series['data']))

                        if data_series['taget'] != 'unknown':
                            if data_series['taget'] != taget_last or data_series['taget_seq'] != taget_seq_last:
                                folder = f"data/{data_series['taget']}"
                                if not path.exists(folder):
                                    mkdir(folder)

                                csi_target_data_file_name = f"{folder}/{datetime.now().strftime('%Y-%m-%d_%H-%M-%S-%f')[:-3]}_{data_series['len']}_{data_series['taget_seq']}.csv"
                                csi_target_data_file_fd = open(
                                    csi_target_data_file_name, 'w+')
                                taget_data_writer = csv.writer(
                                    csi_target_data_file_fd)
                                taget_data_writer.writerow(data_series.index)

                            taget_data_writer.writerow(
                                data_series.astype(str))

                        taget_last = data_series['taget']
                        taget_seq_last = data_series['taget_seq']

                        if queue_read.full():
                            print('============== queue_full ==========')
                            pass
                        else:
                            queue_read.put(data_series)
                    else:
                        queue_read.put(data_series)

                    data_valid['file_writer'].writerow(data_series.astype(str))
                    data_valid['file_fd'].flush()
                    break
        else:
            strings = re.sub(r'\\x1b.*?m', '', strings)
            log_data_writer.writelines(strings + "\n")

            log = re.match(r'.*([DIWE]) \((\d+)\) (.*)', strings, re.I)

            if not log:
                continue

            data_series = pd.Series(index=['type', 'tag', 'timestamp', 'data'],
                                    data=['LOG_DATA', log.group(1), log.group(2), log.group(3)])
            if not queue_read.full():
                queue_read.put(data_series)


# Fonction pour se connecter à un réseau Wi-Fi
def connect_wifi(ssid, password):
    try:
        # Envoi de la commande pour connecter l'ESP32 à un réseau Wi-Fi
        command = f'wifi_config --ssid "{ssid}" --password {password}\r\n'
        command_bytes = command.encode('utf-8')
        ser.write(command_bytes)
        print("Commande de connexion Wi-Fi envoyée")

    except SerialException as e:
        print("Erreur de communication série:", e)


# Fonction pour décoder les données CSI reçues
def base64_decode_bin(str_data):
    try:
        bin_data = base64.b64decode(str_data)
    except Exception as e:
        print(f"Exception: {e}, data: {str_data}")
        return None

    list_data = list(bin_data)

    for i in range(len(list_data)):
        if list_data[i] > 127:
            list_data[i] = list_data[i] - 256

    return list_data

# Fonction pour recevoir les données CSI
def receive_csi_data():
    try:
        # Envoyer la commande de démarrage de la capture
        ser.write(start_capture_command)
        print("Commande de démarrage de la capture envoyée")

        # Attendre un certain temps pour que les données CSI soient collectées
        time.sleep(5)  # Attendre 5 secondes (ajuster si nécessaire)

        while True:
            line = ser.readline()
            if line:
                print("Données CSI reçues (brutes):", line)

                # Décodage des données CSI en base64
                decoded_data = base64_decode_bin(line)
                if decoded_data is not None:
                    print("Données CSI décodées:", decoded_data)
                    print("Nombre de données CSI:", len(decoded_data))
            time.sleep(0.1)

    except SerialException as e:
        print("Erreur de communication série:", e)

    finally:
        # Fermer la connexion série
        ser.close()
        print("Connexion série fermée")

if __name__ == '__main__':
    if sys.version_info < (3, 6):
        print(" Python version should >= 3.6")
        exit()

    parser = argparse.ArgumentParser(
        description="Read CSI data from serial port and display it graphically")
    parser.add_argument('-p', '--port', dest='port', action='store', required=True,
                        help="Serial port number of csv_recv device")

    args = parser.parse_args()
    serial_port = args.port

    serial_queue_read = Queue()
    serial_queue_write = Queue()

    signal_key.signal(signal_key.SIGINT, quit)
    signal_key.signal(signal_key.SIGTERM, quit)

    serial_handle_process = Process(target=serial_handle, args=(
        serial_queue_read, serial_queue_write, serial_port))
    print(f"serial_handle_process: {serial_handle_process}")
    serial_handle_process.start()



    serial_handle_process.join()
