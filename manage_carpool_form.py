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
            edit_button = tk.Button(parent_frame, text="Edit", font=("Arial", 12), command=lambda r=row: open_edit_popup(r[0], parent_frame, user_id))
            edit_button.grid(row=row_num, column=6, padx=5, pady=5, sticky="ew")

            view_passenger_button = tk.Button(parent_frame, text="View Passenger", font=("Arial", 12), bg="blue", fg="white", command=lambda r=row: view_passenger(r[0]))
            view_passenger_button.grid(row=row_num, column=7, padx=5, pady=5, sticky="ew")

            delete_button = tk.Button(parent_frame, text="Delete", font=("Arial", 12), bg="#E21A22", fg="white", command=lambda r=row: delete_carpool(r, parent_frame, user_id))
            delete_button.grid(row=row_num, column=8, padx=(5,10), pady=5, sticky="ew")

        # Close the database connection
        cursor.close()
        db_connection.close()

    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")

def open_edit_popup(carpool_id, parent_frame, user_id):
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
    carpool_form_entries = create_carpool_form(edit_frame, lambda: update_carpool(carpool_id, carpool_form_entries, edit_popup, parent_frame, user_id), lambda: search_from_google_map(edit_frame, carpool_form_entries))

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

def update_carpool(carpool_id, carpool_form_entries, edit_popup, parent_frame, user_id):
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
    status = "Available"

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

        # Refresh the parent frame to reflect the changes
        for widget in parent_frame.winfo_children():
            widget.destroy()
        manage_carpool_form(parent_frame, user_id)

        # Close the database connection
        cursor.close()
        db_connection.close()

    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error updating data: {err}")

def view_passenger(carpool_id):
    # Function to view passengers of the selected carpool
    try:
        # Connect to the MySQL database
        db_connection = mysql.connector.connect(
            host="localhost",  # Your XAMPP MySQL host
            user="root",  # Your MySQL username
            password="",  # Your MySQL password (default is empty for XAMPP)
            database="carpool_system"  # Your database name
        )
        cursor = db_connection.cursor()

        # Query to fetch passengers who requested to join the carpool
        query = """
            SELECT u.username, u.email, u.contact, ca.status, ca.id
            FROM carpool_application ca
            JOIN user u ON ca.user_id = u.id
            WHERE ca.carpool_id = %s
        """
        cursor.execute(query, (carpool_id,))
        passengers = cursor.fetchall()

        # Close the database connection
        cursor.close()
        db_connection.close()

        if not passengers:
            messagebox.showinfo("No Passengers", "No passengers have requested to join this carpool.")
            return

        # Create a new window to display passenger details
        passenger_window = tk.Toplevel()
        passenger_window.title("Passengers")

        for passenger in passengers:
            username, email, contact, status, application_id = passenger
            passenger_frame = tk.Frame(passenger_window, bg="#ffffff", padx=10, pady=10)
            passenger_frame.pack(fill="x", pady=5)

            tk.Label(passenger_frame, text=f"Username: {username}", font=("Arial", 12), bg="#ffffff").pack(anchor="w")
            tk.Label(passenger_frame, text=f"Email: {email}", font=("Arial", 12), bg="#ffffff").pack(anchor="w")
            tk.Label(passenger_frame, text=f"Contact: {contact}", font=("Arial", 12), bg="#ffffff").pack(anchor="w")
            tk.Label(passenger_frame, text=f"Status: {status}", font=("Arial", 12), bg="#ffffff").pack(anchor="w")

            if status == "Pending":
                approve_button = tk.Button(passenger_frame, text="Approve", font=("Arial", 12), bg="green", fg="white", command=lambda aid=application_id: update_application_status(aid, "Joined", passenger_window))
                approve_button.pack(side="left", padx=5)

                decline_button = tk.Button(passenger_frame, text="Decline", font=("Arial", 12), bg="red", fg="white", command=lambda aid=application_id: update_application_status(aid, "Declined", passenger_window))
                decline_button.pack(side="left", padx=5)

    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error fetching data: {err}")

def update_application_status(application_id, status, passenger_window):
    # Function to update the status of a carpool application
    try:
        # Connect to the MySQL database
        db_connection = mysql.connector.connect(
            host="localhost",  # Your XAMPP MySQL host
            user="root",  # Your MySQL username
            password="",  # Your MySQL password (default is empty for XAMPP)
            database="carpool_system"  # Your database name
        )
        cursor = db_connection.cursor()

        # Update the status in the carpool_application table
        update_query = """
            UPDATE carpool_application
            SET status = %s
            WHERE id = %s
        """
        cursor.execute(update_query, (status, application_id))
        
         # If status is "Joined", decrement the available seats
        if status == "Joined":
            # Fetch the carpool_id associated with the application
            fetch_carpool_id_query = """
                SELECT carpool_id
                FROM carpool_application
                WHERE id = %s
            """
            cursor.execute(fetch_carpool_id_query, (application_id,))
            carpool_id = cursor.fetchone()[0]

            # Decrement the available seats in the carpool table
            decrement_seat_query = """
                UPDATE carpool
                SET available_seat = available_seat - 1
                WHERE id = %s AND available_seat > 0
            """
            cursor.execute(decrement_seat_query, (carpool_id,))
            
            # Check if the updated available_seat is now 0
            check_seat_query = """
                SELECT available_seat
                FROM carpool
                WHERE id = %s
            """
            cursor.execute(check_seat_query, (carpool_id,))
            available_seat = cursor.fetchone()[0]

            # If available_seat is 0, update status to 'Full'
            if available_seat == 0:
                update_status_query = """
                    UPDATE carpool
                    SET status = 'Full'
                    WHERE id = %s
                """
                cursor.execute(update_status_query, (carpool_id,))
        
        db_connection.commit()

        # Close the database connection
        cursor.close()
        db_connection.close()

        messagebox.showinfo("Status Updated", f"Application has been {status}.")
        passenger_window.destroy()

    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error updating data: {err}")

def delete_carpool(carpool, parent_frame, user_id):
    # Function to delete the selected carpool from the database
    carpool_id = carpool[0]
    
    # Confirm with the user before deleting
    confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this carpool?")
    if confirm:
        try:
            # Connect to the MySQL database
            db_connection = mysql.connector.connect(
                host="localhost",  # Your XAMPP MySQL host
                user="root",  # Your MySQL username
                password="",  # Your MySQL password (default is empty for XAMPP)
                database="carpool_system"  # Your database name
            )
            cursor = db_connection.cursor()
            
            query_delete_applications = "DELETE FROM carpool_application WHERE carpool_id = %s"
            cursor.execute(query_delete_applications, (carpool_id,))

            # Query to delete the carpool
            query = "DELETE FROM carpool WHERE id = %s"
            cursor.execute(query, (carpool_id,))

            # Commit the changes
            db_connection.commit()

            # Close the cursor and connection
            cursor.close()
            db_connection.close()

            # Show success message
            messagebox.showinfo("Success", "Carpool deleted successfully!")

            # Refresh the parent frame to reflect the changes
            for widget in parent_frame.winfo_children():
                widget.destroy()
            manage_carpool_form(parent_frame, user_id)
            
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error deleting data: {err}")