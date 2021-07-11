import socket
import sys
import threading
from datetime import datetime
from os import path

from Utilities.exchange import send_message
from Utilities.shared import get_shared_standards
from Utilities.data import store_data


class Send(threading.Thread):

    standards = get_shared_standards()

    def __init__(self, client_socket, user_name):
        super().__init__()
        self.client_socket = client_socket
        self.user_name = user_name
        self.messages = []

    def run(self):
        try:
            while True:
                print(f"\r{self.user_name}: ", end="")
                sys.stdout.flush()
                message = sys.stdin.readline()[:-1]

                if message == Send.standards["DISCONNECT_MSG"]:
                    send_message(message, self.client_socket, Send.standards["HEADER_LEN"])
                    break

                message = f"{self.user_name}: {message}"
                send_message(message, self.client_socket, Send.standards["HEADER_LEN"])

                self.messages.append(
                    {
                        "to": "all",
                        "message": message.split(":", 1)[1][1:],
                        "time": datetime.now().strftime("%b %d %Y %H:%M:%S")
                    }
                )
        finally:
            self.client_socket.shutdown(socket.SHUT_WR)

        if len(self.messages):
            filename = (f"./data/Users/{self.user_name}/sent.csv")
            store_data(filename, self.messages, append=path.exists(filename))
            self.messages.clear()
