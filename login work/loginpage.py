from tkinter import *


#functions for login,resgister
def login():
    c=0
    print("working on")
    status=Label(root,text="Loging in...........")
    status.pack(side="bottom",fill=X)
    root.after(5000,lambda:status.destroy())
def resgister_ui():
    resg=Tk()
    resg.title("Resgister")
    
    resg.resizable(False,False)

    resg_label=Label(resg,text="Register",bg="lightblue",font=("Arial",20,"bold"))
    resg_label.grid(row=0, column=1, columnspan=2, pady=10)
    userR_label=Label(resg,text="Username",bg="lightblue",font=("Arial",12))
    userR_entry = Entry(resg,bd=5,font=("Arial",14,"bold"),highlightbackground="black",justify="center")
    userR_label.grid(row=3, column=0, padx=5, pady=5, sticky="E")
    userR_entry.grid(row=3, column=1, padx=5, pady=5, sticky="W")

    passR_label=Label(resg,text="Passcode",bg="lightblue",font=("Arial",12))
    passR_entry = Entry(resg,bd=5,font=("Arial",14,"bold"),highlightbackground="black",justify="center")
    passR_label.grid(row=4, column=0, padx=5, pady=5, sticky="E")
    passR_entry.grid(row=4, column=1, padx=5, pady=5, sticky="W")

      

root =Tk()

root.title("Login")
root.geometry("800x600")
root.resizable(False,False)
#background
background =PhotoImage(file="librarybg.png")
backgroundlabel =Label(root,image=background)
backgroundlabel.image=background
backgroundlabel.place(relwidth=1,relheight=1)

#----login desgin----
login_frame = Frame(root, bg="lightblue", bd=5)
login_frame.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.5, relheight=0.5)

login_label=Label(login_frame,text="LOGIN",bg="lightblue",font=("Arial",20,"bold"))
login_label.grid(row=0, column=1, columnspan=2, pady=10)
#radiobutton work
role=StringVar(value="user")
admin_radio=Radiobutton(login_frame,text="Admin",variable=role,value="admin",bg="lightblue")
admin_radio.grid(row=2,column=0,padx=10)
user_radio=Radiobutton(login_frame,text="User",variable=role,value="user",bg="lightblue")
user_radio.grid(row=2,column=1)
#entry work
user_label=Label(login_frame,text="Username",bg="lightblue",font=("Arial",12))
user_entry = Entry(login_frame,bd=5,font=("Arial",14,"bold"),highlightbackground="black",justify="center")
user_label.grid(row=3, column=0, padx=5, pady=5, sticky="E")
user_entry.grid(row=3, column=1, padx=5, pady=5, sticky="W")

pass_label=Label(login_frame,text="Passcode",bg="lightblue",font=("Arial",12))
pass_entry = Entry(login_frame,bd=5,font=("Arial",14,"bold"),highlightbackground="black",justify="center")
pass_label.grid(row=4, column=0, padx=5, pady=5, sticky="E")
pass_entry.grid(row=4, column=1, padx=5, pady=5, sticky="W")


#button
login_button=Button(login_frame,text="Login?",font=("Arial",12,"bold"),command=login,bg="blue",relief="raised")
login_button.grid(row=5,column=1)

resgister_button=Button(login_frame,text="Resgister",font=("Arial",12,"bold"),bg="blue",relief="raised",command=resgister_ui)
resgister_button.grid(row=6,column=1)
#status bar





root.mainloop()