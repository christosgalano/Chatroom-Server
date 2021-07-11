import socket
import threading

from Utilities.shared import get_shared_standards

from .server_socket import ServerSocket


class Server(threading.Thread):

    standards = get_shared_standards()

    def __init__(self, host, port):
        super().__init__()
        self.host = host
        self.port = port
        self.listening_socket = None
        self.clients = []

    def run(self):
        self.listening_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.listening_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.listening_socket.bind((self.host, self.port))

        self.listening_socket.listen(1)
        print(f"Listening at {self.listening_socket.getsockname()}")

        while True:
            try:
                client_socket, client_address = self.listening_socket.accept()
                print(f"Accepted a new connection from {client_address}")

                client = ServerSocket(client_socket, client_address, self)
                client.start()
                self.send("ACK", client)
                self.clients.append(client)

                print(f"There are currrently {len(self.clients)} active clients")
            except Exception as e:
                print(e)
                print("Run server")
                self.shutdown()

    def send(self, message, server_socket):
        try:
            server_socket.send(message)
        except Exception as e:
            print(e)
            print("Send server")
            server_socket.close()
            self.remove_connection(server_socket)

    def broadcast(self, client_socket, message):
        for sc in self.clients:
            if sc.client_socket != client_socket:
                self.send(message, sc)

    def remove_connection(self, server_socket):
        if server_socket in self.clients:
            self.clients.remove(server_socket)

    def shutdown(self):
        for sc in self.clients:
            sc.close()
        self.clients.clear()
