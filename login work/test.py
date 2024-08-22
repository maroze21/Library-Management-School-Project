import tkinter as tk

root = tk.Tk()
root.geometry("400x300")

# Create a button and place it at an absolute position
button1 = tk.Button(root, text="Button 1")
button1.place(x=50, y=50)

# Create another button and place it using relative positioning
button2 = tk.Button(root, text="Button 2")
button2.place(relx=0.5, rely=0.5, anchor="center")

# Create another button and place it with relative size and position
button3 = tk.Button(root, text="Button 3")
button3.place(relx=0.75, rely=0.75, relwidth=0.2, relheight=0.2, anchor="center")

root.mainloop()
