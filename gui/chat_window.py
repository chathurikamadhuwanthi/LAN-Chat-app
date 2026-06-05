from tkinter import *
from tkinter import filedialog, messagebox, Toplevel
import sqlite3
import os
import shutil
import sys

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
import client


def save_message(sender, message):
    conn = sqlite3.connect("chat.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS messages(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sender TEXT,
            message TEXT
        )
    """)
    cursor.execute("INSERT INTO messages(sender,message) VALUES (?,?)", (sender, message))
    conn.commit()
    conn.close()


def open_chat_window(username):
    root = Tk()
    root.title(f"NodeTalk - {username}")
    root.geometry("700x500")
    root.configure(bg="white")  # app background white

    # MAIN HEADER
    header = Label(root, text="NodeTalk", font=("Arial", 20, "bold"),
                   bg="#800080", fg="white", pady=5)
    header.pack(fill=X)

    try:
        client.connect("127.0.0.1", username)
    except:
        messagebox.showerror("Error", "Start server first")
        return

    # MAIN FRAME (Online Users + Chat side by side)
    main_frame = Frame(root, bg="white")
    main_frame.pack(fill=BOTH, expand=True)

    # LEFT: Online Users
    users_frame = Frame(main_frame, bg="#E6E6FA", width=200, height=300)
    users_frame.pack(side=LEFT, fill=Y, padx=5, pady=5)
    users_frame.pack_propagate(False)

    users_list = Listbox(users_frame, font=("Arial", 11), bg="#E6E6FA", fg="black")
    users_list.pack(fill=BOTH, expand=True)

    # RIGHT: Chat
    chat_frame = Frame(main_frame, bg="#E6E6FA", width=480, height=300)
    chat_frame.pack(side=RIGHT, fill=BOTH, expand=True, padx=5, pady=5)
    chat_frame.pack_propagate(False)

    chat_box = Text(chat_frame, font=("Arial", 11), wrap=WORD, bg="#E6E6FA", fg="black")
    chat_box.pack(fill=BOTH, expand=True)

    scrollbar = Scrollbar(chat_frame, command=chat_box.yview)
    chat_box.config(yscrollcommand=scrollbar.set)
    scrollbar.pack(side=RIGHT, fill=Y)

    # MESSAGE ENTRY (full width under both boxes)
    message_frame = Frame(root, bg="#E6E6FA", height=40)
    message_frame.pack(fill=X, padx=5, pady=5)
    message_entry = Entry(message_frame, font=("Arial", 11), bg="#E6E6FA", fg="black")
    message_entry.pack(fill=X, expand=True, padx=5, ipady=6)

    # BUTTON ROW
    button_frame = Frame(root, bg="white")
    button_frame.pack(fill=X, pady=10)

    def clear_chat():
        chat_box.delete("1.0", END)

    def send_msg():
        msg = message_entry.get()
        if msg == "":
            return
        try:
            selected_user = users_list.get(users_list.curselection())
            client.send(f"PRIVATE:{selected_user}:{msg}")
        except:
            client.send(msg)
        save_message(username, msg)
        message_entry.delete(0, END)
        # Removed manual chat_box.insert to avoid double messages

    def choose_file():
        file = filedialog.askopenfilename()
        if not file:
            return
        if not os.path.exists("uploads"):
            os.makedirs("uploads")
        name = os.path.basename(file)
        shutil.copy(file, "uploads/" + name)
        client.send(f"[FILE SHARED] {name}")

    def open_sticker_window():
        sticker_win = Toplevel(root)
        sticker_win.title("Stickers")
        sticker_win.geometry("220x120")
        sticker_win.configure(bg="white")

        def send_sticker(sticker):
            client.send(f"[STICKER] {sticker}")
            sticker_win.destroy()

        Button(sticker_win, text="❤️", bg="red", fg="white",
               command=lambda: send_sticker("❤️"), width=8, height=3).pack(side=LEFT, padx=5, pady=10)
        Button(sticker_win, text="👍", bg="green", fg="white",
               command=lambda: send_sticker("👍"), width=8, height=3).pack(side=LEFT, padx=5, pady=10)
        Button(sticker_win, text="🙂", bg="yellow", fg="black",
               command=lambda: send_sticker("🙂"), width=8, height=3).pack(side=LEFT, padx=5, pady=10)

    def leave_chat():
        try:
            client.send(f"{username} has left the chat.")
        except:
            pass
        root.destroy()

    Button(button_frame, text="Clear Chat", bg="#800080", fg="white",
           command=clear_chat, width=15, height=2).pack(side=LEFT, padx=10)
    Button(button_frame, text="⋮", bg="#800080", fg="white",
           command=open_sticker_window, width=5, height=2).pack(side=LEFT, padx=10)
    Button(button_frame, text="File", bg="#800080", fg="white",
           command=choose_file, width=15, height=2).pack(side=LEFT, padx=10)
    Button(button_frame, text="Send", bg="#800080", fg="white",
           command=send_msg, width=15, height=2).pack(side=LEFT, padx=10)
    Button(button_frame, text="Leave", bg="#800080", fg="white",
           command=leave_chat, width=15, height=2).pack(side=LEFT, padx=10)

    # LOAD HISTORY
    def load_history():
        conn = sqlite3.connect("chat.db")
        cursor = conn.cursor()
        cursor.execute("SELECT sender,message FROM messages")
        for sender, message in cursor.fetchall():
            chat_box.insert(END, f"{sender}: {message}\n")
        conn.close()

    # MESSAGE HANDLER
    def show_message(message):
        if message.startswith("USERS:"):
            users_list.delete(0, END)
            users = message.replace("USERS:", "").split(",")
            for u in users:
                if u:
                    users_list.insert(END, f"🔵 {u[0].upper()}  {u}")
            return
        chat_box.insert(END, f"{message}\n")
        chat_box.see(END)

    client.start_listening(show_message)
    load_history()
    root.mainloop()



  
