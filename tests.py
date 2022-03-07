from os import mkdir
import unittest
import sys
import shutil
from dnacryptograpy import DNAencrypt, DNAdecrypt
from main import setupTempDir, cleanupTempFiles, videoToImages, imagesToVideo, stegoEncodeFrames, stegoDecodeFrames
import filecmp


class Testing(unittest.TestCase):
    # def test_cryptography(self):
    #     print("\nTEST 1 - Cryptography")
    #     image_path = "test_files/secret_test.bmp"
    #     key = 1
        
    #     with open(image_path, "rb") as image:
    #         secret_image_bytes = bytes(image.read())
    #         image.close()
    #         secret_image_name_bytes = str.encode(image_path)
    #         payload = secret_image_name_bytes + secret_image_bytes
            
    #     final_payload = payload
    #     raw_data = bin(int.from_bytes(final_payload, byteorder=sys.byteorder))[2:]
    #     cipher = DNAencrypt(key, raw_data)
        
    #     plaintext = DNAdecrypt(key, cipher)
        
        
    #     self.assertEqual(raw_data, plaintext)

    # def test_cryptography_mismatched_keys(self):
    #     print("\nTEST 2 - Cryptography (Mismatched Keys)")
    #     image_path = "test_files/secret_test.bmp"
    #     key1 = 1
    #     key2 = 2
        
    #     with open(image_path, "rb") as image:
    #         secret_image_bytes = bytes(image.read())
    #         image.close()
    #         secret_image_name_bytes = str.encode(image_path)
    #         payload = secret_image_name_bytes + secret_image_bytes
            
    #     final_payload = payload
    #     raw_data = bin(int.from_bytes(final_payload, byteorder=sys.byteorder))[2:]
    #     cipher = DNAencrypt(key1, raw_data)
        
    #     plaintext = DNAdecrypt(key2, cipher)
        
        
    #     self.assertNotEqual(raw_data, plaintext)
        
    def test_steganography(self):
        print("\nTEST 3 - Steganography")
        cover = "test_files/cover_test.avi"
        secret = "test_files/secret_test.avi"
        key = 1
        output = "test_temp/encoded.avi"
        mkdir("test_temp/")
        
        setupTempDir()
        cover_fps = videoToImages(cover, "cover")
        videoToImages(secret, "secret")
        stegoEncodeFrames(key)
        imagesToVideo(output, "encoded", cover_fps)
        cleanupTempFiles()
        
        
        encoded_file = "test_temp/encoded.avi"
        secret_output = "test_temp/secret_output.avi"
        
        setupTempDir()
        encoded_fps = videoToImages(encoded_file, "encoded")
        stegoDecodeFrames(key)
        imagesToVideo(secret_output, "secret", encoded_fps)
        cleanupTempFiles()
        
        
        self.assertTrue(filecmp.cmp(secret, secret_output))
        
        shutil.rmtree("test_temp/")


    # def test_file_extension_verification(self):
    #     print("\nTEST 4 - File Management (Incompatible File Extension)")
    #     incompatible_file = "test_files/secret_test.mp4"        
    #     setupTempDir()
        
    #     with self.assertRaises(SystemExit) as exit:
    #         videoToImages(incompatible_file, "cover")
        
    #     print(self.assertEqual(exit.exception.args[0], "Incompatible video type. Must be .avi format."))
            
    # def test_video_length_verification(self):
    #     print("\nTEST 5 - File Management (Incompatible Video Lengths)")       
    #     cover = "test_files/cover_test.avi"
    #     secret = "test_files/secret_long.avi"
    #     key = 1
        
    #     setupTempDir()
    #     cover_fps = videoToImages(cover, "cover")
    #     videoToImages(secret, "secret")
        
    #     with self.assertRaises(SystemExit) as exit:
    #         stegoEncodeFrames(key)
        
    #     print(self.assertEqual(exit.exception.args[0], "Secret video is longer than cover video."))
        
    # def test_frame_size_verification(self):
    #     print("\nTEST 6 - File Management (Incompatible Frame Sizes)")       
    #     secret = "test_files/cover_test.avi"
    #     cover = "test_files/secret_long.avi"
    #     key = 1
        
    #     setupTempDir()
    #     cover_fps = videoToImages(cover, "cover")
    #     videoToImages(secret, "secret")
        
    #     with self.assertRaises(SystemExit) as exit:
    #         stegoEncodeFrames(key)
        
    #     print(self.assertEqual(exit.exception.args[0], "Frame sizes incompatable. Cover video must be 8 times the resolution of the secret video."))
        
    
if __name__ == '__main__':
    runner = unittest.TextTestRunner(verbosity=2)
    unittest.main(testRunner=runner)
