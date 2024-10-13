from tkinter import *
from tkinter import ttk
import tkinter.messagebox as messagebox
import subprocess as sp
import mysql.connector as mc
from datetime import datetime, timedelta

# Connect to MySQL (using localhost and default credentials)
db_connection = mc.connect(host='localhost', user='root', password='root', charset='utf8')
db_cursor = db_connection.cursor()

# Use the 'library_management' database
db_cursor.execute("USE library_management")

# Create tables for books and book requests if they don't exist
db_cursor.execute("""
    CREATE TABLE IF NOT EXISTS barter_books (
        Username VARCHAR(30) PRIMARY KEY, 
        book_id INT, 
        book_name VARCHAR(40), 
        req_date DATE, 
        return_date DATE
    )
""")
db_cursor.execute("""
    CREATE TABLE IF NOT EXISTS books (
        book_id INT PRIMARY KEY, 
        book_name VARCHAR(40), 
        cost INT, 
        available TINYINT(1), 
        author CHAR(40), 
        genre CHAR(20)
    )
""")

# Function to open the login page
def open_login_page():
    root.destroy()  # Close the current window
    sp.run(["python", "loginpage.py"])  # Open login page (assuming it’s a separate Python script)

# Helper function to get a book by its ID
def get_book_by_id(book_id):
    db_cursor.execute("SELECT * FROM books WHERE book_id = %s", (book_id,))
    return db_cursor.fetchone()

# Search books window
def open_search_books_window():
    search_window = Toplevel(root)  # Create a new window
    search_window.title("Search Books")
    search_window.geometry("800x400")
    search_window.configure(bg="lightblue")

    # Label and entry for searching
    Label(search_window, text="Search Books").pack(pady=5)
    search_entry = Entry(search_window)
    search_entry.pack(pady=5)

    # Function to search books
    def search_books():
        search_term = search_entry.get().lower()  # Get search term from input
        db_cursor.execute("SELECT * FROM books WHERE LOWER(book_name) = %s", (search_term,))
        search_result = db_cursor.fetchone()

        # Clear previous search results
        for item in books_tree.get_children():
            books_tree.delete(item)

        # If the book is found, display it
        if search_result:
            books_tree.insert('', "end", values=search_result)
        else:
            messagebox.showerror("ERROR", "No book found")  # Show error if no book is found

    # Define the columns for Treeview (table-like widget)
    columns = ("ID", "Title", "Cost", "Available", "Author", "Genre")
    books_tree = ttk.Treeview(search_window, columns=columns, show='headings')

    # Set column headers and properties
    for col in columns:
        books_tree.heading(col, text=col)
        books_tree.column(col, anchor=CENTER, width=100)

    books_tree.pack(fill=BOTH, expand=True)

    # Search button
    Button(search_window, text="Search", anchor="center", relief="groove", command=search_books).pack(pady=5)

# Request a book window
def open_request_book_window():
    request_window = Tk()  # Create a new window for requesting a book
    request_window.title("Request Book")
    request_window.geometry("600x350")

    Label(request_window, text="REQUEST BOOK", bg="lightblue", font=("Arial", 17)).grid(row=0, column=1, columnspan=2, pady=10, padx=150)
    
    Label(request_window, text="Book ID", bg="lightblue", font=("Arial", 15)).grid(row=1, column=0, columnspan=2, pady=10)
    book_id_entry = Entry(request_window)
    book_id_entry.grid(row=1, column=2, padx=5, pady=5, sticky="W")

    # Function to search and display book details
    def search_and_request_book():
        book_id = book_id_entry.get()  # Get book ID from entry
        book_data = get_book_by_id(book_id)

        if not book_data:
            messagebox.showerror("ERROR", "Book ID not found")  # Error if book isn't found
            return

        # Show the book name
        Label(request_window, text="Book Name", bg="lightblue", font=("Arial", 15)).grid(row=3, column=0, columnspan=2, pady=10)
        book_name_entry = Entry(request_window)
        book_name_entry.grid(row=3, column=2, padx=5, pady=5, sticky="W")
        book_name_entry.insert(END, book_data[1])  # Insert the book name into the field

        request_date = datetime.now()  # Request date is today
        return_date = request_date + timedelta(days=14)  # Return date in 14 days

        # Function to confirm the request
        def confirm_book_request():
            username = "SomeUsername"  # Replace with actual username of the user
            db_cursor.execute("""
                INSERT INTO barter_books (Username, book_id, book_name, req_date, return_date)
                VALUES (%s, %s, %s, %s, %s)
            """, (username, book_id, book_data[1], request_date, return_date))
            db_connection.commit()
            messagebox.showinfo("Success", "Book Requested!")

        # Button to confirm the book request
        Button(request_window, text="Confirm Book Request", command=confirm_book_request, font=("Arial", 12), bg="lightblue").grid(row=5, column=2)

    # Search button to fetch the book details
    Button(request_window, text="Search", font=("Arial", 12), bg="lightblue", relief="raised", command=search_and_request_book).grid(row=2, column=2)

# Main window setup
root = Tk()
root.title("Library Management - Member Page")
root.geometry("800x600")
root.resizable(False, False)

# Background image setup (replace with actual image)
background_image = PhotoImage(file="memberpg_bg.png")
background_label = Label(root, image=background_image)
background_label.place(relwidth=1, relheight=1)

# Frame for the buttons
button_frame = Frame(root)
button_frame.pack(pady=200)

# Buttons for searching, requesting, and returning books
Button(button_frame, text="Search Books", command=open_search_books_window, font=("Arial", 16), fg="black", bg="#2072AA", relief="groove", width=20).pack(pady=10)
Button(button_frame, text="Request Book", command=open_request_book_window, font=("Arial", 16), fg="black", bg="#2072AA", relief="groove", width=20).pack(pady=10)
Button(button_frame, text="Return Book", font=("Arial", 16), fg="black", bg="#2072AA", relief="groove", width=20).pack(pady=10)  # Return functionality yet to be implemented

# Run the main loop
root.mainloop()
