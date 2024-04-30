import sys
import csv
import re
import argparse
import serial
from os import path
from os import mkdir
from io import StringIO
from PyQt5.Qt import *
import base64
import time
from datetime import datetime
from multiprocessing import Process, Queue
import signal as signal_key

#Pour la partie IA
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import warnings
import ast
warnings.filterwarnings('ignore')
from gen_dataset import d, d2, d3
from sklearn import tree
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split


def train_model():
    #isolation du vecteur "data" de taille 109
    X = pd.concat([d, d2, d3])['data'].apply(ast.literal_eval)
    X_data = np.array([np.array(x) for x in X])
    X_data = np.vstack(X_data)


    #version avec le rssi
    X_rssi = pd.concat([d, d2, d3])[['rssi']]

    #creation des étiquettes
    y = pd.concat([d, d2, d3])['State']


    #split des données de tests, 70% pour l'entrainement, 30% pour les tests
    X_train, X_test, y_train, y_test = train_test_split(X_data, y, train_size=0.7, random_state=0)

    #on force l'arbre à n'avoie qu'une profondeur de 15 pour éviter que l'IA apprenne le jeu par coeur
    clf = tree.DecisionTreeClassifier(criterion='entropy', max_depth=15)
    clf.fit(X_train, y_train)


    # Afficher l'arbre
    plt.figure(figsize=(10,10))
    tree.plot_tree(clf, class_names=['1', '0', '-1'], filled=True)
    plt.show()

    # prédiction test et affichage du score de réussite
    y_pred = clf.predict(X_test)

    print("Train data accuracy:",round(100*accuracy_score(y_true = y_train, y_pred=clf.predict(X_train)),3),"%")
    print("Test data accuracy:","%.3f" %(100*accuracy_score(y_true = y_test, y_pred=y_pred)),"%")

    return clf





CSI_DATA_COLUMNS_NAMES = ["type", "seq", "timestamp", "taget_seq", "taget", "mac", "rssi", "rate", "sig_mode", "mcs",
                          "cwb", "smoothing", "not_sounding", "aggregation", "stbc", "fec_coding","sgi", "noise_floor",
                          "ampdu_cnt", "channel_primary", "channel_secondary", "local_timestamp", "ant", "sig_len",
                          "rx_state", "len", "first_word_invalid", "data"]

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


def command_router_connect(queue_write, queue_read):
    command = "wifi_config --ssid " + ("\"%s\"" % "iPhone A") + " --password " + 'testtest'
    print(f"command_router_connect: {command}")
    ser.write(command)
    time.sleep(1)


def serial_handle(queue_read, queue_write, port, clf):
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

    folder_list = ['log']
    for folder in folder_list:
        if not path.exists(folder):
            mkdir(folder)

    data_valid_list = pd.DataFrame(columns=['type', 'columns_names', 'file_name', 'file_fd', 'file_writer'],
                                   data=[["CSI_DATA", CSI_DATA_COLUMNS_NAMES, "log/csi_data.csv", None, None],
                                         ])

    for data_valid in data_valid_list.iloc:
        data_valid['file_fd'] = open(data_valid['file_name'], 'w')
        data_valid['file_writer'] = csv.writer(data_valid['file_fd'])
        data_valid['file_writer'].writerow(data_valid['columns_names'])

    taget_last = 'unknown'
    taget_seq_last = 1000

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
                        print(clf.predict([data_series['data']]))

                        data_series['taget'] = 'someone'

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

                        queue_read.put(data_series)
                    else:
                        queue_read.put(data_series)

                    data_valid['file_writer'].writerow(data_series.astype(str))
                    data_valid['file_fd'].flush()
                    break
        else:
            strings = re.sub(r'\\x1b.*?m', '', strings)

            log = re.match(r'.*([DIWE]) \((\d+)\) (.*)', strings, re.I)

            if not log:
                continue

            data_series = pd.Series(index=['type', 'tag', 'timestamp', 'data'],
                                    data=['LOG_DATA', log.group(1), log.group(2), log.group(3)])
            if not queue_read.full():
                queue_read.put(data_series)




if __name__ == '__main__':

    clf = train_model()




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
        serial_queue_read, serial_queue_write, serial_port, clf))
    print(f"serial_handle_process: {serial_handle_process}")
    serial_handle_process.start()



    serial_handle_process.join()
