import argparse

from src.Client.client import Client


def main(host, port):
    client = Client(host, port)
    client.start()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Chatroom Server")
    parser.add_argument("host", help="Interface the server listens at")
    parser.add_argument(
        "-p", metavar="PORT", type=int, default=5050,
        help="TCP port (default 5050)"
    )
    args = parser.parse_args()

    main(args.host, args.p)
