from tkinter import *


#functions for login

root =Tk()

root.title("Login")
root.geometry("800x600")
#background
background =PhotoImage(file="librarybg.png")
backgroundlabel =Label(root,image=background)
backgroundlabel.place(relwidth=1,relheight=1)

#----login desgin----
login_frame = Frame(root,bg="red",bd=5)
login_frame.place(relx=0.5)

print("new")




root.mainloop()