import socket

port = 60000

s = socket.socket()
host = socket.gethostname()
s.bind((host, port))

s.listen(5)

print("Server is listening")

while True:
    conn, addr = s.accept()
    print("Got connection from ",addr)
    data = conn.recv(1024)
    print('Server recieved',repr(data))

    filename = '1.mp4'
    f=open(filename,'rb')
    l=f.read(10240)
    while(l):
        conn.send(l)
        print('Sent',repr(l))
        l=f.read(10240)
    f.close()
    print('Done sending')
    conn.send('Thank you for connecting'.encode())
    conn.close()
