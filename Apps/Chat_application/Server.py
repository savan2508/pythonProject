# Server side of the chatroom
import socket, threading

# Define constants to be used
HOST_IP = socket.gethostbyname(socket.gethostname())
HOST_PORT = 12345
ENCODER = 'utf-8'
BYTESIZE = 1024

# Create a server socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST_IP, HOST_PORT))
server_socket.listen()

# Create blank lists to store connected client sockets and their names
client_socket_list = []
client_name_list = []


def broadcast_message(message):
    """Send a message to all clients connected to the server"""
    for client_socket in client_socket_list:
        client_socket.send(message)


def receive_message(client_socket):
    """Receive an incoming message from a specific clients and forward the message
    to broadcast to the clients"""
    while True:
        try:
            # Get the name of the clients
            index = client_socket_list.index(client_socket)
            name = client_name_list[index]

            # Receive a message from the client
            message = client_socket.recv(BYTESIZE).decode(ENCODER)
            message = f"{name}: {message}".encode(ENCODER)
            broadcast_message(message)

        except:
            # Find the index of the client socket in our list
            index = client_socket_list.index(client_socket)
            name = client_name_list[index]

            # Remove the client socket and name from the list
            client_socket_list.remove(client_socket)
            client_name_list.remove(name)

            # Close the client socket
            client_socket.close()

            # Broadcast the message stating that the client has left the room
            broadcast_message(f"{name} has left the chat!".encode(ENCODER))
            break


def connect_client():
    """Connect an incoming clients to the server"""
    while True:
        # Accept any incoming client connection
        client_socket, client_address = server_socket.accept()
        print(f"Connected with {client_address}...")

        # Send a NAME flag to prompt the client for their name
        client_socket.send("NAME".encode(ENCODER))
        client_name = client_socket.recv(BYTESIZE).decode(ENCODER)

        # Add new client socket and client name to appropriate lists
        client_socket_list.append(client_socket)
        client_name_list.append(client_name)

        # Update the server, individual clients, and ALL clients
        print(f"Name of new client is {client_name}\n")  # Server
        client_socket.send(f"{client_name}, you have connected to the server!".encode(ENCODER))
        broadcast_message(f"{client_name} has joined the chat!".encode(ENCODER))

        # Start the thread for each client who connected to the server
        receive_thread = threading.Thread(target=receive_message, args=(client_socket,))
        receive_thread.start()


# Start the server
print(f"Server is listening for incoming connections at IP:{HOST_IP} and port:{HOST_PORT}...\n")
connect_client()
