import socket
from _thread import *
import pickle
from game import Game


class Server:
    def __init__(self):
        self.server = "localhost"
        self.port = 5555
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            self.socket.bind((self.server, self.port))
        except socket.error as e:
            print(str(e))

        self.socket.listen(4)
        print("Waiting for a connection, Server Started")

        self.games = {}
        self.idCount = 0

    def threaded_client(self, client_socket, player, gameId):
        client_socket.send(str.encode(str(player)))
        while True:
            try:
                data = client_socket.recv(4096).decode()
                if gameId in self.games:
                    game = self.games[gameId]

                    if not data:
                        break
                    else:
                        if data == "reset":
                            game.reset_health()
                        elif data != "get":
                            game.current_health(player, int(data))

                        client_socket.sendall(pickle.dumps(game))
                else:
                    break
            except:
                break

        print("Lost connection")
        try:
            del self.games[gameId]  # Xóa trận đấu khỏi danh sách khi client ngắt kết nối
            print("Closing Game", gameId)
        except:
            pass
        self.idCount -= 1
        client_socket.close()

    def run(self):
        while True:
            client_socket, client_address = self.socket.accept()  # Chấp nhận kết nối từ client mới
            print("Connected to:", client_address)

            self.idCount += 1
            player = 0
            gameId = (self.idCount - 1) // 2
            if self.idCount % 2 == 1:  # Tạo trận đấu mới khi có đủ 2 client
                self.games[gameId] = Game(gameId)
                print("Creating a new game...")
            else:
                self.games[gameId].ready = True  # Đánh dấu trận đấu đã sẵn sàng
                player = 1

            start_new_thread(self.threaded_client, (client_socket, player, gameId))  # Bắt đầu một luồng xử lý client mới


if __name__ == "__main__":
    server = Server()
    server.run()
