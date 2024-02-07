import socket

serversocket = socket.socket()

port = 49152

serversocket.bind(('192.168.1.82', port))

serversocket.listen(5)

c, addr = serversocket.accept()
print('Got connection from', addr)

while True:

    x = input('Introduce a new value for x: ')
    c.send(x.encode())


