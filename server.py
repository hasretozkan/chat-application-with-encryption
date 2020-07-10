import socket
import sys
import threading
from lazyme.string import color_print


HOST = '192.168.1.23'
PORT = 3002
counter = 0


mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    mySocket.bind((HOST, PORT))
except socket.error:
    color_print("Hatayla karşılaşıldı.", 'red')
    sys.exit
color_print('----------------------------------------', 'blue')
color_print('|                                      |', 'blue')
color_print('|          Sunucu artık hazır          |', 'blue')
color_print('|                                      |', 'blue')
color_print('----------------------------------------', 'blue')
mySocket.listen(2)


clients = list()
while counter < 2:
    connexion, adresse = mySocket.accept()
    counter += 1
    
    color_print('', 'yellow')
    color_print('----------------------------------------', 'yellow')
    color_print('|                                      |', 'yellow')
    color_print('|        Bir kullanıcı bağlandı        |', 'yellow')
    color_print('|                                      |', 'yellow')
    color_print('----------------------------------------', 'yellow')
    clients.append([connexion, adresse])


class worker(threading.Thread):
    def __init__(self, client_from, client_to):
        threading.Thread.__init__(self)
        self.client_from = client_from[0]
        self.client_from_add = client_from[1]
        self.client_to = client_to[0]
        self.client_to_add = client_to[1]

    def run(self):

        while 1:
            msgClient = self.client_from.recv(5000).decode("Utf8")
            self.client_to.send(msgClient.encode("Utf8"))


from_1_to_2 = worker(clients[0], clients[1])
from_2_to_1 = worker(clients[1], clients[0])

from_1_to_2.start()
from_2_to_1.start()
