import tkinter as tk
from tkinter import ttk

def open_joined_carpool_window():
    # Create the joined carpool window
    joined_carpool_window = tk.Toplevel()
    joined_carpool_window.title("Joined Carpool Information")
    joined_carpool_window.geometry("600x400")
    joined_carpool_window.configure(bg="#f0f0f0")

    style = ttk.Style()
    style.theme_use("clam")
    style.configure("TLabel", background="#f0f0f0", font=("Helvetica", 12))
    style.configure("TButton", font=("Helvetica", 12), padding=6)

    # Title Label
    title_label = ttk.Label(joined_carpool_window, text="Your Joined Carpools", font=("Helvetica", 16, "bold"))
    title_label.pack(pady=10)

    # List of joined carpools (Placeholder list for demonstration)
    joined_carpools = ["Carpool A - Sedan - 2:00 PM", "Carpool B - MPV - 3:30 PM", "Carpool C - SUV - 5:00 PM"]

    # Display the joined carpools
    for carpool in joined_carpools:
        carpool_label = ttk.Label(joined_carpool_window, text=carpool)
        carpool_label.pack(pady=5)

    # Close Button
    close_button = ttk.Button(joined_carpool_window, text="Close", command=joined_carpool_window.destroy)
    close_button.pack(pady=20)
