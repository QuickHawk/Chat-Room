import socket
import threading

HOST = "192.168.20.103"
PORT = 12345

def read_messages(s : socket.socket):
    '''
        This function constantly reads if the server recieved 
        any messages from other clients, if yes, it would be 
        recieved and printed in the terminal/console.
    '''
    while True:

        msg = s.recv(1024).decode()
        print(msg)

def start_client():
    '''
        This function is responsible to connect this pc with
        the server and be able to messages
    '''

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:

        s.connect((HOST, PORT))

        name = input("Enter Name : ")
        s.send(name.encode())

        threading._start_new_thread(read_messages, (s, ))

        while True:

            send_message = input()
            s.send(send_message.encode())

if __name__ == "__main__":
    start_client()