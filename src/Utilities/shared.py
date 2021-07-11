import pickle
from os import system, name


def create_shared_standards():
    shared = {"HEADER_LEN": 64, "DISCONNECT_MSG": "!DIS"}
    with open("standards.pkl", "wb") as f:
        pickle.dump(shared, f)


def get_shared_standards():
    with open("standards.pkl", "rb") as f:
        return pickle.load(f)


def clear_screen():
    # for windows
    if name == 'nt':
        _ = system('cls')

    # for mac and linux(here, os.name is 'posix')
    else:
        _ = system('clear')
