import socket
import threading

HOST = "127.0.0.1"
PORT = 5052

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

username = ""


def connect(server_ip, user_name):
    global username

    username = user_name

    client.connect((server_ip, PORT))


def send(message):
    try:
        client.send(f"{username}: {message}".encode())
    except:
        pass


def receive(callback):

    while True:

        try:

            message = client.recv(1024).decode()

            if message == "NICK":

                client.send(username.encode())

            else:

                callback(message)

        except:

            try:
                client.close()
            except:
                pass

            break


def start_listening(callback):

    thread = threading.Thread(
        target=receive,
        args=(callback,),
        daemon=True
    )

    thread.start() 
