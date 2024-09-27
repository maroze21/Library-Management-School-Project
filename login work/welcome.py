from tkinter import *
import subprocess as sp

# Function to run the login page
def on_log():
    root.destroy()
    sp.run(["python", "loginpage.py"])

root = Tk()
root.title("Library Management")
root.geometry("800x600")
root.resizable(False, False)

# Set background image
try:
    background1 = PhotoImage(file="librarybg.png")
    backgroundlabel = Label(root, image=background1)

    backgroundlabel.place(relwidth=1, relheight=1)

except EXCEPTION as e:
    print("load error")

label = Label(root, text="Welcome to the Library Management System", font=("New Amsterdam", 20, "bold"),bg="black",fg="white")
label.place(relx=0.5, rely=0.4, anchor="center")

# Create login button
login_button = Button(root, text="OPEN",bg="black",fg="white", command=on_log,font=("New Amsterdam", 12, "bold"))
login_button.place(relx=0.5, rely=0.5, anchor="center")

root.mainloop()
