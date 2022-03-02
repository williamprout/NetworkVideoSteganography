from pydoc import plain
import cv2
import os
import shutil
import sys
from datetime import datetime
from dcimage import getImageDimensions, stegoEncode, stegoDecode
from dcutils import encryptSecretImage, decryptSecretImage
from dnacryptograpy import DNAencrypt, DNAdecrypt
from multiprocessing import Pool
from networking import sendFile, receiveFile
from functools import partial

def videoToImages(videoFile, type):
    start = datetime.now()
    vidcap = cv2.VideoCapture(videoFile)
    fps = vidcap.get(cv2.CAP_PROP_FPS)
    success, image = vidcap.read()
    count = 0
    # shutil.rmtree("temp/" + type)
    os.mkdir("temp/"+ type)

    while success:
        countString = str(count).zfill(10)
        # save frame as JPEG file
        cv2.imwrite("temp/" + type + "/%s.bmp" % countString, image)
        success, image = vidcap.read()
        # print('Read a new frame: ', success)
        count += 1
    print("Video-to-Image conversion took: " + str(datetime.now() - start))
    return fps
    
def imagesToVideo(video_name, type, fps):
    fourcc = cv2.VideoWriter_fourcc(*'FFV1')

    image_folder = 'temp/' + type
    # video_name = 'output.avi'

    images = [img for img in os.listdir(image_folder) if img.endswith(".bmp")]
    frame = cv2.imread(os.path.join(image_folder, images[0]))
    height, width, layers = frame.shape

    video = cv2.VideoWriter(video_name, fourcc, fps, (width, height))


    for image in images:
        # print(image)
        video.write(cv2.imread(os.path.join(image_folder, image)))

    cv2.destroyAllWindows()
    video.release()
    
def encodeFrame(secretFrame, key):
    #Encrypting
    cipher = encryptSecretImage("temp/secret/" + secretFrame, key)

    # Writing to output image
    stegoEncode(cipher, "temp/cover/" + secretFrame, "temp/encoded/%s" % secretFrame)
    # print(secretFrame)

    

def stegoEncodeFrames(key):
    
    # shutil.rmtree("temp/encoded")
    
    secretFrames = [img for img in os.listdir('temp/secret') if img.endswith(".bmp")]
    coverFrames = [img for img in os.listdir('temp/cover') if img.endswith(".bmp")]
    
    #TODO ensure that they are more cover frames than secret frames
    
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
        print("First cover fmage could not be read.")
        print(coverFrames[0])

    if ((cover_pixel_count / secret_pixel_count) > 8.2):
        print("Frame sizes compatible, cover frame is", str(
            cover_pixel_count / secret_pixel_count), 'times larger than the secret frame.')
        
        os.mkdir("temp/encoded")

        # frameNumber = 0
        threads = []
        # for secretFrame in secretFrames:
        # secretFrameString = str(secretFrame)
        # print(secretFrameString)
        
        pool = Pool(processes=10)
        pool.map(partial(encodeFrame, key=key), secretFrames)
            
        #     threads.append(threading.Thread(target=encodeFrame(secretFrameString)))
        #     threads[-1].start()
            
        # for t in threads:
        #     t.join()
        
        
def decodeFrame(encodedFrame, key):
    #Encrypting
    cipher = stegoDecode("temp/encoded/%s" % encodedFrame)
    
    decryptSecretImage(cipher, key)


def stegoDecodeFrames(key):

    encodedFrames = [img for img in os.listdir('temp/encoded') if img.endswith(".bmp")]
    os.mkdir("temp/secret")
    
    pool = Pool(processes=10)
    pool.map(partial(decodeFrame, key=key), encodedFrames)


def setupTempDir():
    os.mkdir("temp/")

def cleanupTempFiles():
    shutil.rmtree("temp/")
            
def main():
    
    mode = sys.argv[1]
    
    if (mode == "encode"):
        # global key 
        key = int(sys.argv[2])
        start = datetime.now()
        setupTempDir()
        cover_fps = videoToImages("cover_test.avi", "cover")
        videoToImages("secret_test.avi", "secret")
        stegoEncodeFrames(key)
        imagesToVideo("output.avi", "encoded", cover_fps)
        cleanupTempFiles()
        print("Encoding run took: " + str(datetime.now() - start))
    
    if (mode == "decode"):
        key = int(sys.argv[2])
        setupTempDir()
        encoded_fps = videoToImages("output.avi", "encoded")
        stegoDecodeFrames(key)
        imagesToVideo("secret_output.avi", "secret", encoded_fps)
        cleanupTempFiles()
        
    if (mode == "clean"):
        cleanupTempFiles()
        
    # if (mode == "dnatest"):
    #     with open("encrypttest.bmp", "rb") as image:
    #         #Read image data in binary
    #         # print("Reading secret image...")
    #         secret_image_bytes = bytes(image.read())
    #         image.close()
    #         secret_image_name_bytes = str.encode("encrypttest.bmp")
    #         payload = secret_image_name_bytes + secret_image_bytes
            
    #     final_payload = payload
    #     final_final_payload = bin(int.from_bytes(final_payload, byteorder=sys.byteorder))[2:]
    #     print(final_final_payload[0:50])
    #     cipher = DNAencrypt(1, final_final_payload)
    #     # print(cipher[0:50])
    #     decrypted = DNAdecrypt(1, cipher)
    #     # print(decrypted[0:50])
    #     # print(final_final_payload[-50:])
    #     # print(decrypted[-50:])
        
    #     # print(len(final_final_payload))
    #     # print(len(cipher))
    #     # print(len(decrypted))
    #     if final_final_payload == decrypted:
    #         print("SUCCESSFUL")
            
    #     decrypted_raw = int(decrypted, 2)
        
    #     if final_payload == decrypted_raw:
    #         print("SUCCESSFUL2")
        
    #     # filename = (decrypted[0:(decrypted.rfind(bytes('.bmp', 'utf-8')) + 4)]).decode('utf-8')
    #     # plaintext = decrypted[(decrypted.rfind(bytes('.bmp', 'utf-8')) + 4):]
    #     # print(filename)
    #     # print(plaintext)
        
    if (mode == "receive"):
        port = sys.argv[2]
        receiveFile(port)

    if (mode == "send"):
        file = sys.argv[2]
        address = sys.argv[3]
        port = sys.argv[4]
        sendFile(file, address, port)
        
if __name__ == "__main__":
    main()
