# ----------------- Asher Lagemi & Shakedi Levin ---------------
# THIS IS A CLIENT THE HAS A GUI FOR THE CHATS, IT IS BASED ON THE REGULAR CLIENT
# THEREFORE THE ONLY WELL DOCUMENTED LINES ARE THE CHANGED ONES. FOR THE REST SEE Client.py

import socket
import threading
import time
import tkinter as tk

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 3000  # The port used by the server
FORMAT = 'utf-8'
ADDR = (HOST, PORT)  # Creating a tuple of IP+PORT


def start_client():
    client_socket.connect((HOST, PORT))  # Connecting to server's socket
    while True:
        # receive the opening message and options from the server
        print(client_socket.recv(1024).decode(FORMAT))

        # get the choice from the user
        user_choice = input("Enter your choice: ")

        # send the choice to the server
        client_socket.send(user_choice.encode(FORMAT))

        print("You chose option ", end="")

        if user_choice == "1":
            print("1")
            client_connect_to_group(client_socket)
        elif user_choice == "2":
            print("2")
            client_create_group(client_socket)
        elif user_choice == "3":
            print("3")
            break
        else:
            print("an invalid option")

    client_socket.close()  # Closing client's connection with server (<=> closing socket)
    print("\n[CLOSING CONNECTION] client closed socket!")


# -------------------- HELPING FUNCTIONS --------------------------------
def client_connect_to_group(conn):  # This is option 1
    print(conn.recv(1024).decode(FORMAT))
    name = input()
    conn.send(name.encode(FORMAT))
    print(conn.recv(1024).decode(FORMAT))
    group_id = input()
    conn.send(group_id.encode(FORMAT))
    print(conn.recv(1024).decode(FORMAT))
    password = input()
    conn.send(password.encode(FORMAT))

    status = conn.recv(1024).decode(FORMAT)
    print(status)  # this is a status message (error or success)
    if not status.split(':')[0] == 'ERROR':
        # connect to the chat
        chat_gui()  # REPLACED THE SENDING AND RECEIVING WITH THE NEW GUI FUNCTION
    else:
        print("Try Again...\n")


def client_create_group(conn):  # This is option 2
    print(conn.recv(1024).decode(FORMAT))
    name = input()
    conn.send(name.encode(FORMAT))
    print(conn.recv(1024).decode(FORMAT))
    password = input()
    conn.send(password.encode(FORMAT))

    print(conn.recv(1024).decode(FORMAT))  # this is a status message (error or success with new id)

    chat_gui()  # REPLACED THE SENDING AND RECEIVING WITH THE NEW GUI FUNCTION


# Creates a GUI for the group, that displays the messages and sends to sever from textbox
def chat_gui():
    # Create main window
    window = tk.Tk()
    window.title("Chat Client")

    # Create chat log
    chat_log = tk.Text(window, bg="white", width=50, height=20)
    chat_log.pack()

    # Create chat entry field
    chat_entry = tk.Entry(window, width=50)
    chat_entry.pack()

    # Function to send message with GUI
    def send_message():
        message = chat_entry.get()  # get to message
        client_socket.send(message.encode(FORMAT))  # send to server
        chat_log.insert(tk.END, "You: " + message + "\n")  # display on screen
        chat_entry.delete(0, tk.END)  # clear textbox

    # Function to receive message from server and display on GUI
    def receive_from_server():
        while True:
            # Receive message from server
            message = client_socket.recv(1024).decode(FORMAT)
            # Display message in chat log
            chat_log.insert(tk.END, message + "\n")
            # Sleep for a short time to avoid flooding the server with requests
            time.sleep(0.1)

    # Create send button
    send_button = tk.Button(window, text="Send", width=50, command=send_message)
    send_button.pack()

    # Start receiving messages from server in a separate thread
    receive_thread = threading.Thread(target=receive_from_server)
    receive_thread.start()

    # Run main loop
    window.mainloop()


if __name__ == "__main__":
    IP = socket.gethostbyname(socket.gethostname())
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    print("[CLIENT] Started running")
    start_client()
    print("\nGoodbye client:)")
