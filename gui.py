import sqlite3
import tkinter as tk
from tkinter import messagebox

# Store all users
users = {}

# Current logged in user
current_user = None


# BANK ACCOUNT CLASS
class BankAccount:

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.balance = 0
        self.history = []

    def deposit(self, amount):
        self.balance += amount
        self.history.append(f"Deposited ₹{amount}")

    def withdraw(self, amount):

        if amount > self.balance:
            return "Insufficient Balance"

        self.balance -= amount
        self.history.append(f"Withdrawn ₹{amount}")

    def check_balance(self):
        return self.balance


# REGISTER FUNCTION
def register():

    username = username_entry.get()
    password = password_entry.get()

    if username == "" or password == "":
        messagebox.showerror("Error", "Fields cannot be empty")
        return

    if username in users:
        messagebox.showerror("Error", "Username already exists")

    else:
        users[username] = BankAccount(username, password)
    conn = sqlite3.connect("bank.db")

    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO users VALUES (?, ?, ?)",
        (username, password, 0)
    )

    conn.commit()

    conn.close()

    messagebox.showinfo(
        "Success",
        "Account Created Successfully"
    )

    username_entry.delete(0, tk.END)
    password_entry.delete(0, tk.END)


# LOGIN FUNCTION
def login():

    global current_user

    username = username_entry.get()
    password = password_entry.get()

    if username in users and users[username].password == password:

        current_user = users[username]

        messagebox.showinfo(
            "Success",
            f"Welcome {username}"
        )

        open_dashboard()

    else:
        messagebox.showerror(
            "Error",
            "Invalid Username or Password"
        )


# DASHBOARD WINDOW
def open_dashboard():

    dashboard = tk.Toplevel(root)

    dashboard.title("Bank Dashboard")
    dashboard.geometry("500x500")
    dashboard.configure(bg="white")

    # TITLE
    tk.Label(
        dashboard,
        text=f"Welcome {current_user.username}",
        font=("Arial", 20, "bold"),
        bg="white",
        fg="darkblue"
    ).pack(pady=20)

    # AMOUNT LABEL
    tk.Label(
        dashboard,
        text="Enter Amount",
        font=("Arial", 14),
        bg="white"
    ).pack()

    # AMOUNT ENTRY
    amount_entry = tk.Entry(
        dashboard,
        font=("Arial", 14),
        width=20
    )

    amount_entry.pack(pady=10)

    # DEPOSIT FUNCTION
    def deposit_money():

        try:

            amount = float(amount_entry.get())

            if amount <= 0:
                messagebox.showerror(
                    "Error",
                    "Amount must be positive"
                )
                return

            current_user.deposit(amount)

            messagebox.showinfo(
                "Success",
                f"₹{amount} Deposited Successfully"
            )

            amount_entry.delete(0, tk.END)

        except:
            messagebox.showerror(
                "Error",
                "Invalid Input"
            )

    # WITHDRAW FUNCTION
    def withdraw_money():

        try:

            amount = float(amount_entry.get())

            if amount <= 0:
                messagebox.showerror(
                    "Error",
                    "Amount must be positive"
                )
                return

            result = current_user.withdraw(amount)

            if result == "Insufficient Balance":

                messagebox.showerror(
                    "Error",
                    result
                )

            else:

                messagebox.showinfo(
                    "Success",
                    f"₹{amount} Withdrawn Successfully"
                )

            amount_entry.delete(0, tk.END)

        except:
            messagebox.showerror(
                "Error",
                "Invalid Input"
            )

    # CHECK BALANCE
    def check_balance():

        balance = current_user.check_balance()

        messagebox.showinfo(
            "Current Balance",
            f"₹{balance}"
        )

    # SHOW HISTORY
    def show_history():

        if len(current_user.history) == 0:

            messagebox.showinfo(
                "Transaction History",
                "No Transactions Yet"
            )

        else:

            history = "\n".join(current_user.history)

            messagebox.showinfo(
                "Transaction History",
                history
            )

    # BUTTONS
    tk.Button(
        dashboard,
        text="Deposit",
        command=deposit_money,
        bg="green",
        fg="white",
        font=("Arial", 12),
        width=20,
        height=2
    ).pack(pady=10)

    tk.Button(
        dashboard,
        text="Withdraw",
        command=withdraw_money,
        bg="red",
        fg="white",
        font=("Arial", 12),
        width=20,
        height=2
    ).pack(pady=10)

    tk.Button(
        dashboard,
        text="Check Balance",
        command=check_balance,
        bg="blue",
        fg="white",
        font=("Arial", 12),
        width=20,
        height=2
    ).pack(pady=10)

    tk.Button(
        dashboard,
        text="Transaction History",
        command=show_history,
        bg="purple",
        fg="white",
        font=("Arial", 12),
        width=20,
        height=2
    ).pack(pady=10)


# MAIN WINDOW
root = tk.Tk()

root.title("Online Banking System")
root.geometry("500x500")
root.configure(bg="lightblue")

# TITLE
tk.Label(
    root,
    text="Online Banking System",
    font=("Arial", 22, "bold"),
    bg="lightblue",
    fg="darkblue"
).pack(pady=20)

# USERNAME LABEL
tk.Label(
    root,
    text="Username",
    font=("Arial", 14),
    bg="lightblue"
).pack()

# USERNAME ENTRY
username_entry = tk.Entry(
    root,
    font=("Arial", 14),
    width=25
)

username_entry.pack(pady=10)

# PASSWORD LABEL
tk.Label(
    root,
    text="Password",
    font=("Arial", 14),
    bg="lightblue"
).pack()

# PASSWORD ENTRY
password_entry = tk.Entry(
    root,
    show="*",
    font=("Arial", 14),
    width=25
)

password_entry.pack(pady=10)

# REGISTER BUTTON
tk.Button(
    root,
    text="Register",
    command=register,
    bg="green",
    fg="white",
    font=("Arial", 12),
    width=20,
    height=2
).pack(pady=10)

# LOGIN BUTTON
tk.Button(
    root,
    text="Login",
    command=login,
    bg="blue",
    fg="white",
    font=("Arial", 12),
    width=20,
    height=2
).pack(pady=10)

# RUN APPLICATION
root.mainloop()