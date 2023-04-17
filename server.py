import tkinter as tk
import socket
import threading
global mss
cl = None
root = tk.Tk()
root.geometry("640x640")

main_frame = tk.Frame(root)
text_screen = tk.Frame(root)
chats_screen = tk.Frame(text_screen)

main_frame.grid()
frame_lst = [main_frame, text_screen, chats_screen]
for frame in frame_lst:
    for i in range(7):
        frame.grid_rowconfigure(i, minsize=50)
        frame.grid_columnconfigure(i, minsize=100)

clients = []

def handle_client(client):
    while True:
        msg = client.recv(1024).decode('utf-8')
        if not msg:
            break
        print('Client: ' + str(ip_ent.get()) +': ' + msg)
        for c in clients:
            if c != client:
                c.send(msg.encode('utf-8'))
        all_messages.insert(tk.END, "\n" + msg)
        all_messages.update()
    clients.remove(client)

def connect_to_client():
    global cl
    ip_num = ip_ent.get()
    port = int(server_port_ent.get())
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((ip_num, port))
    print('Connected to: ' + str(ip_num))
    cl = client

def send_to_client():
    global mss
    mss = msg_ent.get()
    cl.send(mss.encode('utf-8'))
    print('Sent!!!')
def connect():
    global ip, port
    ip = ip_ent.get()
    port = int(port_ent.get())
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server.bind((ip, port))
    server.listen(5)
    main_frame.grid_forget()
    text_screen.grid(row=0, column=0)
    chats_screen.grid(row=1, column=0)

    all_messages.config(yscrollcommand=scrollbar.set)

    def accept_clients():
        while True:
            client, addr = server.accept()

            clients.append(client)
            t = threading.Thread(target=handle_client, args=(client,))
            t.start()
    t = threading.Thread(target=accept_clients)
    t.start()

def quit():
    root.destroy()

title = tk.Label(main_frame, text='Welcome to Huzaifas and Rayans App')
title.grid(row=0, column=2)

t_screen = tk.Label(text_screen, text='Chatting')
t_screen.grid(row=0, column=0)

all_messages = tk.Text(chats_screen, width=25, height=15)
all_messages.grid(row=1, column=2, columnspan=1)

msg_ent = tk.Entry(chats_screen)
server_port_ent = tk.Entry(chats_screen)

msg_ent.insert(0, "Enter any Text")
msg_ent.grid(row=3, column=2)

server_port_ent.insert(0, "Enter any Port")
server_port_ent.grid(row=2, column=2)

server_port_btn = tk.Button(chats_screen,text='Connect to Port', command=connect_to_client)
server_port_btn.grid(row=2, column=4)

msg_send_btn = tk.Button(chats_screen,text='Send Message', command=send_to_client)
msg_send_btn.grid(row=3, column=4)

scrollbar = tk.Scrollbar(chats_screen, command=all_messages.yview)
scrollbar.grid()

ip_label = tk.Label(main_frame, text='Enter IP')
port_label = tk.Label(main_frame, text='Enter PORT')

ip_ent = tk.Entry(main_frame)
port_ent = tk.Entry(main_frame)

ip_label.grid(row=1, column=1)
ip_ent.grid(row=1, column=2)
port_label.grid(row=2, column=1)
port_ent.grid(row=2, column=2)

btn_connect = tk.Button(main_frame, text='Connect', command=connect)
btn_connect.grid(row=3, column=2)

btn_quit = tk.Button(main_frame, text='Quit', command=quit)
btn_quit.grid(row=3, column=3)

root.mainloop()
