import socket
import threading
import tkinter as tk
from tkinter import scrolledtext, simpledialog

class ChatClient:
    def __init__(self):
        self.username = self.get_username()
        self.init_gui()
        self.connect_to_server()

    def get_username(self):
        root = tk.Tk()
        root.withdraw()
        username = simpledialog.askstring("Username", "Enter your username:")
        root.destroy()
        return username

    def init_gui(self):
        self.root = tk.Tk()
        self.root.title(f"ChatApp - {self.username}")

        self.message_display = scrolledtext.ScrolledText(self.root, wrap=tk.WORD)
        self.message_display.config(state = "disabled")
        self.message_display.pack(expand=True, fill=tk.BOTH)

        self.message_entry = tk.Entry(self.root)
        self.message_entry.pack(expand=True, fill=tk.BOTH)

        self.message_entry.bind("<Return>", self.send_message)

    def connect_to_server(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect(('localhost', 5555))
        self.client.send(self.username.encode('utf-8'))

        receive_thread = threading.Thread(target=self.receive_messages)
        receive_thread.start()

        self.root.mainloop()

    def send_message(self, event):
        message = self.message_entry.get()
        self.client.send(message.encode('utf-8'))
        self.message_entry.delete(0, tk.END)

    def receive_messages(self):
        while True:
            try:
                data = self.client.recv(1024)
                if not data:
                    break

                message = data.decode('utf-8')
                self.message_display.config(state = "normal")
                self.message_display.insert(tk.END, message + '\n')
                self.message_display.yview(tk.END)
                self.message_display.config(state = "disabled")

            except Exception as e:
                print(f"Error receiving message: {e}")
                break

chat_client = ChatClient()
