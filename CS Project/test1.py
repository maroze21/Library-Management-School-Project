from tkinter import *
from tkinter import ttk

# Sample data (you can replace this with dynamic data later)
books = [
    {"BookID": 1, "Title": "The Great Gatsby", "Author": "F. Scott Fitzgerald"},
    {"BookID": 2, "Title": "To Kill a Mockingbird", "Author": "Harper Lee"},
    {"BookID": 3, "Title": "1984", "Author": "George Orwell"},
    {"BookID": 4, "Title": "Pride and Prejudice", "Author": "Jane Austen"},
    {"BookID": 5, "Title": "The Catcher in the Rye", "Author": "J.D. Salinger"},
]

# Function to search for books and display in a Treeview
def search_books():
    search_window = Toplevel(root)
    search_window.title("Search Books")
    search_window.geometry("600x400")

    search_label = Label(search_window, text="Search for a Book:", font=("Arial", 14))
    search_label.pack(pady=10)

    search_entry = Entry(search_window, font=("Arial", 14), width=30)
    search_entry.pack(pady=10)

    def perform_search():
        search_term = search_entry.get().lower()
        filtered_books = [book for book in books if search_term in book["Title"].lower() or search_term in book["Author"].lower()]

        # Clear previous results in the treeview
        for item in tree.get_children():
            tree.delete(item)

        # Insert new search results into the treeview
        for book in filtered_books:
            tree.insert('', 'end', values=(book["BookID"], book["Title"], book["Author"]))

    search_button = Button(search_window, text="Search", font=("Arial", 12), command=perform_search)
    search_button.pack(pady=10)

    # Treeview to display search results
    tree = ttk.Treeview(search_window, columns=("BookID", "Title", "Author"), show="headings")
    tree.heading("BookID", text="Book ID")
    tree.heading("Title", text="Title")
    tree.heading("Author", text="Author")
    tree.pack(fill=BOTH, expand=True)

# Main application window
root = Tk()
root.title("Library Management System")
root.geometry("800x600")

search_button = Button(root, text="Search Books", font=("Arial", 14), command=search_books)
search_button.pack(pady=20)

root.mainloop()
