from tkinter import *
from tkinter import messagebox
import sqlite3

def open_register_window():

    register_window = Toplevel()

    register_window.title("Register")
    register_window.geometry("350x300")
    register_window.configure(bg="#E6E6FA")  # background color

    # TITLE
    Label(
        register_window,
        text="Create Account",
        bg="#E6E6FA",
        fg="black",
        font=("Arial", 14, "bold")
    ).pack(pady=10)

    # USERNAME
    Label(
        register_window,
        text="Username",
        bg="#E6E6FA"
    ).pack(pady=5)

    username_entry = Entry(
        register_window,
        bg="#800080",
        fg="white",
        insertbackground="white"
    )
    username_entry.pack(ipady=5)

    # PASSWORD
    Label(
        register_window,
        text="Password",
        bg="#E6E6FA"
    ).pack(pady=5)

    password_entry = Entry(
        register_window,
        show="*",
        bg="#800080",
        fg="white",
        insertbackground="white"
    )
    password_entry.pack(ipady=5)

    def register():

        username = username_entry.get()
        password = password_entry.get()

        if username == "" or password == "":
            messagebox.showerror("Error", "All fields are required")
            return

        conn = sqlite3.connect("chat.db")
        cursor = conn.cursor()

        try:
            cursor.execute(
                "INSERT INTO users(username,password) VALUES (?,?)",
                (username, password)
            )

            conn.commit()

            messagebox.showinfo("Success", "Registration Successful")
            register_window.destroy()

        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Username already exists")

        conn.close()

    Button(
        register_window,
        text="Register",
        command=register,
        bg="#800080",
        fg="white",
        font=("Arial", 10, "bold")
    ).pack(pady=20)


if __name__ == "__main__":

    root = Tk()
    root.withdraw()

    open_register_window()

    root.mainloop()