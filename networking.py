import socket
import os
import time

BUFFER_SIZE = 1024


def sendFile(filename, destination, port):
    filesize = os.path.getsize(filename)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("Initiating connection to", destination + ":" + port)
    s.connect((destination, int(port)))
    
    file = open(filename, "rb")
    data = file.read(BUFFER_SIZE)
    s.send(f"{filename}".encode())
    
    time.sleep(0.2)
    print("Starting file transmission...")
    while (data):
        s.send(data)
        data = file.read(BUFFER_SIZE)
    
    print("Transmission complete.")
    
    file.close()
    s.close()

def receiveFile(port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('', int(port)))
    print("Waiting for connection...")
    s.listen()

    connection, addr = s.accept()
    print("Received connection from", addr[0]+":"+addr[1])
    filename = connection.recv(BUFFER_SIZE).decode()
    
    with open(filename, "wb") as file:
        while True:
            data = connection.recv(BUFFER_SIZE)
            while (data):
                file.write(data)
                data = connection.recv(BUFFER_SIZE)
            if not data:
                file.close()
                break
    
    print("File received successfully:", filename)
    connection.close()