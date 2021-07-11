import socket
import threading
from datetime import datetime
from os import path

from Utilities.shared import get_shared_standards
from Utilities.data import store_data
from Utilities.exchange import receive_message


class Receive(threading.Thread):

    standards = get_shared_standards()

    def __init__(self, client_socket, user_name):
        super().__init__()
        self.client_socket = client_socket
        self.user_name = user_name
        self.messages = []

    def run(self):
        try:
            while True:
                message, message_len = receive_message(self.client_socket, self.standards["HEADER_LEN"])

                if message is None and message_len is None:
                    break

                self.messages.append(
                    {
                        "from": message.split(":", 1)[0],
                        "message": message.split(":", 1)[1][1:],
                        "time": datetime.now().strftime("%b %d %Y %H:%M:%S"),
                    }
                )
                print(f"\r{message}\n{self.user_name}: ", end="")
        finally:
            self.client_socket.shutdown(socket.SHUT_RD)

        if len(self.messages):
            filename = (f"./data/Users/{self.user_name}/received.csv")
            store_data(filename, self.messages, append=path.exists(filename))
            self.messages.clear()
