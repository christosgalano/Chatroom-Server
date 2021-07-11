import socket
from os import mkdir, path

from .receive import Receive
from .send import Send

from Utilities.exchange import send_message, receive_message
from Utilities.shared import get_shared_standards, clear_screen


class Client:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.username = None
        self.password = None

    def start(self):
        print(f"Trying to connect to {self.host}:{self.port} ...")
        self.client_socket.connect((self.host, self.port))
        print(f"Successfully connected to {self.host}:{self.port}")
        print()

        if not self.connect():
            return

        if self.validate():
            if not path.exists(f"./data/Users/{self.username}"):
                mkdir(f"./data/Users/{self.username}")

            # Create send and receive threads
            send = Send(self.client_socket, self.username)
            receive = Receive(self.client_socket, self.username)

            # Start send and receive threads
            send.start()
            receive.start()

    def connect(self):
        try:
            message, _ = receive_message(self.client_socket, get_shared_standards()["HEADER_LEN"])
            if message == "ACK":
                send_message("SYN_ACK", self.client_socket, get_shared_standards()["HEADER_LEN"])
            return True
        except Exception:
            self.client_socket.close()
            return False

    def validate(self):
        try:
            while True:
                message, _ = receive_message(self.client_socket, get_shared_standards()["HEADER_LEN"])
                if message == "CREDENTIALS":
                    self.username = input("\rGive username: ")
                    while True:
                        self.password = input("\rGive password (exactly 6 characters): ")
                        if len(self.password) >= 6 and self.password.isalpha():
                            break

                    credentials = f"Username:{self.username},Password:{self.password}"
                    send_message(credentials, self.client_socket, get_shared_standards()["HEADER_LEN"])

                elif message == "WRONG PASSWORD":
                    print("\rWrong password!")
                    while True:
                        self.password = input("\rGive password or type exit: ")
                        if self.password == "exit" or (len(self.password) >= 6 and self.password.isalpha()):
                            break

                    if self.password == "exit":
                        send_message("ABORT", self.client_socket, get_shared_standards()["HEADER_LEN"])
                        return False
                    else:
                        credentials = f"Username:{self.username},Password:{self.password}"
                        send_message(credentials, self.client_socket, get_shared_standards()["HEADER_LEN"])

                elif message == "WELCOME":
                    clear_screen()
                    print(f"\rWelcome {self.username}\n")
                    return True

                elif message == "NOT EXISTS, CREATE?":
                    choice = None
                    while choice != "y" and choice != "Y" and choice != "n" and choice != "N":
                        choice = input("\rNo such user exists, do you wish to create one (y/n): ")

                    if choice == "n":
                        send_message("ABORT", self.client_socket, get_shared_standards()["HEADER_LEN"])
                        return False
                    else:
                        send_message("YES", self.client_socket, get_shared_standards()["HEADER_LEN"])

        except Exception:
            self.client_socket.close()
