import socket

s = socket.socket()
host = socket.gethostname()
port = 60000

s.connect((host, port))
s.send("Hello Server!".encode())

with open('received_file','wb') as f:
    print('File opened')
    while True:
        print('Receiving data...')
        data = s.recv(1024)
        print('data=%s',(data))
        if not data:
            break
        f.write(data)

f.close()
print('Successfully get the file')
s.close()
print('Connection closed')