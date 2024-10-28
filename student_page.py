import tkinter as tk
from tkinter import messagebox
import carpool_form  # Import the renamed module
import carpool_list

def open_student_page():
    # Create the carpool window
    carpool_app = tk.Tk()
    carpool_app.title("Carpool Options")
    carpool_app.attributes("-fullscreen", True)  # Set to full-screen

    # Add escape key event to exit full-screen mode
    carpool_app.bind("<Escape>", lambda e: carpool_app.attributes("-fullscreen", False))

    # Define button functions for carpool options
    def create_carpool():
        carpool_form.open_carpool_window()  # Correctly call the function from carpool_form.py

    def find_carpool():
        print("Find Carpool button clicked")

    def joined_carpool():
        carpool_list.open_joined_carpool_window()
        

    # Define functions for navigation bar
    def about_app():
        messagebox.showinfo("About", "Carpool App v1.0\nCreated to connect carpoolers easily.")

    def contact_us():
        messagebox.showinfo("Contact", "Email us if any bugs and report(Email: support@carpoolapp.com)")

    # Create a navigation bar
    nav_bar = tk.Frame(carpool_app, bg="#333333", height=40)
    nav_bar.pack(fill=tk.X)

    nav_button_style = {
        "font": ("Helvetica", 10, "bold"),
        "bg": "#333333",
        "fg": "#ffffff",
        "activebackground": "#555555",
        "activeforeground": "#ffffff",
        "borderwidth": 0,
        "padx": 15,
        "pady": 10,
    }

    # Navigation bar buttons
    tk.Button(nav_bar, text="Create carpool", **nav_button_style, command=create_carpool).pack(side=tk.LEFT)
    tk.Button(nav_bar, text="Find Carpool", **nav_button_style, command=find_carpool).pack(side=tk.LEFT)
    tk.Button(nav_bar, text="Joined Carpool", **nav_button_style, command=joined_carpool).pack(side=tk.LEFT)
    tk.Button(nav_bar, text="About", **nav_button_style, command=about_app).pack(side=tk.LEFT)
    tk.Button(nav_bar, text="Contact Us", **nav_button_style, command=contact_us).pack(side=tk.LEFT)

    # Styling options for main window buttons
    button_style = {
        "font": ("Helvetica", 12, "bold"),
        "bg": "#4CAF50",
        "fg": "#ffffff",
        "activebackground": "#45a049",
        "activeforeground": "#ffffff",
        "width": 20,
        "height": 2,
        "bd": 2
    }

    # Main carpool buttons
    tk.Button(carpool_app, text="Create Carpool", command=create_carpool, **button_style).pack(pady=10)
    tk.Button(carpool_app, text="Find Carpool", command=find_carpool, **button_style).pack(pady=10)
    tk.Button(carpool_app, text="Joined Carpool", command=joined_carpool, **button_style).pack(pady=10)

    # Run the carpool window
    carpool_app.mainloop()

