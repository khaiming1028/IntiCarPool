# profile_form.py
import tkinter as tk
from tkinter import messagebox
import mysql.connector

def create_profile_form(parent_frame, user_data=None, user_id=None):
    # Add a header tab to the profile frame
    profile_header_label = tk.Label(parent_frame, text="Profile Details", font=("Arial", 12, "bold"), bg="#666666", fg="#ffffff", pady=10)
    profile_header_label.grid(row=0, column=0, columnspan=3, padx=0, pady=(0,10), sticky="ew")

    # User Name Label and Entry
    user_name_label = tk.Label(parent_frame, text="User Name:", font=("Arial", 12), bg="#ffffff")
    user_name_label.grid(row=1, column=0, padx=20, pady=5, sticky="e")
    user_name_entry = tk.Entry(parent_frame, font=("Arial", 12), width=30, state=tk.DISABLED)
    user_name_entry.grid(row=1, column=1, padx=20, pady=5, columnspan=2)

    # Email Label and Entry
    email_label = tk.Label(parent_frame, text="Email:", font=("Arial", 12), bg="#ffffff")
    email_label.grid(row=2, column=0, padx=20, pady=5, sticky="e")
    email_entry = tk.Entry(parent_frame, font=("Arial", 12), width=30, state=tk.DISABLED)
    email_entry.grid(row=2, column=1, padx=20, pady=5, columnspan=2)

    # Phone Number Label and Entry
    phone_label = tk.Label(parent_frame, text="Phone Number:", font=("Arial", 12), bg="#ffffff")
    phone_label.grid(row=3, column=0, padx=20, pady=5, sticky="e")
    phone_entry = tk.Entry(parent_frame, font=("Arial", 12), width=30, state=tk.DISABLED)
    phone_entry.grid(row=3, column=1, padx=20, pady=5, columnspan=2)

    # Vehicle Label
    vehicle_label = tk.Label(parent_frame, text="Vehicle:", font=("Arial", 12), bg="#ffffff")
    vehicle_label.grid(row=4, column=0, padx=20, pady=5, sticky="e")

    # Car Details Frame with Border
    car_details_frame = tk.Frame(parent_frame, bd=2, relief="solid", padx=10, pady=10, bg="#ffffff")
    car_details_frame.grid(row=5, column=0, columnspan=3, padx=20, pady=10, sticky="ew")

    # Car Details Labels
    car_plate_label = tk.Label(car_details_frame, text="Car Plate:", font=("Arial", 12), bg="#ffffff")
    car_plate_label.grid(row=0, column=0, padx=20, pady=0, sticky="e")
    car_plate_value = tk.Label(car_details_frame, font=("Arial", 12), bg="#ffffff")
    car_plate_value.grid(row=0, column=1, padx=20, pady=0, sticky="w")

    car_model_label = tk.Label(car_details_frame, text="Car Model:", font=("Arial", 12), bg="#ffffff")
    car_model_label.grid(row=1, column=0, padx=20, pady=0, sticky="e")
    car_model_value = tk.Label(car_details_frame, font=("Arial", 12), bg="#ffffff")
    car_model_value.grid(row=1, column=1, padx=20, pady=0, sticky="w")

    car_type_label = tk.Label(car_details_frame, text="Car Type:", font=("Arial", 12), bg="#ffffff")
    car_type_label.grid(row=2, column=0, padx=20, pady=0, sticky="e")
    car_type_value = tk.Label(car_details_frame, font=("Arial", 12), bg="#ffffff")
    car_type_value.grid(row=2, column=1, padx=20, pady=0, sticky="w")

    # Function to open the "Add/Edit Your Car" window
    def open_add_edit_car_window():
        add_edit_car_window = tk.Toplevel(parent_frame)
        add_edit_car_window.title("Add/Edit Your Car")
        add_edit_car_window.geometry("400x300")

        # Car Plate Label and Entry
        car_plate_label = tk.Label(add_edit_car_window, text="Car Plate:", font=("Arial", 12))
        car_plate_label.grid(row=0, column=0, padx=20, pady=10, sticky="e")
        car_plate_entry = tk.Entry(add_edit_car_window, font=("Arial", 12), width=30)
        car_plate_entry.grid(row=0, column=1, padx=20, pady=10)

        # Car Model Label and Entry
        car_model_label = tk.Label(add_edit_car_window, text="Car Model:", font=("Arial", 12))
        car_model_label.grid(row=1, column=0, padx=20, pady=10, sticky="e")
        car_model_entry = tk.Entry(add_edit_car_window, font=("Arial", 12), width=30)
        car_model_entry.grid(row=1, column=1, padx=20, pady=10)

        # Car Type Label and Dropdown
        car_type_label = tk.Label(add_edit_car_window, text="Car Type:", font=("Arial", 12))
        car_type_label.grid(row=2, column=0, padx=20, pady=10, sticky="e")
        car_type_options = ["Sedan", "SUV", "Hatchback", "Convertible", "Coupe", "Minivan"]
        car_type_var = tk.StringVar(add_edit_car_window)
        car_type_var.set(car_type_options[0])  # Set default value
        car_type_dropdown = tk.OptionMenu(add_edit_car_window, car_type_var, *car_type_options)
        car_type_dropdown.config(font=("Arial", 12))
        car_type_dropdown.grid(row=2, column=1, padx=20, pady=10)

        # Function to save car details
        def save_car_details(car_plate, car_name, car_type):
            if not car_plate or not car_name or not car_type:
                messagebox.showerror("Validation Error", "All fields are required!")
                return

            try:
                # Connect to MySQL Database
                conn = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    password="",
                    database="carpool_system"
                )
                cursor = conn.cursor()

                # Insert or update car details in the database
                query = """
                    UPDATE user SET car_plate = %s, car_name = %s, car_type = %s WHERE id = %s
                """
                values = (car_plate, car_name, car_type, user_id)
                cursor.execute(query, values)
                conn.commit()

                messagebox.showinfo("Success", "Car details saved successfully!")
                add_edit_car_window.destroy()
                # Refresh the profile form to show the updated car details
                fetch_car_details()
            except mysql.connector.Error as err:
                messagebox.showerror("Database Error", f"Error saving car details: {err}")
            finally:
                cursor.close()
                conn.close()

        # Function to cancel and close the window
        def cancel_add_edit_car():
            add_edit_car_window.destroy()

        # Frame for buttons
        button_frame = tk.Frame(add_edit_car_window)
        button_frame.grid(row=3, column=0, columnspan=2, pady=20)

        # Cancel Button
        cancel_car_button = tk.Button(button_frame, text="Cancel", font=("Arial", 12), command=cancel_add_edit_car)
        cancel_car_button.pack(side="left", padx=10)

        # Save Button
        save_car_button = tk.Button(button_frame, text="Save Car", font=("Arial", 12), bg="#E21A22", fg="white", command=lambda: save_car_details(car_plate_entry.get(), car_model_entry.get(), car_type_var.get()))
        save_car_button.pack(side="right", padx=10)

        # Populate the form with existing car data if available
        if car_plate_value.cget("text") != "-":
            car_plate_entry.insert(0, car_plate_value.cget("text"))
            car_model_entry.insert(0, car_model_value.cget("text"))
            car_type_var.set(car_type_value.cget("text"))

    # Add/Edit Your Car Button
    add_edit_car_button = tk.Button(parent_frame, text="Add Your Car", font=("Arial", 12), bg="#E21A22", fg="white", command=open_add_edit_car_window)
    add_edit_car_button.grid(row=4, column=1, padx=20, pady=5, sticky="w")

    def fetch_car_details():
        try:
            # Connect to MySQL Database
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="carpool_system"
            )
            cursor = conn.cursor()

            # Fetch car details from the database
            query = "SELECT car_plate, car_name, car_type FROM user WHERE id = %s"
            cursor.execute(query, (user_id,))
            result = cursor.fetchone()

            if result and all(result):
                car_plate, car_name, car_type = result
                car_plate_value.config(text=car_plate)
                car_model_value.config(text=car_name)
                car_type_value.config(text=car_type)
                add_edit_car_button.config(text="Edit Car")  # Change button text to "Edit Car"
            else:
                car_plate_value.config(text="-")
                car_model_value.config(text="-")
                car_type_value.config(text="-")
                add_edit_car_button.config(text="Add Your Car")  # Change button text to "Add Your Car"
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error fetching car details: {err}")
        finally:
            cursor.close()
            conn.close()

    def enable_fields():
        user_name_entry.config(state=tk.NORMAL)
        email_entry.config(state=tk.NORMAL)
        phone_entry.config(state=tk.NORMAL)
        save_button.config(text="Save Changes", command=save_changes)

    def save_changes():
        user_name = user_name_entry.get()
        email = email_entry.get()
        phone = phone_entry.get()

        if not user_name or not email or not phone:
            messagebox.showerror("Validation Error", "All fields are required!")
            return

        try:
            # Connect to MySQL Database
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="carpool_system"
            )
            cursor = conn.cursor()

            # Update user details in the database
            query = """
                UPDATE user SET username = %s, email = %s, contact = %s WHERE id = %s
            """
            values = (user_name, email, phone, user_id)
            cursor.execute(query, values)
            conn.commit()

            messagebox.showinfo("Success", "Profile updated successfully!")
            save_button.config(text="Edit Profile", command=enable_fields)
            user_name_entry.config(state=tk.DISABLED)
            email_entry.config(state=tk.DISABLED)
            phone_entry.config(state=tk.DISABLED)
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error updating profile: {err}")
        finally:
            cursor.close()
            conn.close()

    save_button = tk.Button(parent_frame, text="Edit Profile", font=("Arial", 12), bg="#E21A22", fg="white", command=enable_fields)
    save_button.grid(row=8, column=0, columnspan=3, padx=20, pady=20, sticky="e")

    # Populate the form with user data if provided
    if user_data:
        print("User data received:", user_data)  # Debug print to check user_data
        user_name_entry.config(state=tk.NORMAL)
        user_name_entry.insert(0, user_data.get("username", ""))
        user_name_entry.config(state=tk.DISABLED)

        email_entry.config(state=tk.NORMAL)
        email_entry.insert(0, user_data.get("email", ""))
        email_entry.config(state=tk.DISABLED)

        phone_entry.config(state=tk.NORMAL)
        phone_entry.insert(0, user_data.get("contact", ""))
        phone_entry.config(state=tk.DISABLED)

    # Fetch and display car details
    fetch_car_details()

    return {
        "user_name_entry": user_name_entry,
        "email_entry": email_entry,
        "phone_entry": phone_entry
    }