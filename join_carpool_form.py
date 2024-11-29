# join_carpool_form.py

import tkinter as tk
from tkinter import messagebox
import mysql.connector
import textwrap

def join_carpool_form(parent_frame, user_id):
    # Define headers
    headers = ["Driver Name", "Contact No.", "Car Details", "Pickup Date & Time", "Dropoff Time", "Pickup Point", "Status", "Action"]
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

        # Query the database to get carpool details where the user has applied
        query = """
            SELECT u.username, u.contact, u.car_plate, u.car_type, u.car_name, c.pickup_datetime, c.dropoff_time, c.pickup_point, ca.status, ca.id
            FROM carpool c
            JOIN user u ON c.driver_id = u.id
            JOIN carpool_application ca ON c.id = ca.carpool_id
            WHERE ca.user_id = %s
        """
        cursor.execute(query, (user_id,))
        results = cursor.fetchall()

        # Display the carpool details in a table view
        for row_num, row in enumerate(results, start=1):
            driver_name_label = tk.Label(parent_frame, text=row[0], font=("Arial", 12), bg="#ffffff", justify="left")
            driver_name_label.grid(row=row_num, column=0, padx=5, pady=5, sticky="ew")

            contact_no_label = tk.Label(parent_frame, text=row[1], font=("Arial", 12), bg="#ffffff", justify="left")
            contact_no_label.grid(row=row_num, column=1, padx=5, pady=5, sticky="ew")

            car_details = f"{row[2]}\n{row[3]}\n{row[4]}"  # Combine car plate, car type, and car name
            car_details_label = tk.Label(parent_frame, text=car_details, font=("Arial", 12), bg="#ffffff", justify="left")
            car_details_label.grid(row=row_num, column=2, padx=5, pady=5, sticky="ew")

            pickup_datetime_label = tk.Label(parent_frame, text=row[5], font=("Arial", 12), bg="#ffffff", justify="left")
            pickup_datetime_label.grid(row=row_num, column=3, padx=5, pady=5, sticky="ew")

            dropoff_time_label = tk.Label(parent_frame, text=row[6], font=("Arial", 12), bg="#ffffff", justify="left")
            dropoff_time_label.grid(row=row_num, column=4, padx=5, pady=5, sticky="ew")

            pickup_point_label = tk.Label(parent_frame, text=textwrap.fill(row[7], width=20), font=("Arial", 12), bg="#ffffff", justify="left", wraplength=200)
            pickup_point_label.grid(row=row_num, column=5, padx=5, pady=5, sticky="ew")

            status_label = tk.Label(parent_frame, text=row[8], font=("Arial", 12), bg="#ffffff", justify="left")
            status_label.grid(row=row_num, column=6, padx=5, pady=5, sticky="ew")

            # Add action button based on status
            if row[8] == "joined":
                leave_button = tk.Button(parent_frame, text="Leave", font=("Arial", 12), bg="red", fg="white", command=lambda r=row: confirm_leave_carpool(r, user_id, parent_frame))
                leave_button.grid(row=row_num, column=7, padx=15, pady=5, sticky="ew")
            else:
                action_label = tk.Label(parent_frame, text="", font=("Arial", 12), bg="#ffffff", justify="left")
                action_label.grid(row=row_num, column=7, padx=15, pady=5, sticky="ew")

        # Close the database connection
        cursor.close()
        db_connection.close()

    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")

def confirm_leave_carpool(carpool, user_id, parent_frame):
    # Function to confirm leaving the carpool
    carpool_application_id = carpool[9]
    response = messagebox.askyesno("Confirm Leave", "Are you sure you want to leave this carpool?")
    if response:
        leave_carpool(carpool_application_id, parent_frame, user_id)

def leave_carpool(carpool_application_id, parent_frame, user_id):
    # Function to handle leaving the carpool
    try:
        # Connect to the MySQL database
        db_connection = mysql.connector.connect(
            host="localhost",  # Your XAMPP MySQL host
            user="root",  # Your MySQL username
            password="",  # Your MySQL password (default is empty for XAMPP)
            database="carpool_system"  # Your database name
        )
        cursor = db_connection.cursor()

        # Delete the carpool application from the database
        delete_query = "DELETE FROM carpool_application WHERE id = %s"
        cursor.execute(delete_query, (carpool_application_id,))
        db_connection.commit()

        # Refresh the parent frame to reflect the changes
        for widget in parent_frame.winfo_children():
            widget.destroy()
        join_carpool_form(parent_frame, user_id)

        # Close the database connection
        cursor.close()
        db_connection.close()

        messagebox.showinfo("Leave Carpool", "You have successfully left the carpool.")

    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")