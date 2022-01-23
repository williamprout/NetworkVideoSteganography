import cv2
import os
import shutil
import sys
from datetime import datetime
from dcimage import getImageDimensions, stegoEncode, stegoDecode
from dcutils import encryptSecretImage, decryptSecretImage

from multiprocessing import Pool

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
    
def encodeFrame(secretFrame):
    #Encrypting
    cipher = encryptSecretImage("temp/secret/" + secretFrame)

    # Writing to output image
    stegoEncode(cipher, "temp/cover/" + secretFrame, "temp/encoded/%s" % secretFrame)
    # print(secretFrame)

    

def stegoEncodeFrames():
    
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
        pool.map(encodeFrame, secretFrames)
            
        #     threads.append(threading.Thread(target=encodeFrame(secretFrameString)))
        #     threads[-1].start()
            
        # for t in threads:
        #     t.join()
        
        
def decodeFrame(encodedFrame):
    #Encrypting
    cipher = stegoDecode("temp/encoded/%s" % encodedFrame)
    
    decryptSecretImage(cipher)


def stegoDecodeFrames():

    encodedFrames = [img for img in os.listdir('temp/encoded') if img.endswith(".bmp")]
    os.mkdir("temp/secret")
    
    pool = Pool(processes=10)
    pool.map(decodeFrame, encodedFrames)


def setupTempDir():
    os.mkdir("temp/")

def cleanupTempFiles():
    shutil.rmtree("temp/")
            
def main():
    
    mode = sys.argv[1]
    
    if (mode == "encode"):
        setupTempDir()
        cover_fps = videoToImages("cover_test.avi", "cover")
        videoToImages("secret_test.avi", "secret")
        stegoEncodeFrames()
        imagesToVideo("output.avi", "encoded", cover_fps)
        cleanupTempFiles()
    
    if (mode == "decode"):
        setupTempDir()
        encoded_fps = videoToImages("output.avi", "encoded")
        stegoDecodeFrames()
        imagesToVideo("secret_output.avi", "secret", encoded_fps)
        cleanupTempFiles()
        
    if (mode == "clean"):
        cleanupTempFiles()
    
if __name__ == "__main__":
    main()
