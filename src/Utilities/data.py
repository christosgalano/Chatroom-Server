import pandas as pd
import numpy as np
from os import path


def store_data(filename, messages, append):
    df = pd.DataFrame(messages, index=np.arange(len(messages)))
    df.to_csv(
        filename, mode="a" if append else "w", index=False, header=False if append else df.iloc[0].keys()
    )


filename = "./data/Server/users.csv"


def find_user(username):
    if not path.exists(filename):
        return False
    df = pd.read_csv(filename)
    return len(df[df["username"] == username])


def authenticate(username, password):
    # It is already ensured that a user with the given username exists
    df = pd.read_csv(filename)
    df = df[df["username"] == username]
    return password in df.values


def find_no_users():
    if not path.exists(filename):
        return 0
    df = pd.read_csv(filename)
    return len(df.index)


def add_user(username, password):
    user = {"username": username, "password": password}
    df = pd.DataFrame(user, index=[find_no_users()], columns=["username", "password"])

    append = True if path.exists(filename) else False
    df.to_csv(
        filename, mode="a" if append else "w",
        index=False, header=not append
    )
