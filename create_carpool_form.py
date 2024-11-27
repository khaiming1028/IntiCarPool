# create_carpool_form.py

import tkinter as tk
from tkcalendar import DateEntry

def create_carpool_form(parent_frame, create_carpool_callback, search_location_callback):
    # Add a header tab to the create carpool frame
    carpool_header_label = tk.Label(parent_frame, text="Create Carpool", font=("Arial", 12, "bold"), bg="#666666", fg="#ffffff", pady=10)
    carpool_header_label.grid(row=0, column=0, columnspan=3, padx=0, pady=(0,10), sticky="ew")

    # Carpool Name Label and Entry
    carpool_name_label = tk.Label(parent_frame, text="Carpool Name:", font=("Arial", 12), bg="#ffffff")
    carpool_name_label.grid(row=1, column=0, padx=20, pady=5, sticky="e")
    carpool_name_entry = tk.Entry(parent_frame, font=("Arial", 12), width=30)
    carpool_name_entry.grid(row=1, column=1, padx=20, pady=5)

    # Carpool Time Label and Entry
    carpool_pickup_date_label = tk.Label(parent_frame, text="Pickup Date:", font=("Arial", 12), bg="#ffffff")
    carpool_pickup_date_label.grid(row=2, column=0, padx=20, pady=5, sticky="e")
    carpool_pickup_date_entry = DateEntry(parent_frame, font=("Arial", 12), width=27, showweeknumbers=False)
    carpool_pickup_date_entry.grid(row=2, column=1, padx=20, pady=5)

    # Carpool Pickup Time Label and Entry
    carpool_pickup_time_label = tk.Label(parent_frame, text="Pickup Time:", font=("Arial", 12), bg="#ffffff")
    carpool_pickup_time_label.grid(row=3, column=0, padx=20, pady=5, sticky="e")

    # Create a frame for the pickup time entries
    pickup_time_frame = tk.Frame(parent_frame, bg="#ffffff")
    pickup_time_frame.grid(row=3, column=1, padx=20, pady=5, sticky="w")

    carpool_pickup_hour_entry = tk.Spinbox(pickup_time_frame, from_=0, to=23, format="%02.0f", font=("Arial", 12), width=5)
    carpool_pickup_hour_entry.pack(side="left", padx=(5, 10))
    carpool_pickup_minute_entry = tk.Spinbox(pickup_time_frame, from_=0, to=59, format="%02.0f", font=("Arial", 12), width=5)
    carpool_pickup_minute_entry.pack(side="left")

    # Carpool Dropoff Time Label and Entry
    carpool_dropoff_time_label = tk.Label(parent_frame, text="Dropoff Time:", font=("Arial", 12), bg="#ffffff")
    carpool_dropoff_time_label.grid(row=4, column=0, padx=20, pady=5, sticky="e")

    # Create a frame for the dropoff time entries
    dropoff_time_frame = tk.Frame(parent_frame, bg="#ffffff")
    dropoff_time_frame.grid(row=4, column=1, padx=20, pady=5, sticky="w")

    carpool_dropoff_hour_entry = tk.Spinbox(dropoff_time_frame, from_=0, to=23, format="%02.0f", font=("Arial", 12), width=5)
    carpool_dropoff_hour_entry.pack(side="left", padx=(5, 10))
    carpool_dropoff_minute_entry = tk.Spinbox(dropoff_time_frame, from_=0, to=59, format="%02.0f", font=("Arial", 12), width=5)
    carpool_dropoff_minute_entry.pack(side="left")

    # Carpool Available Seats Label and Entry
    carpool_available_seat_label = tk.Label(parent_frame, text="Available Seats:", font=("Arial", 12), bg="#ffffff")
    carpool_available_seat_label.grid(row=5, column=0, padx=20, pady=5, sticky="e")
    carpool_available_seat_entry = tk.Entry(parent_frame, font=("Arial", 12), width=30)
    carpool_available_seat_entry.grid(row=5, column=1, padx=20, pady=5)

    # Carpool Pickup Point Label and Entry
    carpool_pickup_point_label = tk.Label(parent_frame, text="Pickup Point:", font=("Arial", 12), bg="#ffffff")
    carpool_pickup_point_label.grid(row=6, column=0, padx=20, pady=5, sticky="e")
    carpool_pickup_point_entry = tk.Entry(parent_frame, font=("Arial", 12), width=30)
    carpool_pickup_point_entry.grid(row=6, column=1, padx=20, pady=5, sticky="w")

    # Search Location Button
    search_location = tk.Button(parent_frame, text="Search Location", command=search_location_callback, font=("Arial", 12), bg="blue", fg="white")
    search_location.grid(row=6, column=2, padx=(10,20), pady=5)

    # Submit Button
    submit_button = tk.Button(parent_frame, text="Create Carpool", command=create_carpool_callback, font=("Arial", 12), bg="#E21A22", fg="white")
    submit_button.grid(row=8, column=0, columnspan=3, padx=20, pady=20, sticky="ew")

    return {
        "carpool_name_entry": carpool_name_entry,
        "carpool_pickup_date_entry": carpool_pickup_date_entry,
        "carpool_pickup_hour_entry": carpool_pickup_hour_entry,
        "carpool_pickup_minute_entry": carpool_pickup_minute_entry,
        "carpool_dropoff_hour_entry": carpool_dropoff_hour_entry,
        "carpool_dropoff_minute_entry": carpool_dropoff_minute_entry,
        "carpool_available_seat_entry": carpool_available_seat_entry,
        "carpool_pickup_point_entry": carpool_pickup_point_entry
    }