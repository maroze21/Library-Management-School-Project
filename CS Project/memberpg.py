from tkinter import *
from tkinter import ttk
import tkinter.messagebox as messagebox
import mysql.connector as mc
from datetime import datetime

# Database connection
con = mc.connect(host='localhost', user='root', password='root', charset='utf8')
cur = con.cursor()
cur.execute("create database if not exists library_management")
# Use the library_management database
cur.execute("USE library_management")

# Create necessary tables if not present
cur.execute("""
    CREATE TABLE IF NOT EXISTS barter_books(
        Username VARCHAR(30), 
        book_id INT, 
        book_name VARCHAR(40), 
        req_date DATE, 
        return_date DATE,
        PRIMARY KEY (Username, book_id)
    )
""")
cur.execute("""
    CREATE TABLE IF NOT EXISTS books(
        book_id INT PRIMARY KEY, 
        book_name VARCHAR(40), 
        cost INT, 
        avaiable TINYINT(1), 
        author CHAR(40), 
        genre CHAR(20)
    )
""")

# Placeholder for logged-in username (for demonstration purposes)
username = "SampleUser"  # Replace with actual login mechanism

# Function to view all available books
def view_window():
    view = Toplevel(root)
    view.title("View Books")
    view.geometry("800x400")
    view.configure(bg="lightblue")
    
    # Columns for the Treeview
    columns = ("ID", "Title", "Cost", "Availability", "Author", "Genre")
    tree = ttk.Treeview(view, columns=columns, show='headings')
    
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, anchor='center', width=100)
    
    # Add scrollbar for the Treeview
    scrollbar = Scrollbar(view, orient="vertical", command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    scrollbar.pack(side=RIGHT, fill=Y)
    
    # Fetch all books from the database
    ask = "SELECT * FROM books"
    cur.execute(ask)
    result = cur.fetchall()
    
    for item in result:
        tree.insert('', 'end', values=item)
    
    tree.pack(fill=BOTH, expand=True)

# Function to search for books
def search_window():
    search = Toplevel(root)
    search.title("Search Books")
    search.geometry("800x400")
    search.configure(bg="lightblue")

    Label(search, text="Search Books").pack(pady=5)
    search_entry = Entry(search)
    search_entry.pack(pady=5)

    def addBooks():
        # Search for the book in the database
        search_term = search_entry.get().lower()
        query = "SELECT * FROM books WHERE LOWER(book_name) = %s"
        cur.execute(query, (search_term,))
        result = cur.fetchone()

        # Ensure all results are processed
        con.commit()

        for item in tree.get_children():
            tree.delete(item)

        if result:
            tree.insert('', "end", values=result)
        else:
            messagebox.showerror("ERROR", "No book found")

    columns = ("ID", "Title", "Cost", "Availability", "Author", "Genre")
    tree = ttk.Treeview(search, columns=columns, show='headings')

    # Search button
    Button(search, text="Search", anchor="center", relief="groove", command=addBooks).pack(pady=5)

    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, anchor=CENTER, width=100)

    tree.pack(fill=BOTH, expand=True)

# Function to request a book (only 1 book per user)
def request_book():
    req = Toplevel(root)
    req.title("Request Book")
    req.geometry("600x350")

    Label(req, text="REQUEST BOOK", bg="lightblue", font=("Arial", 17)).grid(row=0, column=1, columnspan=2, pady=10, padx=150)

    Label(req, text="Book Id", bg="lightblue", font=("Arial", 15)).grid(row=1, column=0, columnspan=2, pady=10)
    book_id_entry = Entry(req)
    book_id_entry.grid(row=1, column=2, padx=5, pady=5, sticky="W")

    def request_confirm():
        # Ensure book_id is an integer and valid
        try:
            book_id = int(book_id_entry.get())
        except ValueError:
            messagebox.showerror("ERROR", "Invalid Book ID. Please enter a valid number.")
            return

        # Check if the user already has a book borrowed (where return_date is still NULL)
        cur.execute("SELECT * FROM barter_books WHERE Username = %s AND return_date IS NULL", (username,))
        existing_borrow = cur.fetchone()

        # Ensure all results are processed
        con.commit()

        if existing_borrow:
            messagebox.showerror("ERROR", "You have already borrowed a book. Please return it before borrowing another.")
            return

        # Check if the book is available
        cur.execute("SELECT * FROM books WHERE book_id = %s AND avaiable = 1", (book_id,))
        book_data = cur.fetchone()

        # Ensure all results are processed
        con.commit()

        if not book_data:
            messagebox.showerror("ERROR", "Book not found or unavailable.")
            return

        # If everything is fine, proceed to borrow the book
        book_name = book_data[1]
        req_date = datetime.now().date()

        # Insert the request into barter_books if no duplicate exists
        cur.execute("""
            INSERT INTO barter_books (Username, book_id, book_name, req_date, return_date) 
            VALUES (%s, %s, %s, %s, NULL)
        """, (username, book_id, book_name, req_date))

        cur.execute("UPDATE books SET avaiable = 0 WHERE book_id = %s", (book_id,))
        con.commit()

        messagebox.showinfo("Success", "Book requested successfully")
        req.destroy()

    Button(req, text="Request Book", font=("Arial", 12), command=request_confirm).grid(row=3, column=2)

# Function to view leased books (only for the current logged-in member)
def view_leased_books():
    leased_window = Toplevel(root)
    leased_window.title("Books Leased")
    leased_window.geometry("600x350")

    Label(leased_window, text="BOOKS LEASED", bg="lightblue", font=("Arial", 17)).pack(pady=10)

    tree = ttk.Treeview(leased_window, columns=("Book ID", "Book Name", "Request Date", "Return Date"), show='headings')
    tree.heading("Book ID", text="Book ID")
    tree.heading("Book Name", text="Book Name")
    tree.heading("Request Date", text="Request Date")
    tree.heading("Return Date", text="Return Date")
    tree.pack(fill=BOTH, expand=True)

    # Fetch books leased by the current user
    cur.execute("SELECT book_id, book_name, req_date, return_date FROM barter_books WHERE Username = %s", (username,))
    rows = cur.fetchall()

    # Ensure all results are processed
    con.commit()

    for row in rows:
        tree.insert("", "end", values=row)

# Function to return a book
def return_book():
    return_win = Toplevel(root)
    return_win.title("Return Book")
    return_win.geometry("600x350")

    Label(return_win, text="RETURN BOOK", bg="lightblue", font=("Arial", 17)).grid(row=0, column=1, columnspan=2, pady=10, padx=150)

    Label(return_win, text="Book Id", bg="lightblue", font=("Arial", 15)).grid(row=1, column=0, columnspan=2, pady=10)
    book_id_entry = Entry(return_win)
    book_id_entry.grid(row=1, column=2, padx=5, pady=5, sticky="W")

    def return_confirm():
        book_id = book_id_entry.get()

        # Check if the book exists in barter_books for the logged-in member
        cur.execute("SELECT * FROM barter_books WHERE book_id = %s AND Username = %s", (book_id, username))
        lease_data = cur.fetchone()

        # Ensure all results are processed
        con.commit()

        if not lease_data:
            messagebox.showerror("ERROR", "This book was not leased by you")
            return

        # Mark the book as available in the books table
        cur.execute("UPDATE books SET avaiable = 1 WHERE book_id = %s", (book_id,))
        
        # Delete the entry from barter_books since the book is returned
        cur.execute("DELETE FROM barter_books WHERE book_id = %s AND Username = %s", (book_id, username))
        con.commit()

        messagebox.showinfo("Success", "Book returned and removed from borrow records successfully")
        return_win.destroy()

    Button(return_win, text="Return Book", font=("Arial", 12), command=return_confirm).grid(row=3, column=2)

# Main window
root = Tk()
root.title("Library Management - Member Page")
root.geometry("800x600")
root.resizable(False, False)

# Set background image (replace with the correct path to your image)
background1 = PhotoImage(file="library_background_1920x1024.png")
backgroundlabel = Label(root, image=background1)
backgroundlabel.place(relwidth=1, relheight=1)

# Buttons for library actions
button_frame = Frame(root, bg="lightblue")
button_frame.pack(pady=100)

# Added the View All Books button above the Search Books button
Button(button_frame, text="View All Books", command=view_window, font=("Arial", 16), fg="black", bg="white", relief="groove", width=20).pack(pady=10)
Button(button_frame, text="Search Books", command=search_window, font=("Arial", 16), fg="black", bg="white", relief="groove", width=20).pack(pady=10)
Button(button_frame, text="Request Book", command=request_book, font=("Arial", 16), fg="black", bg="white", relief="groove", width=20).pack(pady=10)
Button(button_frame, text="Books Leased", command=view_leased_books, font=("Arial", 16), fg="black", bg="white", relief="groove", width=20).pack(pady=10)
Button(button_frame, text="Return Book", command=return_book, font=("Arial", 16), fg="black", bg="white", relief="groove", width=20).pack(pady=10)

# Start the Tkinter event loop
root.mainloop()
