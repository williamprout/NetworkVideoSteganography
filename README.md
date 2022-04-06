# NetworkVideoSteganography

##Installation
###System Requirements 
- Operating System: Windows 10
- Python 3.8.2
- Python Libraries:
    - numpy – version 1.22.0
    - opencv_python – version 4.5.5.62
    - Pillow – version 9.0.1
    - tqdm – version 4.62.3
- VLC Media Player 2.2.4
###Installation Steps
1.	Install Python 3.8.2 (including pip) if it is not already installed. 
2.	Place all the provided .py Python files in an empty directory. 
3.	Place the ‘requirements.txt’ file in the same directory.
4.	Open a command line terminal in the same directory.
5.	Run the following command to install the required Python libraries:
    pip install -r requirements.txt

##Local Encoding
###File Compatibility
- Video files used with the program must be .avi format. Other video formats will not work. 
- Cover videos must be at least 8 times the resolution of the secret video. Example:
    - Cover Video Resolution: 1920x1080 = 2,073,600 pixels
    - Secret Video Resolution: 480×360 = 172,800 pixels
    - 2,073,600 ÷ 127,800 ≈ 16. Cover video is 16 times the resolution of the secret video. They are compatible. 
- Cover videos must not be longer than the secret video. 
###Command Execution
1.	Open a command line terminal in the directory containing the .py Python files. 
2.	Place a cover video and a secret video in the same directory. 
-	cover_test.avi and secret_test.avi located in the test_files directory are example files that can be used for testing.
3.	Run the following command with the inputs replaced with your desired parameters:
    python main.py encode <cover file> <secret file> <encryption key> <output file>
    Parameters:
        1.	<cover file> - name of the cover video file that you wish to encode.
        Example: cover_test.avi
        2.	<secret file> - name of the secret video file that you wish to hide.
        Example: secret_test.avi
        3.	<encryption key> - number 1-255 that you want to use for encryption.
        Example: 1
        4.	<output file> - name for the program to use for the output encoded video file.
        Example encoded.avi
        5.	Encoded file should be playable in VLC Media Player. 

##Local Decoding
###Command Execution
1.	Open a command line terminal in the directory containing the .py Python files. 
2.	Place a previously encoded video file in the same directory. 
3.	Run the following command with the inputs replaced with your desired parameters:
    python main.py decode <encoded file> <decryption key> <output file>
    Parameters:
        1.	<encoded file> - name of the encoded video file that you wish to decode.
        Example: encoded.avi
        2.	<decryption key> - number 1-255 that you want to use for decryption.
        Example: 1
        3.	<output file> - name for the program to use for the output decoded video file.
        Example decoded.avi
        4.	Decoded file should be playable in VLC Media Player. 

##File Transfer
###Setup
1.	Follow the installation instructions on two separate computers that are on the same local network. 
2.	Choose which computer you want to use as the receiver and the other will be the sender. 
3.	Find the local “IPv4 Address” of the receiver computer by running the ipconfig command in a terminal window on the chosen receiver computer.
###Command Execution
####Receiver
    1.	Open a command line terminal in the directory containing the .py Python files. 
    2.	Run the following command with the inputs replaced with your desired parameters:
    python main.py receive <destination port>
    Parameter:
        1.	<destination port> - TCP destination port (a number from 1 to 65535) that you wish to use.
        Example: 8407
####Sender
1.	Open a command line terminal in the directory containing the .py Python files. 
2.	Place a previously encoded video file in the same directory. 
3.	Run the following command with the inputs replaced with your desired parameters:
    python main.py send <file> <destination IP address> <destination port>
    Parameters:
        1.	<file> - name of the encoded video file that you wish to send.
        Example: encoded.avi
        2.	<destination IP address> - IPv4 address of the receiver.
        Example: 192.168.1.14
        3.	<destination port> - TCP destination port (a number from 1 to 65535) that you wish to use.
        Example: 8407

##Video Stream
###Setup
1.	Follow the installation instructions on two separate computers that are on the same local network. 
2.	Choose which computer you want to use as the receiver and the other will be the sender. 
3.	Find the local “IPv4 Address” of the receiver computer by running the ipconfig command in a terminal window on the chosen receiver computer.
###ommand Execution
####Receiver
1.	Open a command line terminal in the directory containing the .py Python files. 
2.	Run the following command with the inputs replaced with your desired parameters:
    python main.py receive_stream <destination port> <encryption key>
    Parameters:
        1.	<destination port> - TCP destination port (a number from 1 to 65535) that you wish to use.
        Example: 8407
        2.	<encryption key> - number 1-255 that you want to use for encryption.
        Example: 1
3.	The program will now start waiting for a connection from the sender. 
4.	Start the script on the sender’s side.
5.	Once a connection is made, the decoding process will start.
6.	The video display will start when 85% of the total frames have been received and decoded.
####Sender
1.	Open a command line terminal in the directory containing the .py Python files. 
2.	Place a cover video and a secret video in the same directory. 
    - cover_480p.avi and secret_144p2.avi located in the test_files directory are example files that can be used for testing.
3.	Run the following command with the inputs replaced with your desired parameters:
    python main.py transmit_stream <secret file> <cover file> <destination IP address> <destination port> <encryption key>
    Parameters:
        1.	<secret file> - name of the secret video file that you wish to hide.
            Example: secret_test.avi
        2.	<cover file> - name of the cover video file that you wish to encode.
            Example: cover_test.avi
        3.	<destination IP address> - IPv4 address of the receiver.
            Example: 192.168.1.14
        4.	<destination port> - TCP destination port (a number from 1 to 65535) that you wish to use.
            Example: 8407
        5.	<decryption key> - number 1-255 that you want to use for decryption.
            Example: 1
        4.	A connection will be made with the receiver. 
        5.	The video stream will begin and complete once all the frames have been sent. 
