# Client side GUI chat room
import tkinter, socket, threading
from tkinter import DISABLED, VERTICAL, END, NORMAL

# Define window
root = tkinter.Tk()
root.title("Chat Client")
root.iconbitmap("message_icon.ico")
root.geometry("800x600")
root.resizable(False, False)

# Define fonts and colors
my_font = ('Sim sun', 14)
black = "#010101"
light_green = "#1fc742"
root.config(bg=black)

# Define socket constants
ENCODER = 'utf-8'
BYTESIZE = 1024
global client_socket


# Define functions
def connect():
    """Connect to a server at a given ip/port address"""
    global client_socket

    # Clear any previous chat
    my_listbox.delete(0, END)

    # Get the required connection information
    name = name_entry.get()
    ip = ip_entry.get()
    port = port_entry.get()

    if name and ip and port:
        # Conditions for connections are met
        my_listbox.insert(0, f"{name} is waiting to connect to {ip} at {port}...")

        # Create a client socket to connect to the server
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((ip, int(port)))

        # varify the connection is valid
        verify_connection(name)
    else:
        # The Condition for the connection isn't met
        my_listbox.insert(0, "Insufficient information for connection...")


def verify_connection(name):
    """Verify that the server connection is valid and pass required information"""
    global client_socket

    # The server will send a NAME flag if a valid connection is made
    flag = client_socket.recv(BYTESIZE).decode(ENCODER)

    if flag == "NAME":
        client_socket.send(name.encode(ENCODER))
        message = client_socket.recv(BYTESIZE).decode(ENCODER)

        if message:
            my_listbox.insert(0, message)

            # change the button status
            connect_button.config(state=DISABLED)
            disconnect_button.config(state=NORMAL)
            send_button.config(state=NORMAL)

            name_entry.config(state=DISABLED)
            ip_entry.config(state=DISABLED)
            port_entry.config(state=DISABLED)

            # Create a thread to continuously receive messages from the server
            receive_thread = threading.Thread(target=receive_message)
            receive_thread.start()

        else:
            my_listbox.insert(0, "Connection not verified...")
            client_socket.close()
    else:
        my_listbox.insert(0, "Connection refused.")
        client_socket.close()


def disconnect():
    """Disconnect from the server"""
    global client_socket

    # Close the client socket
    client_socket.close()

    # change the status of the buttons
    connect_button.config(state=NORMAL)
    disconnect_button.config(state=DISABLED)
    send_button.config(state=DISABLED)

    name_entry.config(state=NORMAL)
    ip_entry.config(state=NORMAL)
    port_entry.config(state=NORMAL)


def send_message():
    """Send a message to the server to be broadcast"""
    global client_socket

    # Send the message to the server
    message = input_entry.get()
    client_socket.send(message.encode(ENCODER))

    # Clear the input entry
    input_entry.delete(0, END)


def receive_message():
    """Receive an incoming message from the server"""
    global client_socket

    while True:
        try:
            # Receive an incoming message from the server
            message = client_socket.recv(BYTESIZE).decode(ENCODER)
            my_listbox.insert(0, message)
        except:
            my_listbox.insert(0, "Closing the connection. Good Bye...")
            disconnect()
            break


# Define GUI Layout
# Creates frames
info_frame = tkinter.Frame(root, bg=black)
output_frame = tkinter.Frame(root, bg=black)
input_frame = tkinter.Frame(root, bg=black)

info_frame.pack()
output_frame.pack(pady=10)
input_frame.pack()

# Info Frame Layout
name_label = tkinter.Label(info_frame, text="Client Name:", font=my_font, fg=light_green, bg=black)
name_entry = tkinter.Entry(info_frame, borderwidth=3, font=my_font)
ip_label = tkinter.Label(info_frame, text="Host IP:", font=my_font, fg=light_green, bg=black)
ip_entry = tkinter.Entry(info_frame, borderwidth=3, font=my_font)
port_label = tkinter.Label(info_frame, text="Port Num:", font=my_font, fg=light_green, bg=black)
port_entry = tkinter.Entry(info_frame, borderwidth=3, font=my_font, width=10)
connect_button = tkinter.Button(info_frame, text="Connect", font=my_font, bg=light_green,
                                borderwidth=5, width=10, command=connect)
disconnect_button = tkinter.Button(info_frame, text="Disconnect", font=my_font, bg=light_green,
                                   borderwidth=5, width=10, state=DISABLED, command=disconnect)

name_label.grid(row=0, column=0, padx=2, pady=10)
name_entry.grid(row=0, column=1, padx=2, pady=10)
port_label.grid(row=0, column=2, padx=2, pady=10)
port_entry.grid(row=0, column=3, padx=2, pady=10)
ip_label.grid(row=1, column=0, padx=2, pady=5)
ip_entry.grid(row=1, column=1, padx=2, pady=5)
connect_button.grid(row=1, column=2, padx=10, pady=5)
disconnect_button.grid(row=1, column=3, padx=4, pady=5)

# Output frame layout
my_scrollbar = tkinter.Scrollbar(output_frame, orient=VERTICAL)
my_listbox = tkinter.Listbox(output_frame, height=18, width=68, borderwidth=3, bg=black, fg=light_green,
                             font=my_font, yscrollcommand=my_scrollbar.set)
my_scrollbar.config(command=my_listbox.yview)

my_listbox.grid(row=0, column=0)
my_scrollbar.grid(row=0, column=1, sticky="NS")

# Input frame Layout
input_entry = tkinter.Entry(input_frame, width=55, borderwidth=3, font=my_font)
send_button = tkinter.Button(input_frame, text="send", borderwidth=5, width=10, font=my_font,
                             bg=light_green, command=send_message)

input_entry.grid(row=0, column=0, padx=10, pady=5)
send_button.grid(row=0, column=1, padx=5, pady=5)

# Run the root window's loop
root.mainloop()
