import socket
import tqdm
import os

SEPERATOR = "<SEPERATOR>"
BUFFER_SIZE = 4096

host = "0.0.0.0"
port = 5000

filename = "dsa.pdf"
filesize = os.path.getsize(filename)

s = socket.socket()
print(f"[+] Connecting to {host}:{port}")
s.connect((host,port))
print(f"[+] Connected.")

s.send(f"{filename}{SEPERATOR}{filesize}".encode())

progress = tqdm.tqdm(range(filesize),f"Sending {filename}",unit="B", unit_scale=True, unit_divisor=1024)
with open(filename,"rb") as f:
    for _ in progress:
        bytes_read = f.read(BUFFER_SIZE)
        if not bytes_read:
            break
        s.sendall(bytes_read)
        progress.update(len(bytes_read))
s.close()

