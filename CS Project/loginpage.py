from tkinter import *
import tkinter.messagebox as messagebox
import subprocess as sp
import mysql.connector as mc

con = mc.connect(host='localhost',user='root',password='root',charset='utf8')
cur = con.cursor()

cur.execute("create database if not exists Library")
cur.execute("use Library")
cur.execute("create table if not exists Members(UserName varchar(20), Password varchar(10))")

#main function

    
def openmember():
    sp.run(['python','member.py'])
def login():
    useid= user_entry.get()
    passw=pass_entry.get()
    if useid.lower()=="admin" and passw.lower()=="nothing":
        
        login_status()
        
        root.after(2100,root.destroy())
        root.after(2100,lambda:sp.run(["python","adminpg.py" ]))
    else:
        ask="select * from Members where UserName=%s and Password=%s"
        cur.execute(ask,(useid,passw))
        result=cur.fetchone()
        if result :
            messagebox.showinfo("Login"," Login is Successful ")
            root.after(2100,root.destroy())
            root.after(2000,openmember)
        else:
            messagebox.showerror("ERROR","Invalid UserName or Passcode")

    

#functions for login,resgister  

def login_status():
    c=0
    print("working on")
    status=Label(root,text="Loging in...........")
    status.pack(side="bottom",fill=X)
    root.after(2000,lambda:status.destroy())

def register_ui():
    usernameR = user_entry.get()
    passwsd = pass_entry.get()

    if usernameR != "admin" and passwsd != "nothing":
        global userR_entry,passR_entry,passccR_entry
        resg=Tk()
        resg.title("Register")
        resg.geometry("600x350")

        resg_label=Label(resg,text="Register",bg="lightblue",font=("Arial",20,"bold"))
        resg_label.grid(row=0, column=1, columnspan=2, pady=10)
        userR_label=Label(resg,text="Username",bg="lightblue",font=("Arial",12))
        userR_entry = Entry(resg,bd=5,font=("Arial",14,"bold"),highlightbackground="black",justify="center")
        userR_label.grid(row=3, column=0, padx=5, pady=5, sticky="E")
        userR_entry.grid(row=3, column=1, padx=5, pady=5, sticky="W")

        passR_label=Label(resg,text="Passcode",bg="lightblue",font=("Arial",12))
        passR_entry = Entry(resg,bd=5,font=("Arial",14,"bold"),highlightbackground="black",justify="center",show="#")
        passR_label.grid(row=4, column=0, padx=5, pady=5, sticky="E")
        passR_entry.grid(row=4, column=1, padx=5, pady=5, sticky="W")


        passccR_label=Label(resg,text="Confirm Passcode",bg="lightblue",font=("Arial",12))
        passccR_entry = Entry(resg,bd=5,font=("Arial",14,"bold"),highlightbackground="black",justify="center",show="#")
        passccR_label.grid(row=5, column=0, padx=5, pady=5, sticky="E")
        passccR_entry.grid(row=5, column=1, padx=5, pady=5, sticky="W")
        

        resg_button=Button(resg,text="Register",font=("Arial",12,"bold"),bg="blue",relief="raised",command=onClick)
        resg_button.grid(row=6,column=1)
        
def onClick():
    usernameR = userR_entry.get()
    passwsd = passR_entry.get()
    cpassword = passccR_entry.get()
    if passwsd == cpassword:
        qry = "INSERT INTO Members (UserName, Password) VALUES (%s, %s)"
        cur.execute(qry, (usernameR, passwsd))
        con.commit()  
        messagebox.showinfo("Success", "Registration Successful!")
    else:
        messagebox.showerror("Error", "Passwords do not match!")


root =Tk()

root.title("Login")
root.geometry("800x600")
root.resizable(False,False)
#background
#had to give this big path as it was not recognizging image pos
background = PhotoImage(file="librarybg.png")

backgroundlabel =Label(root,image=background)
backgroundlabel.image=background
backgroundlabel.place(relwidth=1,relheight=1)

#----login desgin----
login_frame = Frame(root, bg="black", bd=6)
login_frame.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.5, relheight=0.5)

login_label=Label(login_frame,text="LOGIN",bg="black",fg="white",font=("Georgia",20,"bold"))
login_label.grid(row=0, column=1, columnspan=2, pady=10)

#entry work
user_label=Label(login_frame,text="Username",bg="black",fg="white",font=("Arial",12),relief="raised")
user_entry = Entry(login_frame,bd=5,font=("Arial",14,"bold"),highlightbackground="black",justify="center")
user_label.grid(row=3, column=0, padx=5, pady=5, sticky="E")
user_entry.grid(row=3, column=1, padx=5, pady=5, sticky="W")

pass_label=Label(login_frame,text="Passcode",bg="black",fg="white",font=("Arial",12),relief="raised")
pass_entry = Entry(login_frame,bd=5,font=("Arial",14,"bold"),highlightbackground="black",justify="center",show="*",)
pass_label.grid(row=4, column=0, padx=5, pady=5, sticky="E")
pass_entry.grid(row=4, column=1, padx=5, pady=5, sticky="W")

#button
login_button=Button(login_frame,text="Login",font=("Arial",12,"bold"),command=login,bg="black",fg="white",relief="raised")
login_button.grid(row=5,column=1,pady=7)

register_label=Label(login_frame,text="Don't have an account?",bg="black",fg="white",font=("Georgia",15))
register_label.grid(row=8,column=1,pady=5)
resgister_button=Button(login_frame,text="Register",font=("Arial",12,"bold"),bg="black",fg="white",relief="raised",command=register_ui)
resgister_button.grid(row=9,column=1)

root.mainloop()