import socket
import os
import time
import main 

from multiprocessing import Pool
from multiprocessing import Process
from multiprocessing import Pipe

from functools import partial

from tkinter import *
from PIL import ImageTk, Image
import shutil

BUFFER_SIZE = 2048

def sendFile(filename, destination, port):
    filesize = os.path.getsize(filename)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("Initiating connection to", destination + ":" + port)
    s.connect((destination, int(port)))
    
    file = open(filename, "rb")
    data = file.read(1024)
    s.send(f"{filename}".encode())
    
    time.sleep(0.2)
    print("Starting file transmission...")
    while (data):
        s.send(data)
        data = file.read(1024)
    
    print("Transmission complete.")
    
    file.close()
    s.close()

def receiveFile(port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('', int(port)))
    print("Waiting for connection...")
    s.listen()

    connection, addr = s.accept()
    print("Received connection from", str(addr[0])+":"+str(addr[1]))
    filename = connection.recv(1024).decode()
    
    with open(filename, "wb") as file:
        while True:
            data = connection.recv(1024)
            while (data):
                file.write(data)
                data = connection.recv(1024)
            if not data:
                file.close()
                break
    
    print("File received successfully:", filename)
    connection.close()


def streamTransmit(destination, port, key):
    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("Initiating connection to", destination + ":" + port)
    s.connect((destination, int(port)))
    
    secretFrames = [img for img in os.listdir('temp/secret') if img.endswith(".bmp")]
    coverFrames = [img for img in os.listdir('temp/cover') if img.endswith(".bmp")]
    
    s.send(str(len(secretFrames)).encode())
    
    secret_pixel_count, cover_pixel_count = main.framesCompatabilityCheck(secretFrames, coverFrames)

    if ((cover_pixel_count / secret_pixel_count) > 8.2):
        print("File compatability check complete!")
        
        os.mkdir("temp/encoded")
        
        blockSize = 10
        last_sent = 0
        
        pool = Pool(processes=blockSize)
        i = 0
        sentCount = 0
        ackCount = 0
        for _ in pool.imap(partial(main.encodeFrame, key=key), secretFrames):
            i+=1
            print("Encoded: %i/%i Sent: %i/%i ACKs: %i/%i" % (i, len(secretFrames), sentCount, len(secretFrames), ackCount, len(secretFrames)), end='\r')
            if i % blockSize == 0:
                last_sent = i 
                for x in range(i-blockSize, i):
                    xstring = str(x).zfill(10)
                    secret_frame = "%s.bmp" % xstring
        
                    file = open("temp/encoded/%s" % secret_frame, "rb")
                    data = file.read(BUFFER_SIZE)

                    while (data):
                        s.send(data)
                        data = file.read(BUFFER_SIZE)
                    sentCount += 1
                    print("Encoded: %i/%i Sent: %i/%i ACKs: %i/%i" % (i, len(secretFrames), sentCount, len(secretFrames), ackCount, len(secretFrames)), end='\r')
                    time.sleep(0.3)
                    s.send(b"<end_file>")

                    ack = s.recv(BUFFER_SIZE)
                    while True:
                        if ack.decode() == xstring:
                            break 
                        else:
                            print("incorrect ACK")
                            ack = s.recv(BUFFER_SIZE)
                    ackCount += 1
                    print("Encoded: %i/%i Sent: %i/%i ACKs: %i/%i" % (i, len(secretFrames), sentCount, len(secretFrames), ackCount, len(secretFrames)), end='\r')
            elif i == len(secretFrames):
                for x in range(last_sent, i):
                    xstring = str(x).zfill(10)
                    secret_frame = "%s.bmp" % xstring
        
                    file = open("temp/encoded/%s" % secret_frame, "rb")
                    data = file.read(BUFFER_SIZE)

                    while (data):
                        s.send(data)
                        data = file.read(BUFFER_SIZE)
                    sentCount += 1
                    print("Encoded: %i/%i Sent: %i/%i ACKs: %i/%i" % (i, len(secretFrames), sentCount, len(secretFrames), ackCount, len(secretFrames)), end='\r')
                    time.sleep(0.3)
                    s.send(b"<end_file>")

                    ack = s.recv(BUFFER_SIZE)
                    while True:
                        if ack.decode() == xstring:
                            break 
                        else:
                            print("incorrect ACK")
                            ack = s.recv(BUFFER_SIZE)
                    ackCount += 1
                    print("Encoded: %i/%i Sent: %i/%i ACKs: %i/%i" % (i, len(secretFrames), sentCount, len(secretFrames), ackCount, len(secretFrames)), end='\r')
        print("Encoded: %i/%i Sent: %i/%i ACKs: %i/%i" % (i, len(secretFrames), sentCount, len(secretFrames), ackCount, len(secretFrames)))
        
        time.sleep(0.2)      
        s.send(b"<end>")
        ack = s.recv(BUFFER_SIZE)
        while True:
            if ack == b"endACK":
                break
            else:
                print("incorrect end ACK")
                ack = s.recv(BUFFER_SIZE)
        s.close()
        
        print("Video stream transmission complete")
        
def receivingProcess(c, port):
    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('', int(port)))
    print("Waiting for connection...")
    s.listen()
    connection, addr = s.accept()
    print("Received connection from", str(addr[0])+":"+str(addr[1]))
    data = connection.recv(BUFFER_SIZE)
    c.send(int(data.decode()))
    count = 0
    complete = False
    while complete == False:
        countString = str(count).zfill(10)
        file_complete = False
        
        with open("temp/encoded/%s.bmp" % countString, "wb") as file:
            while file_complete == False:
                data = connection.recv(BUFFER_SIZE)
                if data == b"<end_file>":
                    file_complete = True
                    file.close()
                    connection.send(countString.encode())
                elif data == b"<end>":
                    break
                else:
                    file.write(data)
        if data == b"<end>":
            os.remove("temp/encoded/%s.bmp" % countString)
            connection.send(b"endACK")
            complete = True
            global endTransmission
            endTransmission = True
        count += 1
    connection.close()
    
def diplayVideoProcess(c):
    waiting = True
    frame = 0
    totalFrames = 0
    while waiting:
        secretFrames = [img for img in os.listdir('temp/secret') if img.endswith(".bmp")]
        encodedFrames = [img for img in os.listdir('temp/encoded') if img.endswith(".bmp")]
        if len(encodedFrames) > 1:
            if totalFrames == 0:
                totalFrames = c.recv()
            print("Received: %i/%i Decoded: %i/%i Displayed %i/%i" % (len(encodedFrames), totalFrames, len(secretFrames), totalFrames, 0, totalFrames), end='\r')
            if len(secretFrames) >= totalFrames*0.85 and len(encodedFrames) != 0:
                waiting = False
    print("Received: %i/%i Decoded: %i/%i Displayed %i/%i" % (len(encodedFrames), totalFrames, len(secretFrames), totalFrames, 0, totalFrames), end='\r')

    print("\nSTARTING VIDEO DISPLAY")

    root = Tk()
    secretFrames = [img for img in os.listdir('temp/secret') if img.endswith(".bmp")]
    image = ImageTk.PhotoImage(image = Image.open("temp/secret/%s" % secretFrames[frame]))
    root.title("Video")
    myLabel = Label(root, image = image)
    myLabel.grid(row = 0)
    def playVideo(frame=0):
        FRAMERATE = 30
        frame_delay = round((1/FRAMERATE)*1000)
        printedEnd = False
        secretFrames = [img for img in os.listdir('temp/secret') if img.endswith(".bmp")]
        encodedFrames = [img for img in os.listdir('temp/encoded') if img.endswith(".bmp")]
        try:
            image = ImageTk.PhotoImage(image = Image.open("temp/secret/%s" % secretFrames[frame]))
            myLabel.configure(image = image)
            myLabel.image = image
            if frame == len(secretFrames)-1 and (len(secretFrames) == len(encodedFrames)):
                shutil.rmtree("temp/")
                print("Received: %i/%i Decoded: %i/%i Displayed %i/%i" % (len(encodedFrames), totalFrames, len(secretFrames), totalFrames, frame+1, totalFrames), end='\r')
                root.quit()
            print("Received: %i/%i Decoded: %i/%i Displayed %i/%i" % (len(encodedFrames), totalFrames, len(secretFrames), totalFrames, frame+1, totalFrames), end='\r')
            root.after(frame_delay, playVideo, frame+1)
        except IndexError:
            root.after(frame_delay, playVideo, frame)
    if frame == 0:
        playVideo()
    root.mainloop()
        
def streamReceive(port, key):
    
    os.mkdir("temp/")
    os.mkdir("temp/encoded")
    os.mkdir("temp/secret")
    pc, cc = Pipe()
    rp = Process(target=receivingProcess, args=(cc, port,))
    rp.start()
    
    dvp = Process(target=diplayVideoProcess, args=(pc,))
    dvp.start()
    
    i = 0
    file_count = 0
    while True:
        encodedFrames = []
        try:
            path, dirs, files = next(os.walk("temp/encoded"))
        except:
            pass
        last_file_count = file_count
        file_count = len(files)
        if file_count >= i + 10:
            for name in range(i,i+10):
                nameString = str(name).zfill(10)
                encodedFrames.append("%s.bmp" % nameString)
            pool = Pool(processes=10)
            for _ in pool.imap(partial(main.decodeFrame, key=key), encodedFrames):
                time.sleep(0.2)
            i += 10
        elif file_count == i and i != 0:
            break
        elif last_file_count == file_count and file_count > i and i != 0:
            for name in range(i,file_count):
                nameString = str(name).zfill(10)
                encodedFrames.append("%s.bmp" % nameString)
            pool = Pool(processes=10)
            for _ in pool.imap(partial(main.decodeFrame, key=key), encodedFrames):
                time.sleep(0.2)
            i += file_count-i
    dvp.join()
    
    print("\nVideo stream diplay complete")