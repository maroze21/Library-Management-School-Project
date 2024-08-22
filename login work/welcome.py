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
background = PhotoImage(file="librarybg.png")
backgroundlabel = Label(root, image=background)
backgroundlabel.place(relwidth=1, relheight=1)

# Create a label that will "blend" with the background image
label = Label(root, text="Welcome to the Library Management System", font=("New Amsterdam", 20, "bold"))
label.place(relx=0.5, rely=0.4, anchor="center")

# Create login button
login_button = Button(root, text="open", command=on_log,font=("New Amsterdam", 12, "bold"))
login_button.place(relx=0.5, rely=0.5, anchor="center")

root.mainloop()
