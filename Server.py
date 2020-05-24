import socket
import threading

# Parameters used in this program

class Server:

    HOST = "192.168.20.103"
    PORT = 12345

    clients = []
    client_names = {}

    def broadcast_message(self, message : str):
        '''
            This function sends the message recieved 
            from the client to all the other clients
            to achieve multi-client Chat room
        '''
        _clients = self.clients.copy()

        for c in _clients:
            c.send(message.encode())
            

    def listen_to_client_messages(self, conn : socket.socket):
        '''
            This function is ran under a new thread where it 
            constantly listens to the ip if the client is sending
            any messages and if any message is recieved the message
            is broadcasted to other clients
        '''

        # Getting the IP and PORT of the Client
        IP, PORT = conn.getpeername()

        # The first message recieved by the client is the name
        # of the client. This is mapped using the `client_names`
        name = conn.recv(1024).decode()
        # client_names[(IP, PORT)] = name

        # Log to the server
        print(f"{IP}:{PORT} => {name}")

        # This Loop keeps on reading messages from the client
        while True:

            try:
                msg = conn.recv(1024).decode()
                self.broadcast_message(f"{name} => {msg}")

            except Exception:
                
                # client_names.pop((IP, PORT))
                # clients.remove(conn)
                
                conn.close()
                threading.currentThread()._stop()


    def start_server(self):
        '''
            This function is responsible to start the server
            and listen to all the client messages using threads
        '''
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:

            s.bind((self.HOST, self.PORT))
            print(f"Starting server on -> {self.HOST}:{self.PORT}")
            
            s.listen()

            while True:

                conn, addr = s.accept()
                
                if conn not in self.clients:
                    self.clients.append(conn)

                threading._start_new_thread(self.listen_to_client_messages, (conn, ))

if __name__ == "__main__":

    serv = Server()
    serv.start_server()