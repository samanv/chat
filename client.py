import time
from Tkinter import *
from socket import *
import thread

global name
name = str(raw_input("Screen name: "))
HOST = 'silvahwuff.pythonanywhere.com'
PORT = 21567
BUFSIZE = 1024
ADDR = (HOST, PORT)
print "Connecting..."
tcpCliSock = socket(AF_INET, SOCK_STREAM)
tcpCliSock.connect(ADDR)
print "Connection successful."
inmsg=name+" has joined!"
tcpCliSock.send(inmsg)

class Application(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.grid()
        self.create_widgets()
        self.socket()

    def callback(self, event):
        global name
        message = self.entry_field.get()
        if message[:5] == "/quit":
            tcpCliSock.send(name+" has disconnected")
            quit()
        elif message[:3] == "/me":
            messages="* "+name+message[3:]
            tcpCliSock.send(messages)
        elif message [:5] == "/nick":
            oldname = name
            name = message[6:]
            if oldname==name:
                err="You are already known as "+name+".\n"
                self.messaging_field.config(state=NORMAL)
                self.messaging_field.insert(END, err)
                self.messaging_field.yview_moveto(1.0)
                self.messaging_field.config(state=DISABLED)
                pass
            else:
                messages=oldname+" changed their nick to "+name+"."
                tcpCliSock.send(messages)
        elif message [:1] == "/":
            err=message+" - command not found\n"
            self.messaging_field.config(state=NORMAL)
            self.messaging_field.insert(END, err)
            self.messaging_field.yview_moveto(1.0)
            self.messaging_field.config(state=DISABLED)
        elif message == "":
            pass
        else:
            messages = name + ": " + message
            tcpCliSock.send(messages)
        self.entry_field.delete(0, END)

    def create_widgets(self):
        self.scrollingbar = Scrollbar(self)
        self.scrollingbar.pack(side=RIGHT, fill=Y)
        
        self.messaging_field = Text(self, wrap = WORD, font="Arial 10 normal", state=DISABLED)
        self.messaging_field.pack({"side": "top"}, expand=YES, fill=BOTH)

        self.entry_field = Entry(self, font="Arial 10 normal")
        self.entry_field.pack({"side": "bottom"}, expand=YES, fill=BOTH)
        self.entry_field.bind('<Return>', self.callback)
        
        self.messaging_field.config(yscrollcommand=self.scrollingbar.set)
        self.scrollingbar.config(command=self.messaging_field.yview)

    def add(self, data):
        self.messaging_field.config(state=NORMAL)
        self.messaging_field.insert(END, data)
        self.messaging_field.yview_moveto(1.0)
        self.messaging_field.config(state=DISABLED)
        print data[:-1]

    def socket(self):
        def loop0():
            while 1:
                data = tcpCliSock.recv(BUFSIZE)
                if data: self.add(data)

        thread.start_new_thread(loop0, ())



root = Tk()
root.resizable(0,0)
root.title("Chat client")

app = Application(root)

root.mainloop()
