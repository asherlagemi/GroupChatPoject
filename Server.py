# ----------------- Asher Lagemi & Shakedi Levin ---------------
# Imports
import random
import socket
import string
import threading

# Define constants

HOST = '127.0.0.1'  # Standard loop-back IP address (localhost)
PORT = 3000  # Port to listen on (non-privileged ports are > 1023)
FORMAT = 'utf-8'  # Define the encoding format of messages from client-server
ADDR = (HOST, PORT)  # Creating a tuple of IP+PORT

existing_groups = {}  # This will contain all the data about the groups the were created. The format is


# {"id": {"password": pass, "clients": {name: conn}}}

# Prints the existing_groups in a nice format
def print_groups():
    print("GROUPS-STATUS:")
    for g in existing_groups:
        print("\tid: {}, password: {}, clients: {}".format(g,
                                                           existing_groups[g]["password"],
                                                           list(existing_groups[g]["clients"].keys())))


# Function that handles a single client connection
# Operates like an echo-server
def handle_client(conn, addr):
    print('[CLIENT CONNECTED] on address: ', addr)  # Printing connection address
    while True:  # will come back to here on failure
        conn.send("Welcome to the group chat server!\nPlease choose an option:\n1. Connect"
                  " to a group chat\n2. Create a "
                  "group chat\n3. Exit the server\n".encode(FORMAT))  # Send options to client
        user_choice = conn.recv(1024).decode(FORMAT)  # Receiving from client his option from the menu
        print("User chose option " + user_choice)

        try:
            if user_choice == "1":
                connect_to_group(conn)  # connect user to a group
            elif user_choice == "2":
                create_group(conn)  # create a new group
            elif user_choice == "3":
                break  # will disconnect immediately after
            else:
                raise ValueError  # In this case the user sent an illegal value

            print()
        except ValueError:
            print("Invalid option was inserted.")
            print("[CLIENT CONNECTION INTERRUPTED] on address: ", addr)
        except:  # probably some kind of connection error
            print("[CLIENT CONNECTION INTERRUPTED] on address: ", addr)

    # Here we broke out of the while true
    print("\n[CLIENT DISCONNECTED] on address: ", addr)


# -------------------- HELPING FUNCTIONS --------------------------------

# Option 1 - get name, id and password and connects the client to the group
def connect_to_group(conn):  # This is option 1
    conn.send("Please enter your name: ".encode(FORMAT))
    name = conn.recv(1024).decode(FORMAT)       # get the name
    conn.send("Group ID: ".encode(FORMAT))
    group_id = conn.recv(1024).decode(FORMAT)   # get the id
    conn.send("Password: ".encode(FORMAT))
    password = conn.recv(1024).decode(FORMAT)   # get the password
    if group_id in existing_groups:
        if password == existing_groups[group_id]['password']:
            # Both the id and password exist and are matching
            conn.send("You are now connected to group chat {}!\n".format(group_id).encode(FORMAT))
            existing_groups[group_id]['clients'][name] = conn   # add client to group
            print_groups()  # print status
            for member_conn in existing_groups[group_id]['clients'].values():
                # notify members that the client has joined the chat
                member_conn.send("* SERVER: {} entered the chat room *".format(name).encode(FORMAT))
            groupchat(group_id, conn, name)  # handle the client in the chat
        else:   # password isn't matching
            conn.send("ERROR: WRONG PASSWORD\n".encode(FORMAT))
    else:   # id does not exit in data
        conn.send("ERROR: NO SUCH GROUP\n".encode(FORMAT))


# Option 2 - get name and desired password, then connect client to the new group and supply him with the id
def create_group(conn):  # This is option 2
    conn.send("Please enter your name: ".encode(FORMAT))
    name = conn.recv(1024).decode(FORMAT)       # get the name
    conn.send("Password: ".encode(FORMAT))
    password = conn.recv(1024).decode(FORMAT)   # get the password
    group_id = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))    # generate a random id
    while group_id in existing_groups:  # make sure the id is unique (probably on first try, but we make sure)
        group_id = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))
    group = {'password': password, 'clients': {name: conn}}     # create the group with the creator client inside
    existing_groups[group_id] = group   # store the group data
    print_groups()  # print the status
    conn.send("Successfully created group with id: {}".format(group_id).encode(FORMAT))  # send the status message
    groupchat(group_id, conn, name)  # handle the client in the chat


# Function that sends the client messages to every other client in the group
def groupchat(group_id, curr_conn, name):
    while True:
        msg = curr_conn.recv(1024).decode(FORMAT)   # get the message
        for member_conn in existing_groups[group_id]['clients'].values():
            if not member_conn == curr_conn:    # to every member but self
                member_conn.send("{}: {}".format(name, msg).encode(FORMAT))  # send to members


# Function that starts the server
def start_server():
    server_socket.bind(ADDR)  # binding socket with specified IP+PORT tuple

    print(f"[LISTENING] server is listening on {HOST}")
    server_socket.listen()  # Server is open for connections

    while True:
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}\n")  # printing the amount of threads working

        connection, address = server_socket.accept()  # Waiting for client to connect to server (blocking call)
        print(connection)
        print(address)
        thread = threading.Thread(target=handle_client, args=(connection, address))  # Creating new Thread object.
        # Passing the handle func and full address to thread constructor
        thread.start()  # Starting the new thread (<=> handling new client)

        # print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}\n")  # printing the amount of threads working
        # on this process (opening another thread for next client to come!)


# Main
if __name__ == '__main__':
    IP = socket.gethostbyname(socket.gethostname())  # finding your current IP address

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Opening Server socket

    print("[STARTING] server is starting...")
    start_server()

    print("THE END!")
