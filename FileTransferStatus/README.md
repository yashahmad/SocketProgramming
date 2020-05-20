File transfer is the process of copying or moving a file from a computer to another over a network or Internet connection. In this tutorial we'll go step by step on how you can write client/server Python scripts that handles that.

The basic idea is to create a server that listens on a particular port, this server will be responsible for receiving files (you can make the server sends files as well). On the other hand, the client will try to connect to the server and send a file of any type.

We are going to use socket module which comes built-in with Python and provides us with socket operations that are widely used on the Internet, as they are behind of any connection to any network.

Related: How to Send Emails in Python using smtplib Module.

First, we gonna need to install tqdm which will enable us to print fancy progress bars:

pip3 install tqdm

Client Code

Let's start with the client, the sender:

import socket
import tqdm
import os

SEPARATOR = "<SEPARATOR>"
BUFFER_SIZE = 4096 # send 4096 bytes each time step

We need to specify the IP address and the port of the server we want to connect to, and also the name of the file we want to send.

# the ip address or hostname of the server, the receiver
host = "192.168.1.101"
# the port, let's use 5001
port = 5001
# the name of file we want to send, make sure it exists
filename = "data.csv"
# get the file size
filesize = os.path.getsize(filename)

The filename needs to exist in the current directory, or you can use an absolute path to that file somewhere in your computer. This is the file you want to send.

os.path.getsize(filename) gets the size of that file in bytes, that's great, as we need it for printing progress bars in the client and the server.

Let's create the TCP socket:

# create the client socket
s = socket.socket()

Connecting to the server:

print(f"[+] Connecting to {host}:{port}")
s.connect((host, port))
print("[+] Connected.")

connect() method expects an address of the pair (host, port) to connect the socket to that remote address. Once the connection is established, we need to send the name and size of the file:

# send the filename and filesize
s.send(f"{filename}{SEPARATOR}{filesize}".encode())

I've used SEPARATOR here just to separate the data fields, it is just a junk message, we can just use send() twice, but we may don't wanna do that anyways. encode() function encodes the string we passed to 'utf-8' encoding (that's necessary).

Now we need to send the file, and as we are sending the file, we'll print nice progress bars using tqdm library:

# start sending the file
progress = tqdm.tqdm(range(filesize), f"Sending {filename}", unit="B", unit_scale=True, unit_divisor=1024)
with open(filename, "rb") as f:
    for _ in progress:
        # read the bytes from the file
        bytes_read = f.read(BUFFER_SIZE)
        if not bytes_read:
            # file transmitting is done
            break
        # we use sendall to assure transimission in 
        # busy networks
        s.sendall(bytes_read)
        # update the progress bar
        progress.update(len(bytes_read))
# close the socket
s.close()

Basically what we are doing here is opening the file as read in binary, read chunks from the file (in this case, 4096 bytes or 4KB) and send them to the socket using sendall() function, and then we update the progress bar each time, once that's finished, we close that socket.
Server Code

Alright, so we are done with the client. Let's dive into the server, so open up a new empty Python file and:

import socket
import tqdm
import os
# device's IP address
SERVER_HOST = "0.0.0.0"
SERVER_PORT = 5001
# receive 4096 bytes each time
BUFFER_SIZE = 4096
SEPARATOR = "<SEPARATOR>"

I've initialized some parameters we gonna use, notice that I've used "0.0.0.0" as the server IP address, this means all IPv4 addresses on the local machine. You may wonder, why we don't just use our local IP address or "localhost" or "127.0.0.1" ? Well, if the server has two IP addresses, let's say "192.168.1.101" on a network, and "10.0.1.1" on another, and the server listens on "0.0.0.0", it will be reachable at both of those IPs.

Alternatively, you can use either your public or private IP address, depending on your clients. If the connected clients are in your local network, you should use your private IP (you can check it using ipconfig command in Windows or ifconfig command in Mac OS/Linux), but if you're expecting clients from the Internet, you definitely should use your public address.

Also, Make sure you use the same port in the server as in the client.

Let's create our TCP socket:

# create the server socket
# TCP socket
s = socket.socket()

Now this is different from the client, we need to bind the socket we just created to our SERVER_HOST and SERVER_PORT:

# bind the socket to our local address
s.bind((SERVER_HOST, SERVER_PORT))

After that, we gonna listen for connections:

# enabling our server to accept connections
# 5 here is the number of unaccepted connections that
# the system will allow before refusing new connections
s.listen(5)
print(f"[*] Listening as {SERVER_HOST}:{SERVER_PORT}")

Once the client connects to our server, we need to accept that connection:

# accept connection if there is any
client_socket, address = s.accept() 
# if below code is executed, that means the sender is connected
print(f"[+] {address} is connected.")

Remember that when the client is connected, it'll send the name and size of file, let's receive them:

# receive the file infos
# receive using client socket, not server socket
received = client_socket.recv(BUFFER_SIZE).decode()
filename, filesize = received.split(SEPARATOR)
# remove absolute path if there is
filename = os.path.basename(filename)
# convert to integer
filesize = int(filesize)

As mentioned earlier, the received data is combined of the filename and and the filesize, we can easily extract them by splitting by SEPARATOR string.

After that, we need to remove the absolute path of the file, that's because the sender sent the file with his own file path, which may differ from ours, os.path.basename() returns the final component of a path name.

Now we need to receive the file:

# start receiving the file from the socket
# and writing to the file stream
progress = tqdm.tqdm(range(filesize), f"Receiving {filename}", unit="B", unit_scale=True, unit_divisor=1024)
with open(filename, "wb") as f:
    for _ in progress:
        # read 1024 bytes from the socket (receive)
        bytes_read = client_socket.recv(BUFFER_SIZE)
        if not bytes_read:    
            # nothing is received
            # file transmitting is done
            break
        # write to the file the bytes we just received
        f.write(bytes_read)
        # update the progress bar
        progress.update(len(bytes_read))

# close the client socket
client_socket.close()
# close the server socket
s.close()

Not quite different from the client code. However, we are opening the file as write in binary here, and using recv(BUFFER_SIZE) to receive BUFFER_SIZE bytes from the client socket and write it to the file. Once that's finished, we close both the client and server sockets.

Alright, let me try it on my own private network:

C:\> python receiver.py

[*] Listening as 0.0.0.0:5001

I need to go to my Linux box and send some example file:

root@rockikz:~/tools# python3 sender.py
[+] Connecting to 192.168.1.101:5001
[+] Connected.
Sending data.npy:   9%|███████▊                                                                            | 45.5M/487M [00:14<02:01, 3.80MB/s]

Let's see the server now:

[+] ('192.168.1.101', 47618) is connected.
Receiving data.npy:  33%|███████████████████▍                                       | 160M/487M [01:04<04:15, 1.34MB/s]

Great, we are done!

You can extend this code for your own needs now, here are some examples you can implement:

    Enabling the server to receive multiple files from multiple clients in the same time using threads.
    Compressing the files before sending them.
    Encrypting the file before sending it, to ensure that no one has the ability to intercept and read that file, this tutorial will help.
    Ensuring the file is sent properly by checking the checksums of both files (the original file of the sender and the sent file in the receiver). In this case, you need secure hashing algorithms to do it.
