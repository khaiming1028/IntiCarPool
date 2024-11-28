# manage_carpool_form.py

import tkinter as tk
from tkinter import messagebox
import mysql.connector
from datetime import datetime
from create_carpool_form import create_carpool_form
import textwrap
from tkintermapview import TkinterMapView
from geopy.geocoders import Nominatim
import requests

GOOGLE_API_KEY = "AIzaSyC4GMTOjpDLoMQsQKBc1y64bPTwJFsPgBg"

def manage_carpool_form(parent_frame, user_id):
    # Define headers
    headers = ["Car Details", "Available Seats", "Pickup Date & Time", "Dropoff Time", "Pickup Point", "Status", "Action", "", ""]
    for col, header in enumerate(headers):
        header_label = tk.Label(parent_frame, text=header, font=("Arial", 12, "bold"), bg="#666666", fg="#ffffff", padx=10, pady=10)
        header_label.grid(row=0, column=col, pady=(0,10), sticky="ew")

    try:
        # Connect to the MySQL database
        db_connection = mysql.connector.connect(
            host="localhost",  # Your XAMPP MySQL host
            user="root",  # Your MySQL username
            password="",  # Your MySQL password (default is empty for XAMPP)
            database="carpool_system"  # Your database name
        )
        cursor = db_connection.cursor()

        # Query the database to get carpool details created by the user
        query = """
            SELECT c.id, u.car_plate, u.car_type, u.car_name, c.available_seat, c.pickup_datetime, c.dropoff_time, c.pickup_point, c.status
            FROM carpool c
            JOIN user u ON c.driver_id = u.id
            WHERE c.driver_id = %s
        """
        cursor.execute(query, (user_id,))
        results = cursor.fetchall()

        # Display the carpool details in a table view
        for row_num, row in enumerate(results, start=1):
            car_details = f"{row[1]}\n{row[2]}\n{row[3]}"  # Combine car plate, car type, and car name
            car_details_label = tk.Label(parent_frame, text=car_details, font=("Arial", 12), bg="#ffffff", justify="left")
            car_details_label.grid(row=row_num, column=0, padx=5, pady=5, sticky="ew")

            for col_num, value in enumerate(row[4:], start=1):  # Skip the first four columns (car details)
                if col_num == 5:  # If the column is the pickup point
                    value = textwrap.fill(value, width=20)  # Wrap the text to a width of 20 characters
                cell_label = tk.Label(parent_frame, text=value, font=("Arial", 12), bg="#ffffff", justify="left", wraplength=200)
                cell_label.grid(row=row_num, column=col_num, padx=5, pady=5, sticky="ew")

            # Add action buttons
            edit_button = tk.Button(parent_frame, text="Edit", font=("Arial", 12), command=lambda r=row: open_edit_popup(r[0]))
            edit_button.grid(row=row_num, column=6, padx=5, pady=5, sticky="ew")

            view_passenger_button = tk.Button(parent_frame, text="View Passenger", font=("Arial", 12), bg="blue", fg="white", command=lambda r=row: view_passenger(r))
            view_passenger_button.grid(row=row_num, column=7, padx=5, pady=5, sticky="ew")

            delete_button = tk.Button(parent_frame, text="Delete", font=("Arial", 12), bg="#E21A22", fg="white", command=lambda r=row: delete_carpool(r))
            delete_button.grid(row=row_num, column=8, padx=(5,10), pady=5, sticky="ew")

        # Close the database connection
        cursor.close()
        db_connection.close()

    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")

def open_edit_popup(carpool_id):
    # Create a popup window
    edit_popup = tk.Toplevel()
    edit_popup.title("Edit Carpool")
    edit_popup.geometry("400x400")

    # Create a frame for the form
    edit_frame = tk.Frame(edit_popup, bg="#ffffff")
    edit_frame.pack(expand=True, fill='both')

    # Connect to the MySQL database to fetch carpool details
    try:
        db_connection = mysql.connector.connect(
            host="localhost",  # Your XAMPP MySQL host
            user="root",  # Your MySQL username
            password="",  # Your MySQL password (default is empty for XAMPP)
            database="carpool_system"  # Your database name
        )
        cursor = db_connection.cursor()

        # Query to fetch carpool details
        query = """
            SELECT carpool_name, available_seat, pickup_point, pickup_datetime, dropoff_time
            FROM carpool
            WHERE id = %s
        """
        cursor.execute(query, (carpool_id,))
        carpool = cursor.fetchone()

        # Close the database connection
        cursor.close()
        db_connection.close()

    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error fetching data: {err}")
        return

    # Populate the form with existing carpool details
    carpool_form_entries = create_carpool_form(edit_frame, lambda: update_carpool(carpool_id, carpool_form_entries, edit_popup), lambda: search_from_google_map(edit_frame, carpool_form_entries))

    carpool_form_entries["carpool_name_entry"].insert(0, carpool[0])
    carpool_form_entries["carpool_available_seat_entry"].insert(0, carpool[1])
    carpool_form_entries["carpool_pickup_point_entry"].insert(0, carpool[2])
    pickup_date, pickup_time = carpool[3].split()
    carpool_form_entries["carpool_pickup_date_entry"].set_date(pickup_date)
    pickup_hour, pickup_minute = pickup_time.split(":")
    carpool_form_entries["carpool_pickup_hour_entry"].delete(0, tk.END)
    carpool_form_entries["carpool_pickup_hour_entry"].insert(0, pickup_hour)
    carpool_form_entries["carpool_pickup_minute_entry"].delete(0, tk.END)
    carpool_form_entries["carpool_pickup_minute_entry"].insert(0, pickup_minute)
    dropoff_hour, dropoff_minute = carpool[4].split(":")
    carpool_form_entries["carpool_dropoff_hour_entry"].delete(0, tk.END)
    carpool_form_entries["carpool_dropoff_hour_entry"].insert(0, dropoff_hour)
    carpool_form_entries["carpool_dropoff_minute_entry"].delete(0, tk.END)
    carpool_form_entries["carpool_dropoff_minute_entry"].insert(0, dropoff_minute)

def search_from_google_map(parent_frame, carpool_form_entries):
    google_map_page = tk.Toplevel(parent_frame)
    google_map_page.title("Google Map")
    google_map_page.geometry("800x800")

    geolocator = Nominatim(user_agent="google_map_search")
    
    # Map widget
    map_widget = TkinterMapView(google_map_page, width=600, height=400, corner_radius=0)
    map_widget.pack(fill="both", expand=True)

    # Use Google Maps tile server
    map_widget.set_tile_server("https://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=22)

    # Variable to store the marker
    global current_marker
    current_marker = None

    # Function to search for a location
    def search_place():
        place = search_entry.get()
        if place:
            geocode_url = f"https://maps.googleapis.com/maps/api/geocode/json?address={place}&key={GOOGLE_API_KEY}"
            response = requests.get(geocode_url)
            data = response.json()

            if data["status"] == "OK":
                # Extract latitude and longitude
                location = data["results"][0]["geometry"]["location"]
                lat, lng = location["lat"], location["lng"]

                # Update map position and add a marker
                map_widget.set_position(lat, lng, zoom=15)
                global current_marker
                if current_marker:  # Remove existing marker
                    current_marker.delete()
                current_marker = map_widget.set_marker(lat, lng)
            else:
                print("Error from Geocoding API:", data.get("error_message", "Unknown error"))

    # Function to set the pickup location
    def set_pickup_location():
        if current_marker:
            # Get the position (latitude, longitude)
            lat, lng = current_marker.position
            
            # Convert coordinates to address
            location = geolocator.reverse((lat, lng), language='en')
            
            if location:
                # Display the address in the entry widget
                carpool_form_entries["carpool_pickup_point_entry"].delete(0, tk.END)
                carpool_form_entries["carpool_pickup_point_entry"].insert(0, location.address)
            else:
                print("Address not found!")
            
            google_map_page.destroy()
        else:
            print("No location selected!")

    # Search bar and button
    search_entry = tk.Entry(google_map_page, width=40)
    search_entry.pack(pady=10)
    
    search_button = tk.Button(google_map_page, text="Search", command=search_place)
    search_button.pack(pady=5)
    # Confirm button
    confirm_button = tk.Button(google_map_page, text="Set as Pickup Point", command=set_pickup_location)
    confirm_button.pack(pady=10)

def update_carpool(carpool_id, carpool_form_entries, edit_popup):
    # Get user input
    carpool_name = carpool_form_entries["carpool_name_entry"].get()
    available_seat = carpool_form_entries["carpool_available_seat_entry"].get()
    pickup_point = carpool_form_entries["carpool_pickup_point_entry"].get()
    pickup_date = carpool_form_entries["carpool_pickup_date_entry"].get()
    pickup_hour = carpool_form_entries["carpool_pickup_hour_entry"].get()
    pickup_minute = carpool_form_entries["carpool_pickup_minute_entry"].get()
    dropoff_hour = carpool_form_entries["carpool_dropoff_hour_entry"].get()
    dropoff_minute = carpool_form_entries["carpool_dropoff_minute_entry"].get()
    dropoff_time = f"{dropoff_hour}:{dropoff_minute}"
    status = "available"

    # Combine pickup date and time
    pickup_time = f"{pickup_hour}:{pickup_minute}"
    pickup_datetime = f"{pickup_date} {pickup_time}"

    # Validate input
    if not all([carpool_name, pickup_date, pickup_hour, pickup_minute, dropoff_hour, dropoff_minute, available_seat, pickup_point]):
        messagebox.showerror("Input Error", "All fields are required!")
        return

    try:
        # Combine pickup date and time
        pickup_datetime = datetime.strptime(pickup_datetime, "%m/%d/%y %H:%M").strftime("%Y-%m-%d %H:%M:%S")
        dropoff_time = datetime.strptime(dropoff_time, "%H:%M").strftime("%H:%M:%S")

        # Connect to the MySQL database
        db_connection = mysql.connector.connect(
            host="localhost",  # Your XAMPP MySQL host
            user="root",  # Your MySQL username
            password="",  # Your MySQL password (default is empty for XAMPP)
            database="carpool_system"  # Your database name
        )
        cursor = db_connection.cursor()

        # Update data in the database
        query = """
            UPDATE carpool
            SET carpool_name = %s, available_seat = %s, pickup_point = %s, pickup_datetime = %s, dropoff_time = %s, status = %s
            WHERE id = %s
        """
        values = (carpool_name, available_seat, pickup_point, pickup_datetime, dropoff_time, status, carpool_id)
        cursor.execute(query, values)
        db_connection.commit()

        messagebox.showinfo("Success", "Carpool updated successfully!")

        # Close the popup window
        edit_popup.destroy()

        # Close the database connection
        cursor.close()
        db_connection.close()

    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error updating data: {err}")

def view_passenger(carpool):
    # Function to view passengers of the selected carpool
    messagebox.showinfo("View Passenger", f"View passengers for carpool: {carpool}")

def delete_carpool(carpool):
    # Function to delete the selected carpool
    messagebox.showinfo("Delete Carpool", f"Delete carpool: {carpool}")