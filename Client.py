import socket
import tkinter
import threading

class Client:

    HOST = "192.168.20.103"
    PORT = 12345

    def __init__(self):
        '''
            Initializes the GUI
        '''
        
        self.start_client()

        self.screen = tkinter.Tk(screenName="Main Window")

        canvas = tkinter.Canvas(self.screen, width = 800, height = 600)
        canvas.pack()

        self.__startpage(canvas)

        self.screen.mainloop()

    def __startpage(self, canvas : tkinter.Canvas):
        ''' 
            This method helps in rendering the starting page of the application.
            Starting page is basically sending the name data to the server.
        '''

        canvas.delete("all")

        label = tkinter.Label(self.screen, text = "Enter name : ")
        canvas.create_window(300, 300, window = label)

        name = tkinter.Entry(self.screen)
        canvas.create_window(400, 300, window = name)

        button = tkinter.Button(text = "Enter Chat room", command = lambda : self.__gotoChatroom(canvas, name.get()))
        canvas.create_window(400, 350, window = button)

    def __gotoChatroom(self, canvas : tkinter.Canvas, name : str):
        '''
            Guiding the GUI to clear the screen and render the chat room.
            In the process, send the name data to the server.
            Then, go to the chatroom page
        '''

        canvas.destroy()
        self.name = name

        print(self.name)
        self.s.send(self.name.encode())

        self.__chatroom()

    def __showMessage(self, message : str):
        '''
            This is a utility function that displays the message in that chat
            history.
        '''

        self.chats.config(state = tkinter.NORMAL)
        self.chats.insert(tkinter.END, message + "\n")
        self.chats.config(state = tkinter.DISABLED)

    def __sendMessage(self, message : tkinter.Entry):
        '''
            This is a utility function which sends the data given by the user, 
            and sends it to server.

            Then, we clear the text field.
        '''

        _message = message.get()

        # self.__showMessage(_message)
        # print(_message)

        self.s.send(_message.encode())

        message.delete(0, tkinter.END)

    def __chatroom(self):
        '''
            This is a chatroom.

            It is divided into 2 frames.
                1. Chat Frame
                2. Message Frame

            Chat Frame:-
                In this frame, all the chat history is displayed from various users which is broadcasted
                by the server.

            Message Frame:-
                In this frame, there is a text field for user input and a send button which transmits the data
                to the server.
        '''        

        self.screen.geometry("800x600")

        # ----------------x-------------------------

        # Chat Frame :-
        chatFrame = tkinter.Frame(self.screen)

        yScroll =  tkinter.Scrollbar(chatFrame)
        yScroll.pack(side = tkinter.RIGHT, fill = tkinter.Y)

        self.chats = tkinter.Text(chatFrame, width = 100, height = 35, wrap = tkinter.WORD, yscrollcommand = yScroll.set)
        yScroll.config(command = self.chats.yview)
        self.chats.config(state = tkinter.DISABLED)
        self.chats.pack()

        chatFrame.pack(side = tkinter.TOP)

        # ----------------x--------------------------

        # Message Frame :-
        messageFrame = tkinter.Frame(self.screen)

        message = tkinter.Entry(messageFrame, width = 120)
        message.pack(side = tkinter.LEFT)

        sendButton = tkinter.Button(messageFrame, text = "Send", width = 10, command = lambda : self.__sendMessage(message))
        sendButton.pack(side = tkinter.RIGHT)
        
        # ------------------x-------------------------

        messageFrame.pack(side = tkinter.BOTTOM, fill = "x")

    def read_messages(self, s: socket.socket):
        '''
            This function constantly reads if the server recieved 
            any messages from other clients, if yes, it would be 
            recieved and printed in the terminal/console.
        '''
        while True:

            msg = s.recv(1024).decode()
            self.__showMessage(msg)

    def start_client(self):
        '''
            This function is responsible to connect this pc with
            the server and be able to messages
        '''

        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((self.HOST, self.PORT))
        threading._start_new_thread(self.read_messages, (self.s, ))


if __name__ == "__main__":

    client = Client()
