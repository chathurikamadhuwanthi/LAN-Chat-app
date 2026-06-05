from tkinter import *
from tkinter import messagebox
import sqlite3

from register import open_register_window
from chat_window import open_chat_window

def login():
    username = username_entry.get()
    password = password_entry.get()

    conn = sqlite3.connect("chat.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM users WHERE username=? AND password=?",
        (username, password)
    )

    user = cursor.fetchone()
    conn.close()

    if user:
        root.destroy()
        open_chat_window(username)
    else:
        messagebox.showerror("Error", "Invalid Username or Password")

root = Tk()
root.title("NodeTalk Login")
root.geometry("470x420")   # slightly larger window
root.configure(bg="#E6E6FA")  # background lavender

# HEADER
Label(
    root,
    text="NodeTalk Login",
    font=("Arial", 20, "bold"),
    bg="#E6E6FA",
    fg="black"
).pack(pady=20)

# USERNAME
Label(root, text="Username", bg="#E6E6FA", fg="black", font=("Arial", 12)).pack(pady=5)
username_entry = Entry(root, bg="#800080", fg="white", insertbackground="white", font=("Arial", 12))
username_entry.pack(ipady=6, pady=5)   # increased height with ipady

# PASSWORD
Label(root, text="Password", bg="#E6E6FA", fg="black", font=("Arial", 12)).pack(pady=5)
password_entry = Entry(root, show="*", bg="#800080", fg="white", insertbackground="white", font=("Arial", 12))
password_entry.pack(ipady=6, pady=5)   # increased height with ipady

# LOGIN BUTTON
Button(
    root,
    text="Login",
    width=18,
    height=1,
    bg="#800080",
    fg="white",
    font=("Arial", 12, "bold"),
    command=login
).pack(pady=15)

# REGISTER SECTION
Label(
    root,
    text="Don't have an account?",
    bg="#E6E6FA",
    fg="black",
    font=("Arial", 11)
).pack(pady=5)

Button(
    root,
    text="Register",
    width=18,
    height=1,
    bg="#800080",
    fg="white",
    font=("Arial", 12, "bold"),
    command=open_register_window
).pack(pady=5)

root.mainloop()
