#!/usr/bin/python3
import socket, time
from threading import Thread, Lock
import random

BASE = 20
normal_counter = 0
error_counter = 0
packet_count = BASE

lock = Lock()


def connection():
        global normal_counter, error_counter, packet_count
        HOST = '10.10.10.1'
        PORT = 1234

        sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        sock.connect((HOST, PORT))

        message = "0" * 1024

        #client'ın saldırısız ne kadar yolladığını hesapla 9k-11k mesela

        while True:
                try:
                        if packet_count <= 0:
                                continue
                        sock.send(message.encode('ascii'))
                        data = str(sock.recv(1024).decode("ascii"))
                        if "a" not in data:
                                lock.acquire()
                                error_counter += 1
                                packet_count -= 1
                                lock.release()
                        else:
                                lock.acquire()
                                normal_counter += 1
                                packet_count -= 1
                                lock.release()
                except socket.error as e:
                                sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
                                sock.connect((HOST, PORT))
        sock.close()

def timer():
    global normal_counter, error_counter, packet_count, BASE

    while True:
        time.sleep(1)
        print(f"Usage Percentage: %{round(((normal_counter / BASE) * 100), 2)}")
        lock.acquire()
        normal_counter = 0
        error_counter = 0
        #rand  = [-2, -1, 0, 1, 2][random.randrange(5)]
        #rand  = [-6,-5,-4,-3,-2, -1, 0, 1, 2,3,4,5,6][random.randrange(13)]
        rand  = [-10, -9, -8, -7, -6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6, 7][random.randrange(18)]
        #rand = -10
        packet_count = BASE + rand
        lock.release()

lis = Thread(target=connection)
tim = Thread(target=timer)
tim.start()
lis.start()
