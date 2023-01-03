# ----------------- Asher Lagemi & Shakedi Levin ---------------

import socket
import threading

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 3000  # The port used by the server
FORMAT = 'utf-8'
ADDR = (HOST, PORT)  # Creating a tuple of IP+PORT


def start_client():
    client_socket.connect((HOST, PORT))  # Connecting to server's socket
    while True:
        # receive the opening message and options from the server
        print()
        print(client_socket.recv(1024).decode(FORMAT))

        # get the choice from the user
        user_choice = input("Enter your choice: ")

        # send the choice to the server
        client_socket.send(user_choice.encode(FORMAT))

        print("You chose option ", end="")

        if user_choice == "1":
            print("1")
            client_connect_to_group(client_socket)  # corresponds to the server function connect_to_group
        elif user_choice == "2":
            print("2")
            client_create_group(client_socket)  # corresponds to the server function create_group
        elif user_choice == "3":
            print("3")
            break   # exit at once
        else:
            print("an invalid option")

    client_socket.close()  # Closing client's connection with server (<=> closing socket)
    print("\n[CLOSING CONNECTION] client closed socket!")


# -------------------- HELPING FUNCTIONS --------------------------------

# Option 1 - send name, id and password and connects to the group
def client_connect_to_group(conn):  # This is option 1
    print(conn.recv(1024).decode(FORMAT))
    name = input()
    conn.send(name.encode(FORMAT))      # send the name
    print(conn.recv(1024).decode(FORMAT))
    group_id = input()
    conn.send(group_id.encode(FORMAT))  # send the id
    print(conn.recv(1024).decode(FORMAT))
    password = input()
    conn.send(password.encode(FORMAT))  # send the password

    status = conn.recv(1024).decode(FORMAT)
    print(status)  # this is a status message (error or success)
    if not status.split(':')[0] == 'ERROR':  # if the first word of the status message is ERROR we try again
        # otherwise we connect to the chat
        sending_thread = threading.Thread(target=group_send_msg, args=())
        sending_thread.start()      # Creating new thread for sending messages
        group_receive_msg(conn)     # In Current thread we receive messages
    else:
        print("Try Again...\n")


# Option 2 - send name and desired password, then connect to the new group
def client_create_group(conn):  # This is option 2
    print(conn.recv(1024).decode(FORMAT))
    name = input()
    conn.send(name.encode(FORMAT))          # send the name
    print(conn.recv(1024).decode(FORMAT))
    password = input()
    conn.send(password.encode(FORMAT))      # send the password

    print(conn.recv(1024).decode(FORMAT))  # this is a status message (error or success with new id)
    sending_thread = threading.Thread(target=group_send_msg, args=())
    sending_thread.start()      # Creating new thread for sending messages
    group_receive_msg(conn)     # In Current thread we receive messages


# In different thread, wait for input, sent to server, repeat...
def group_send_msg():
    while True:
        msg = input()
        client_socket.send(msg.encode(FORMAT))


# In thread, wait for new message from server, print it, repeat...
def group_receive_msg(server_conn):
    while True:
        print(server_conn.recv(1024).decode(FORMAT))


if __name__ == "__main__":
    IP = socket.gethostbyname(socket.gethostname())
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    print("[CLIENT] Started running")
    start_client()
    print("\nGoodbye client:)")
