import socket
import tqdm
import os

SERVER_HOST = "0.0.0.0"
SERVER_PORT = 5000

BUFFER_SIZE = 4096
SEPERATOR = "<SEPERATOR>"

s = socket.socket()
s.bind((SERVER_HOST, SERVER_PORT))

s.listen(5)
print(f"[*] Listening as {SERVER_HOST}:{SERVER_PORT}")

client_socket , address = s.accept()

print(f"[+] {address} is connected.")

received = client_socket.recv(BUFFER_SIZE).decode()
filename, filesize = received.split(SEPERATOR)

filename = os.path.basename(filename)

filesize = int(filesize)

progress = tqdm.tqdm(range(filesize), f"Receiving {filename}", unit="B", unit_scale=True, unit_divisor=1024)
with open(filename, "wb") as f:
    for _ in progress:
        bytes_read = client_socket.recv(BUFFER_SIZE)
        if not bytes_read:
            break
        f.write(bytes_read)
        progress.update(len(bytes_read))
client_socket.close()
s.close()