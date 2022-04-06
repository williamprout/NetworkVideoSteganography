import cv2
import os
import shutil
import sys
from datetime import datetime
from framesteganography import getImageDimensions, stegoEncode, stegoDecode
from framecryptography import encryptSecretImage, decryptSecretImage
from dnacryptograpy import DNAencrypt, DNAdecrypt
from multiprocessing import Pool
import networking
from functools import partial
import tqdm

def videoToImages(videoFile, type):
    if videoFile.endswith(".avi"):
        start = datetime.now()
        vidcap = cv2.VideoCapture(videoFile)
        fps = vidcap.get(cv2.CAP_PROP_FPS)
        success, image = vidcap.read()
        count = 0
        os.mkdir("temp/"+ type)

        while success:
            countString = str(count).zfill(10)
            # save frame as JPEG file
            cv2.imwrite("temp/" + type + "/%s.bmp" % countString, image)
            success, image = vidcap.read()
            count += 1
        return fps
    else:
        cleanupTempFiles()
        sys.exit("Incompatible video type. Must be .avi format.")
    
def imagesToVideo(video_name, type, fps):
    fourcc = cv2.VideoWriter_fourcc(*'FFV1')

    image_folder = 'temp/' + type

    images = [img for img in os.listdir(image_folder) if img.endswith(".bmp")]
    frame = cv2.imread(os.path.join(image_folder, images[0]))
    height, width, layers = frame.shape

    video = cv2.VideoWriter(video_name, fourcc, fps, (width, height))


    for image in images:
        video.write(cv2.imread(os.path.join(image_folder, image)))

    cv2.destroyAllWindows()
    video.release()
    
def encodeFrame(secretFrame, key):
    #Encrypting
    cipher = encryptSecretImage("temp/secret/" + secretFrame, key)

    # Writing to output image
    stegoEncode(cipher, "temp/cover/" + secretFrame, "temp/encoded/%s" % secretFrame)

def framesCompatabilityCheck(secretFrames, coverFrames):
    if len(secretFrames) > len(coverFrames):
        cleanupTempFiles()
        sys.exit("Secret video is longer than cover video.")
    
    try:
        secret_width, secret_height = getImageDimensions("temp/secret/" + secretFrames[0])
        secret_pixel_count = secret_width * secret_height
    except:
        print("First secret frame could not be read.")
        print(secretFrames[0])

    try:
        cover_width, cover_height = getImageDimensions("temp/cover/" + coverFrames[0])
        cover_pixel_count = cover_width * cover_height
    except:
        print("First cover frame could not be read.")
        print(coverFrames[0])
        
    return secret_pixel_count, cover_pixel_count

def stegoEncodeFrames(key):
    secretFrames = [img for img in os.listdir('temp/secret') if img.endswith(".bmp")]
    coverFrames = [img for img in os.listdir('temp/cover') if img.endswith(".bmp")]
    
    secret_pixel_count, cover_pixel_count = framesCompatabilityCheck(secretFrames, coverFrames)

    if ((cover_pixel_count / secret_pixel_count) > 8.2):
        if (len(secretFrames) <= len(coverFrames)):
            print("File compatability check complete!")
            
            os.mkdir("temp/encoded")
            
            threads = []
            
            print("Frame Encoding Progress:")
            
            pool = Pool(processes=10)
            for _ in tqdm.tqdm(pool.imap(partial(encodeFrame, key=key), secretFrames), total=len(secretFrames)):
                pass
                
        else:
            cleanupTempFiles()
            sys.exit("Video lengths incompatable. Cover video must be longer than the secret video.")
    else:
        cleanupTempFiles()
        sys.exit("Frame sizes incompatable. Cover video must be 8 times the resolution of the secret video.")
        
        
def decodeFrame(encodedFrame, key):
    #Encrypting
    cipher = stegoDecode("temp/encoded/%s" % encodedFrame)
    
    decryptSecretImage(cipher, key)
    

def stegoDecodeFrames(key):

    encodedFrames = [img for img in os.listdir('temp/encoded') if img.endswith(".bmp")]
    os.mkdir("temp/secret")
    
    print("Frame Decoding Progress:")
    
    pool = Pool(processes=10)
    for _ in tqdm.tqdm(pool.imap(partial(decodeFrame, key=key), encodedFrames), total=len(encodedFrames)):
        pass


def setupTempDir():
    os.mkdir("temp/")

def cleanupTempFiles():
    shutil.rmtree("temp/")
            
def main():
    
    mode = sys.argv[1]
    
    if (mode == "encode"):
        #py main.py encode cover_test.avi secret_test.avi 1 output.avi
        cover = sys.argv[2]
        secret = sys.argv[3]
        key = int(sys.argv[4])
        output = sys.argv[5]
        
        start = datetime.now()
        setupTempDir()
        cover_fps = videoToImages(cover, "cover")
        videoToImages(secret, "secret")
        stegoEncodeFrames(key)
        imagesToVideo(output, "encoded", cover_fps)
        cleanupTempFiles()
        print("Encoding run took: " + str(datetime.now() - start))
    
    if (mode == "decode"):
        #py main.py decode output.avi 1 secret_output.avi
        encoded_file = sys.argv[2]
        key = int(sys.argv[3])
        output = sys.argv[4]
        
        setupTempDir()
        encoded_fps = videoToImages(encoded_file, "encoded")
        stegoDecodeFrames(key)
        imagesToVideo(output, "secret", encoded_fps)
        cleanupTempFiles()
        
    if (mode == "clean"):
        #py main.py clean
        cleanupTempFiles()
        
    if (mode == "receive"):
        #py main.py receive <destination port>
        port = sys.argv[2]
        
        networking.receiveFile(port)

    if (mode == "send"):
        #py main.py send <file> <destination ip address> <destination port>
        file = sys.argv[2]
        address = sys.argv[3]
        port = sys.argv[4]
        
        networking.sendFile(file, address, port)
        
    if (mode == "transmit_stream"):
        #py main.py transmit_stream <secret video> <cover video> <destination ip address> <destination port> <encryption key>
        secret = sys.argv[2]
        cover = sys.argv[3]
        address = sys.argv[4]
        port = sys.argv[5]
        key = int(sys.argv[6])
        
        setupTempDir()
        cover_fps = videoToImages(cover, "cover")
        videoToImages(secret, "secret")
        networking.streamTransmit(address, port, key)
        cleanupTempFiles()
        
    if (mode == "receive_stream"):
        #py main.py receive_stream <destination port> <encryption key>
        port = sys.argv[2]
        key = int(sys.argv[3])
        
        networking.streamReceive(port, key)

        
if __name__ == "__main__":
    main()