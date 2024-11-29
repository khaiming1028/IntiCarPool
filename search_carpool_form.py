#search_carpool_form.py

import tkinter as tk
from tkcalendar import DateEntry
import mysql.connector
from tkinter import messagebox

def search_carpool_form(parent_frame, user_id):
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
    
    def search_carpool():
        # Retrieve the user input
        pickup_date = search_carpool_pickup_date_entry.get_date()
        pickup_hour = search_carpool_pickup_hour_entry.get()
        pickup_minute = search_carpool_pickup_minute_entry.get()
        pickup_point = search_carpool_pickup_point_entry.get()

        # Convert time to a single string for easier comparison
        pickup_time = f"{pickup_hour}:{pickup_minute}"
        pickup_datetime = f"{pickup_date} {pickup_time}"
        try:
            # Connect to the MySQL database
            db_connection = mysql.connector.connect(
                host="localhost",  # Your XAMPP MySQL host
                user="root",  # Your MySQL username
                password="",  # Your MySQL password (default is empty for XAMPP)
                database="carpool_system"  # Your database name
            )
            cursor = db_connection.cursor()

            # Query the database to find matching carpool
            query = """
                SELECT * FROM carpool
                WHERE pickup_datetime = %s AND pickup_point LIKE %s
            """
            cursor.execute(query, (pickup_datetime, "%" + pickup_point + "%"))
            results = cursor.fetchall()
            
            # Close the database connection (extra)
            cursor.close()
            db_connection.close()

            # Display the results
            if results:
                show_carpool_details(results)
            else:
                messagebox.showinfo("No Results", "No carpools found matching the criteria.")
    
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")
    
    def show_carpool_details(results):
        # Create a new frame for the carpool details page
        carpool_details_frame = tk.Frame(parent_frame, bg="white", padx=10, pady=10, borderwidth=2, relief="solid")
        carpool_details_frame.grid(row=5, column=0, columnspan=3, sticky="nsew", padx=20, pady=20)
        
        # Set a header label for carpool details
        header_label = tk.Label(carpool_details_frame, text="Carpool Details", font=("Arial", 16, "bold"), bg="white")
        header_label.grid(row=0, column=0, columnspan=2, padx=10, pady=10)  # Use grid to place the header
        
        # Loop through each result and create labels to display carpool details
        for idx, row in enumerate(results):
            carpool_id = row[0]
            carpool_name = row[2]
            available_seat = row[3]
            pickup_point = row[4]
            pickup_datetime = row[5]
        

            # Create labels to display each carpool's details
            carpool_name_label = tk.Label(carpool_details_frame, text=f"Carpool Name: {carpool_name}", font=("Arial", 12), bg="#F5F5F5")
            carpool_name_label.grid(row=idx+1, column=0, sticky="w", padx=10, pady=2)

            available_seat_label = tk.Label(carpool_details_frame, text=f"Available Seats: {available_seat}", font=("Arial", 12), bg="#F5F5F5")
            available_seat_label.grid(row=idx+1, column=1, sticky="w", padx=10, pady=2)

            pickup_point_label = tk.Label(carpool_details_frame, text=f"Pickup Point: {pickup_point}", font=("Arial", 12), bg="#F5F5F5")
            pickup_point_label.grid(row=idx+2, column=0, sticky="w", padx=10, pady=2)

            pickup_datetime_label = tk.Label(carpool_details_frame, text=f"Pickup DateTime: {pickup_datetime}", font=("Arial", 12), bg="#F5F5F5")
            pickup_datetime_label.grid(row=idx+2, column=1, sticky="w", padx=10, pady=2)

            # Add a button to allow the user to join the carpool
            join_button = tk.Button(carpool_details_frame, text="Join Carpool", font=("Arial", 12), bg="#E21A22", fg="white", command=lambda c=carpool_id, u=user_id: request_carpool(c,u))
            join_button.grid(row=idx + 3, column=0, columnspan=2, pady=10, sticky="ew")
        
        
    def request_carpool(carpool_id,user_id):
        status = "Pending"
        try:
            # Connect to the MySQL database
            db_connection = mysql.connector.connect(
                host="localhost",  # Your XAMPP MySQL host
                user="root",  # Your MySQL username
                password="",  # Your MySQL password (default is empty for XAMPP)
                database="carpool_system"  # Your database name
            )
            cursor = db_connection.cursor()
            
            # Query the database to find matching carpool
            query = """
                INSERT INTO carpool_application (user_id, carpool_id, status)
                VALUES (%s, %s, %s)
            """
            values = (user_id,carpool_id, status)
            cursor.execute(query, values)
            
            # Close the database connection
            db_connection.commit()
            cursor.close()
            db_connection.close()
            messagebox.showinfo("Success", "Carpool request submitted successfully.")
            
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")
            
    # Search Button
    search_button = tk.Button(parent_frame, text="Search Carpool", command=search_carpool, font=("Arial", 12), bg="#E21A22", fg="white")
    search_button.grid(row=4, column=0, columnspan=3, padx=20, pady=20, sticky="ew")

    return {
        "search_carpool_pickup_date_entry": search_carpool_pickup_date_entry,
        "search_carpool_pickup_hour_entry": search_carpool_pickup_hour_entry,
        "search_carpool_pickup_minute_entry": search_carpool_pickup_minute_entry,
        "search_carpool_pickup_point_entry": search_carpool_pickup_point_entry
    }