import socket
from tkinter import *
import threading

root = Tk()
root.minsize(640, 400)
root.maxsize(800, 640)



# Frame switchers
def to_connection():
    connection.grid()

def to_main():
    connection.grid_forget()

# Functions
cl = None

def submission():
    global cl
    ip_num = ip_ent.get()
    port_num = int(port_ent.get())
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((ip_num, port_num))
    cl = client
    threading.Thread(target=receive_msg, args=()).start()

def send_msg(client):
    msg = msg_ent.get()        
    client.send(msg.encode('utf-8'))

def receive_msg():
    ip_server = ip_ent.get()
    port_num = int(port_ent.get())
    from_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    from_server.connect((ip_server, port_num))
    while True:
        msg_ = from_server.recv(1024).decode('utf-8')
        all_messages.insert(END, '\n' + msg_)
        all_messages.update()
        # print('Server: ' + msg_) # for debugging purposes

# Frames
connection = Frame(root)
texting = Frame(connection)

frame_lst = [connection, root]
for frame in frame_lst:
    for i in range(100):
        frame.grid_rowconfigure(i, minsize=20)
        frame.grid_columnconfigure(i, minsize=100)



# root
root_msg = Label(root, text='Welcome to Huzaifas and Rayans App')
root_msg.grid(row=0, column=3)

# connection
main_msg = Label(connection, text='Enter IP and PORT')
ip_label = Label(connection, text='Enter IP')
port_label = Label(connection, text='Enter PORT')

ip_ent = Entry(connection)
port_ent = Entry(connection)

main_msg.grid(row=1, column=3)
ip_label.grid(row=2, column=3)
ip_ent.grid(row=2, column=4)
port_label.grid(row=3, column=3)
port_ent.grid(row=3, column=4)

# texting
msg_ent = Entry(texting, width=50)
msg_ent.insert(0, "Enter any Text")
msg_ent.grid(row=10, column=2)

all_messages = Text(texting, width=25, height=15)
all_messages.grid(row=1, column=2, columnspan=1)

# btn to change
btn_to_connection = Button(root, text='Switch to connection', command=to_connection)
btn_to_connection.grid(column=3)

btn_to_root = Button(connection, text='Go to Main', command=to_main)
btn_to_root.grid(row=0, column=3)

# btn for submit ip and port number
submit = Button(connection, text='Connect and Text', command=submission)
submit.grid(row=4, column=4)

# btn for msg send
send = Button(texting, text='Send', command=lambda: send_msg(cl))
send.grid(row=11, column=2)

# Pack the frames
texting.grid()
to_main()

root.mainloop()
