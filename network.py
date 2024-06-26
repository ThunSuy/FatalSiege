import socket
import pickle


class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "localhost"
        self.port = 5555
        self.addr = (self.server, self.port)
        self.p = self.connect()

    def getP(self):
        return self.p

    def connect(self):
        try:
            self.client.connect(self.addr)
            return self.client.recv(2048).decode()
        except Exception as e:
            print(f"Failed to connect to server: {e}")
            return None

    def send(self, data):
        try:
            self.client.send(str.encode(data))
            reply = self.client.recv(2048 * 2)
            return pickle.loads(reply)
        except socket.error as e:
            print(f"Socket error: {e}")
            return None
