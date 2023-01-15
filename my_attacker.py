#!/usr/bin/python3                
import socket, time

HOST = '10.10.10.1'
PORT = 1234

sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
sock.connect((HOST, PORT))

burst = 0.05
period = 1
sleep_time = period - burst

def send_burst(sock, burst):
    start = time.time()
    data = '0' * 50

    while time.time() - start < burst:
        try:
            sock.send(data.encode('ascii'))
#            data = str(sock.recv(1024).decode("ascii"))
#            if "a" not in data:
#                print('Received from the server :',data)
        except socket.error as e:
            print(e)

while True:
    send_burst(sock, burst)
    sleep_len = period - burst
    time.sleep(sleep_time)
