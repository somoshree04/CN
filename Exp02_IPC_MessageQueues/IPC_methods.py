
import netpack as npk
import time

def write_to(container, arr):
    print("P1 has been started")
    for data in arr:
        container=npk.write_queue(container, data)
        print("Printing from P1 & write Data = {}".format(data))

def read_from(container):
    print("P2 has been started")
    time.sleep(1)
    while True:
        data = npk.read_queue(container)
        if data is not None:
            print('Printing from P2 & read Data = {}'.format(data))
        else:
            break

def write_read(container, arr):
    print("P3 has been started")
    for data in arr:
        container=npk.write_queue(container, data)
        print("Printing from P3 & write Data = {}".format(data))
    print('[=] Reading in P3 & data is {}'.format(container.get()))

def read_write(container):
    print("P4 has been started")
    time.sleep(1)
    while True:
        data = npk.read_queue(container)
        if data is not None:
            print('Printing from P4 & read Data = {}'.format(data))
        else:
            break
    
    container = npk.write_queue(container, 1000)
    data = npk.read_queue(container)
    if data is not None:
        print('[=] Writing in P4 & the data is {}'.format(data))