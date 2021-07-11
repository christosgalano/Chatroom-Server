# Documentation #

## General ##
This project implements a simple chat room server using the TCP protocol.

## Functionality ##

* Multiple clients can connect to the server

* In order for a client to connect to the server and use the chatroom they
must first login - if a user with their username already exists - or create
a new user

* The server stores both the username and the password of every user in order to authenticate when a
client tries to connect to the chatroom. All the usernames and their corresponding passwords are stored
in data/Server/users.csv

* For each user a history is being kept in data/Users/username, where received.csv keeps track of the messages
the user has received and send.csv of those they have sent

## Build ##

Run "pip install ." from the top-level directory (Chatroom_Server if you do not rename it).


## Run ##

Run "python run_server -h" so that you can get information regarding the different options of the command line.
Similarly run "python run_client -h".
