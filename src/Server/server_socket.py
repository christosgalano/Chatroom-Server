import threading

from Utilities.exchange import send_message, receive_message
from Utilities.data import find_user, add_user, authenticate


class ServerSocket(threading.Thread):
    def __init__(self, client_socket, client_address, server):
        super().__init__()
        self.client_socket = client_socket
        self.client_address = client_address
        self.server = server

    def run(self):
        if not self.validate():
            self.close()
            return
        try:
            while True:
                message = self.receive()
                if message == self.server.standards["DISCONNECT_MSG"]:
                    print(f"{self.client_address} is disconnecting ...")
                    break

                print(f"{self.client_address} : {message}")
                self.server.broadcast(self.client_socket, message)
        finally:
            self.close()

    def send(self, message):
        send_message(message, self.client_socket, self.server.standards["HEADER_LEN"])

    def receive(self):
        message, _ = receive_message(self.client_socket, self.server.standards["HEADER_LEN"])
        return message

    def close(self):
        self.client_socket.close()
        self.server.remove_connection(self)
        print(f"Closed {self.client_address}")

    def validate(self):
        message = self.receive()
        if message == "SYN_ACK":
            self.send("CREDENTIALS")
        while True:
            message = self.receive()
            if message == "ABORT":
                break
            index = message.find(",Password:")
            username = message[:index].split(":", 1)[1]
            password = message[index:].split(":", 1)[1]
            if find_user(username):
                if authenticate(username, password):
                    self.send("WELCOME")
                    return True
                else:
                    self.send("WRONG PASSWORD")
            else:
                self.send("NOT EXISTS, CREATE?")
                answer = self.receive()
                if answer == "YES":
                    add_user(username, password)
                    self.send("WELCOME")
                    return True
                else:
                    break
        return False
