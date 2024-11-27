# search_carpool_form.py

import tkinter as tk
from tkcalendar import DateEntry

def search_carpool_form(parent_frame):
    # Add a header tab to the search carpool frame
    search_carpool_header_label = tk.Label(parent_frame, text="Search for Carpools", font=("Arial", 12, "bold"), bg="#666666", fg="#ffffff", pady=10)
    search_carpool_header_label.grid(row=0, column=0, columnspan=3, padx=0, pady=(0,10), sticky="ew")

    # Carpool Time Label and Entry
    search_carpool_pickup_date_label = tk.Label(parent_frame, text="Pickup Date:", font=("Arial", 12), bg="#ffffff")
    search_carpool_pickup_date_label.grid(row=1, column=0, padx=20, pady=5, sticky="e")
    search_carpool_pickup_date_entry = DateEntry(parent_frame, font=("Arial", 12), width=27, showweeknumbers=False)
    search_carpool_pickup_date_entry.grid(row=1, column=1, padx=20, pady=5)

    # Carpool Pickup Time Label and Entry
    search_carpool_pickup_time_label = tk.Label(parent_frame, text="Pickup Time:", font=("Arial", 12), bg="#ffffff")
    search_carpool_pickup_time_label.grid(row=2, column=0, padx=20, pady=5, sticky="e")
    # Create a frame for the pickup time entries
    search_pickup_time_frame = tk.Frame(parent_frame, bg="#ffffff")
    search_pickup_time_frame.grid(row=2, column=1, padx=20, pady=5, sticky="w")

    search_carpool_pickup_hour_entry = tk.Spinbox(search_pickup_time_frame, from_=0, to=23, format="%02.0f", font=("Arial", 12), width=5)
    search_carpool_pickup_hour_entry.pack(side="left", padx=(0, 10))
    search_carpool_pickup_minute_entry = tk.Spinbox(search_pickup_time_frame, from_=0, to=59, format="%02.0f", font=("Arial", 12), width=5)
    search_carpool_pickup_minute_entry.pack(side="left")

    # Carpool Pickup Point Label and Entry
    search_carpool_pickup_point_label = tk.Label(parent_frame, text="Pickup Point:", font=("Arial", 12), bg="#ffffff")
    search_carpool_pickup_point_label.grid(row=3, column=0, padx=20, pady=5, sticky="e")
    search_carpool_pickup_point_entry = tk.Entry(parent_frame, font=("Arial", 12), width=30)
    search_carpool_pickup_point_entry.grid(row=3, column=1, padx=20, pady=5, sticky="w")

    # Search Button
    search_button = tk.Button(parent_frame, text="Search Carpool", font=("Arial", 12), bg="#E21A22", fg="white")
    search_button.grid(row=4, column=0, columnspan=3, padx=20, pady=20, sticky="ew")

    return {
        "search_carpool_pickup_date_entry": search_carpool_pickup_date_entry,
        "search_carpool_pickup_hour_entry": search_carpool_pickup_hour_entry,
        "search_carpool_pickup_minute_entry": search_carpool_pickup_minute_entry,
        "search_carpool_pickup_point_entry": search_carpool_pickup_point_entry
    }