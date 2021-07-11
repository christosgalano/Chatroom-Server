from time import sleep


def send_message(message, connection, header_length):
    message_length = str(len(message)).encode()
    message_length += b"" * (header_length - len(message))
    connection.sendall(message_length)
    sleep(0.1)
    connection.sendall(message.encode())


def receive_message(connection, header_length):
    message_length = connection.recv(header_length).decode()
    if message_length:
        try:
            message_length = int(message_length)
            message = connection.recv(message_length).decode()
        except ValueError as v:
            if message_length == "3ACK":
                message, message_length = "ACK", 3
            else:
                raise v
        return message, message_length
    else:
        return None, None
