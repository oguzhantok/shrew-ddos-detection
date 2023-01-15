#!/usr/bin/python3
import socket
from _thread import *
import time 
from threading import Thread, Lock

lock = Lock()
total_data = 0
bandwidth = 1024*200
HOST = "10.10.10.1"
PORT = 1234

normal_message = "a"
error_message = "error"

#START TO LISTEN
def listen(sock, conn):

    global total_data
    global lock
    check = True
    
    while True:
        if total_data <= bandwidth:
            check = True
            data = conn.recv(1024) 
            if not data:
                continue
            lock.acquire()
            total_data += len(data)
            lock.release()
            conn.send(normal_message.encode('ascii'))
        elif check == True:
            check = False
            conn.send(error_message.encode('ascii'))
    conn.close()

def timer():
    global total_data

    while True:
        time.sleep(1)
        print(f"total_data: {total_data}")
        lock.acquire()
        total_data = 0
        lock.release()
        

    
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((HOST, PORT))
sock.listen()
print("Socket is Listening")

tim = Thread(target=timer)
tim.start()

while True:
    conn, addr = sock.accept()
    print('Connected to :', addr[0], ':', addr[1])
    lis = Thread(target=listen, args=(sock,conn))
    lis.start()
sock.close()
