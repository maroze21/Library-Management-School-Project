from tkinter import *
from tkinter import ttk
import mysql.connector as sql


mycon=sql.connect(host='localhost',username='root',password='root',database='library_management')
mycur=mycon.cursor()
#functions to search ,add ,delete,modify

def search_window():
    search =Toplevel(root)
    search.title("Search Books")
    search.geometry("800x400")
    search.configure(bg="lightblue")
    
    columns = ("ID", "Title" ,"Cost","Author", "Genre", "Availability")
    tree = ttk.Treeview(search, columns=columns, show='headings')
    
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, anchor='center', width=100)
    
    #just for testing as database yet to be connected
    """bookdata = [
        (1, "Python Programming", "John Doe", "Programming", "Available"),
        (2, "Data Structures", "Jane Smith", "Education", "Issued"),
    ]"""
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

    Label(addw, text="Cost", bg="lightgreen").pack(pady=5)
    Cost_entry = Entry(addw)
    Cost_entry.pack(pady=5)
    
    Label(addw, text="Title:", bg="lightgreen").pack(pady=5)
    title_entry = Entry(addw)
    title_entry.pack(pady=5)
    
    Label(addw, text="Author:", bg="lightgreen").pack(pady=5)
    author_entry = Entry(addw)
    author_entry.pack(pady=5)
    
    Label(addw, text="Genre:", bg="lightgreen").pack(pady=5)
    genre_entry = Entry(addw)
    genre_entry.pack(pady=5)
    
    Label(addw, text="Availability:", bg="lightgreen").pack(pady=5)
    availability_entry =Entry(addw)
    availability_entry.pack(pady=5)
    
    Button(addw, text="Add Book", command=lambda: addvaluestodb(bookid_entry.get(),title_entry.get(),Cost_entry.get(), author_entry.get(), genre_entry.get(), availability_entry.get()), bg="white").pack(pady=20)

def addvaluestodb(bookid, title,cost, author, genre, availability):
    st="insert ignore into(book_id,book_name,cost,author,genre,available) books values (%s,'%s',%s,'%s','%s',%s)"
    mycur.execute(st,(bookid,cost,title,author,genre,availability))
    mycon.commit()

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
    print(f"Removing book with ID: {book_id}")

def modify_window():
    modify_window =Toplevel(root)
    modify_window.title("Modify Book")
    modify_window.geometry("400x300")
    modify_window.configure(bg="lightyellow")

#main 
root = Tk()
root.title("Library Management System")
root.geometry("800x600")

#background work
background_image =PhotoImage(file="C:\Users\USER\Desktop\Library-Management-School-Project\CS Project\library_background_1920x1024.png")
background_label =Label(root, image=background_image)
background_label.place(relwidth=1, relheight=1)

#title
title_label = Label(root, text="Library Management System", font=("Arial", 24, "bold"), bg="#4CAF50", fg="white")
title_label.pack(pady=20)

#buttons for admin
button_frame = Frame(root,bg="brown")
button_frame.pack(pady=100)

#btn_style = {"font": ("Arial", 16), "width": 20, "bg": "#4CAF50", "fg": "white"}
Button(button_frame, text="Search Books", command=search_window, font=("Arial",16),fg="white",bg="black",relief="groove",width=20).pack(pady=10)
Button(button_frame, text=" Add Book ", command=add_window,font=("Arial",16),fg="white",bg="black",relief="groove",width=20).pack(pady=10)
Button(button_frame, text="Remove Book", command=remove_window, font=("Arial",16),fg="white",bg="black",relief="groove",width=20).pack(pady=10)
Button(button_frame, text="Modify Book", command=modify_window, font=("Arial",16),fg="white",bg="black",relief="groove",width=20).pack(pady=10)

root.mainloop()
