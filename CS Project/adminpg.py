from tkinter import *
from tkinter import ttk
import mysql.connector as sql
import tkinter.messagebox as messagebox


mycon=sql.connect(host='localhost',username='root',password='root',database='library_management')
mycur=mycon.cursor()
#functions to search ,add ,delete,modify
def search_window():
    search = Toplevel(root)
    search.title("Search Books")
    search.geometry("800x400")
    search.configure(bg="lightblue")

    Label(search,text="Search Books").pack(pady=5)
    search_entry=Entry(search)
    search_entry.pack(pady=5)

    def addBooks():
        #mysql
        searchdt=search_entry.get().lower()
        m="SELECT * FROM books WHERE book_name=%s"
        mycur.execute(m,(searchdt,))
        result=mycur.fetchone()

        for item in tree.get_children():
            tree.delete(item)

        if result:
            tree.insert('',"end",values=result)
        else:
            messagebox.showerror("ERROR","No book found")
            
    columns = ("ID", "Title" ,"Cost","Author", "Genre", "Availability")
    tree = ttk.Treeview(search, columns=columns, show='headings')

    #search button
    Button(search,text="Search",anchor="center",relief="groove",command=addBooks).pack(pady=5)
    for col in columns:
        tree.heading(col,text=col)
        tree.column(col,anchor=CENTER,width=100)
    tree.pack(fill=BOTH,expand=True)


def view_window():
    view =Toplevel(root)
    view.title("View Books")
    view.geometry("800x400")
    view.configure(bg="lightblue")
    
    columns = ("ID", "Title" ,"Cost", "Availability","Author", "Genre",)
    tree = ttk.Treeview(view, columns=columns, show='headings')
    
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, anchor='center', width=100)
    
    scrollbar = Scrollbar(view, orient="vertical", command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    scrollbar.pack(side=RIGHT, fill=Y)
    
    ask="select * from books"
    mycur.execute(ask)
    result=mycur.fetchall()
    
    for item in result:
        tree.insert('', 'end', values=item)
    
    tree.pack(fill=BOTH, expand=True)



def add_window():
    addw = Toplevel(root)
    addw.title("Add Book")
    addw.geometry("600x500")
    addw.configure(bg="lightgreen")

    Label(addw, text="BookID:", bg="lightgreen").pack(pady=5)
    bookid_entry = Entry(addw)
    bookid_entry.pack(pady=5)
    
    Label(addw, text="Title:", bg="lightgreen").pack(pady=5)
    title_entry = Entry(addw)
    title_entry.pack(pady=5)

    Label(addw, text="Cost", bg="lightgreen").pack(pady=5)
    Cost_entry = Entry(addw)
    Cost_entry.pack(pady=5)
    
    Label(addw, text="Author:", bg="lightgreen").pack(pady=5)
    author_entry = Entry(addw)
    author_entry.pack(pady=5)
    
    Label(addw, text="Genre:", bg="lightgreen").pack(pady=5)
    genre_entry = Entry(addw)
    genre_entry.pack(pady=5)
    
    Label(addw, text="Availability:", bg="lightgreen").pack(pady=5)
    availability_entry =Entry(addw)
    availability_entry.pack(pady=5)
    
    Button(addw, text="Add Book", command=lambda: addvaluestodb(bookid_entry.get(),title_entry.get(),Cost_entry.get(),availability_entry.get(), author_entry.get(), genre_entry.get()), bg="white").pack(pady=20)

def addvaluestodb(bookid, title,cost,availability,author,genre):
   st = "INSERT IGNORE INTO books (book_id,book_name,cost,avaiable,author,genre) VALUES (%s, %s, %s, %s, %s, %s)"
   mycur.execute(st, (bookid, title, cost, availability, author, genre))
    
   mycon.commit()
   messagebox.showinfo("Success","  Book is added successfully  ")

#function to open the remove window
def remove_window():
    removew = Toplevel(root)
    removew.title("Remove Book")
    removew.geometry("400x200")
    removew.configure(bg="lightcoral")
    
    Label(removew, text="Enter Book ID to Remove:", bg="lightcoral").pack(pady=20)
    book_id_entry = Entry(removew)
    book_id_entry.pack(pady=10)
    
    Button(removew, text="Remove", command=lambda: removebookfromdb(book_id_entry.get()), bg="white").pack(pady=20)

def removebookfromdb(book_id):
    c=messagebox.askquestion("Remove","Are you Sure?")
    if c=="yes":
        remove="delete from books where book_id=%s"
        mycur.execute(remove,(book_id,))
        mycon.commit()
        messagebox.showinfo("Success!!","  Book is removed  ")
    


def modify_window():
    modify_window =Toplevel(root)
    modify_window.title("Modify Book")
    modify_window.geometry("600x500")
    modify_window.configure(bg="lightyellow")

    #ui desgin
    Label(modify_window,text="BookID",bg="lightyellow").pack(pady=5)
    bookid_entry=Entry(modify_window)
    bookid_entry.pack(pady=5)
    
    Label(modify_window,text="Title",bg="lightyellow").pack(pady=5)
    Title_entry=Entry(modify_window)
    Title_entry.pack(pady=5)
    
    Label(modify_window,text="Cost",bg="lightyellow").pack(pady=5)
    cost_entry=Entry(modify_window)
    cost_entry.pack(pady=5)

    Label(modify_window,text="Available",bg="lightyellow").pack(pady=5)
    avaliable_entry=Entry(modify_window)
    avaliable_entry.pack(pady=5)

    Label(modify_window,text="Author",bg="lightyellow").pack(pady=5)
    author_entry=Entry(modify_window)
    author_entry.pack(pady=5)

    Label(modify_window,text="Genre",bg="lightyellow").pack(pady=5)
    genare_entry=Entry(modify_window)
    genare_entry.pack(pady=5)
     
   

    modifybutton=Button(modify_window,text="Modify",relief="raised",anchor=CENTER,command=lambda:modifydb(bookid_entry.get(),Title_entry.get(),cost_entry.get(),avaliable_entry.get(),author_entry.get(),genare_entry.get()))
    modifybutton.pack(pady=5)
    
    
def modifydb(book_id,title,cost,available,author,genre):
 
    try:
        s1="update books set book_name=%s,cost=%s,avaiable=%s,author=%s,genre=%s where book_id=%s"
        mycur.execute(s1,(title,cost,available,author,genre,book_id))
        mycon.commit()
        messagebox.showinfo("SUCCESS","Modified successfully")
    except Exception as e:
        mycon.rollback()
        messagebox.showerror("ERROR","Please Make Sure to Enter All data")
#main 
root = Tk()
root.title("Library Management System")
root.geometry("800x600")

#background work
background_image =PhotoImage(file="library_background_1920x1024.png")
background_label =Label(root, image=background_image)
background_label.place(relwidth=1, relheight=1)

#title
title_label = Label(root, text="Library Management System", font=("Arial", 24, "bold"), bg="#4CAF50", fg="white")
title_label.pack(pady=20)

#buttons for admin
button_frame = Frame(root,bg="brown")
button_frame.pack(pady=100)

#btn_style = {"font": ("Arial", 16), "width": 20, "bg": "#4CAF50", "fg": "white"}
Button(button_frame, text="View", command=view_window, font=("Arial",16),fg="white",bg="black",relief="groove",width=20).pack(pady=10)
Button(button_frame, text="Search Books", command=search_window, font=("Arial",16),fg="white",bg="black",relief="groove",width=20).pack(pady=10)
Button(button_frame, text=" Add Book ", command=add_window,font=("Arial",16),fg="white",bg="black",relief="groove",width=20).pack(pady=10)
Button(button_frame, text="Remove Book", command=remove_window, font=("Arial",16),fg="white",bg="black",relief="groove",width=20).pack(pady=10)
Button(button_frame, text="Modify Book", command=modify_window, font=("Arial",16),fg="white",bg="black",relief="groove",width=20).pack(pady=10)

root.mainloop()
