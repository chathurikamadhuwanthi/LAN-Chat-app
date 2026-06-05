import socket
import threading

HOST = "0.0.0.0"
PORT = 5052

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

clients = []
usernames = []


def broadcast(message):
    for client in clients:
        try:
            client.send(message)
        except:
            pass


def update_users():

    user_list = ",".join(usernames)

    broadcast(
        f"USERS:{user_list}".encode()
    )


def handle(client):

    while True:

        try:

            message = client.recv(1024).decode()

            if message.startswith("PRIVATE:"):

                parts = message.split(":", 2)

                target_user = parts[1]

                private_message = parts[2]

                if target_user in usernames:

                    index = usernames.index(target_user)

                    clients[index].send(
                        f"[PRIVATE] {private_message}".encode()
                    )

            else:

                broadcast(message.encode())

        except:

            if client in clients:

                index = clients.index(client)

                username = usernames[index]

                clients.remove(client)
                usernames.remove(username)

                update_users()

                broadcast(
                    f"{username} left the chat".encode()
                )

                client.close()

            break


def receive():

    print(f"Server running on port {PORT}...")

    while True:

        client, address = server.accept()

        print(f"Connected: {address}")

        client.send("NICK".encode())

        username = client.recv(1024).decode()

        usernames.append(username)
        clients.append(client)

        update_users()

        print(f"{username} joined")

        broadcast(
            f"{username} joined the chat".encode()
        )

        thread = threading.Thread(
            target=handle,
            args=(client,)
        )

        thread.start()


receive() 
