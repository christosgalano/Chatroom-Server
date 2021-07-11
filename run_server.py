import argparse
import pathlib

from src.Server.server import Server


def main(host, port):
    pathlib.Path("data/Server").mkdir(parents=True, exist_ok=True)

    server = Server(host, port)
    server.start()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Chatroom Server")
    parser.add_argument("host", help="Interface the server listens at")
    parser.add_argument(
        "-p", metavar="PORT", type=int, default=5050, help="TCP port (default 5050)"
    )
    args = parser.parse_args()

    main(args.host, args.p)
