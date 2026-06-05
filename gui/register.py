from tkinter import *
from tkinter import messagebox
import sqlite3

def open_register_window():

    register_window = Toplevel()

    register_window.title("Register")
    register_window.geometry("300x250")

    Label(register_window, text="Username").pack(pady=5)

    username_entry = Entry(register_window)
    username_entry.pack()

    Label(register_window, text="Password").pack(pady=5)

    password_entry = Entry(register_window, show="*")
    password_entry.pack()

    def register():

        username = username_entry.get()
        password = password_entry.get()

        if username == "" or password == "":
            messagebox.showerror(
                "Error",
                "All fields are required"
            )
            return

        conn = sqlite3.connect("chat.db")
        cursor = conn.cursor()

        try:

            cursor.execute(
                "INSERT INTO users(username,password) VALUES (?,?)",
                (username, password)
            )

            conn.commit()

            messagebox.showinfo(
                "Success",
                "Registration Successful"
            )

            register_window.destroy()

        except sqlite3.IntegrityError:

            messagebox.showerror(
                "Error",
                "Username already exists"
            )

        conn.close()

    Button(
        register_window,
        text="Register",
        command=register
    ).pack(pady=20)


if __name__ == "__main__":

    root = Tk()
    root.withdraw()

    open_register_window()

    root.mainloop()