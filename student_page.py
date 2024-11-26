import tkinter as tk
from tkinter import messagebox
import mysql.connector

# MySQL Database Configuration
DB_HOST = "localhost"  # Replace with your database host
DB_USER = "root"       # Replace with your MySQL username
DB_PASSWORD = ""  # Replace with your MySQL password
DB_NAME = "carpool_system"    # Replace with your database name

def open_student_page():
    # Connect to MySQL Database
    try:
        conn = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        cursor = conn.cursor()
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error connecting to database: {err}")
        return
    
    # Create the carpool window
    carpool_app = tk.Tk()
    carpool_app.title("Carpool Options")
    carpool_app.attributes("-fullscreen", True)  # Set to full-screen

    # Add escape key event to exit full-screen mode
    carpool_app.bind("<Escape>", lambda e: carpool_app.attributes("-fullscreen", False))

    # Define button functions for carpool options
    def show_main_menu():
        create_carpool_frame.pack_forget()
        main_menu_frame.pack()
        page_title_label.config(text="Home")
        
    def show_create_carpool_page():
        main_menu_frame.pack_forget()
        create_carpool_frame.pack()
        page_title_label.config(text="Create Carpool")

    def create_carpool():
        # Get user input
        carpool_name = carpool_name_entry.get()
        person_limit = carpool_available_seat_entry.get()
        pickup_point = carpool_pickup_point_entry.get()
        pickup_time = carpool_pickup_time_entry.get()
        dropoff_time = carpool_dropoff_time_entry.get()
        status = selected_status.get()

        # Validate input
        if not all([carpool_name, person_limit, pickup_point, pickup_time, dropoff_time]):
            messagebox.showerror("Input Error", "All fields are required!")
            return

        try:
            # Insert data into the database
            query = """
                INSERT INTO carpool (carpool_name, person_limit, pickup_point, pickup_time, dropoff_time, status)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            values = (carpool_name, person_limit, pickup_point, pickup_time, dropoff_time, status)
            cursor.execute(query, values)
            conn.commit()

            messagebox.showinfo("Success", "Carpool created successfully!")
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error inserting data: {err}")

    def search_carpool():
        # Implement search carpool functionality
        page_title_label.config(text="Search Carpool")

    def joined_carpool():
        # Implement joined carpool functionality
        page_title_label.config(text="Joined Carpool")

    def manage_carpool():
        # Implement manage carpool functionality
        page_title_label.config(text="Manage Carpool")
        
    def view_carpool():
    # Clear previous frames and switch to the View Carpool frame
        create_carpool_frame.pack_forget()
        main_menu_frame.pack_forget()
        view_carpool_frame.pack(fill="both", expand=True)
        page_title_label.config(text="View Carpool")

        # Clear the listbox to refresh data
        carpool_listbox.delete(0, tk.END)

        try:
            # Fetch all data from the carpool table
            query = "SELECT carpool_name, available_seat, pickup_point, pickup_time, dropoff_time, status FROM carpool"
            cursor.execute(query)
            rows = cursor.fetchall()

            if not rows:
                carpool_listbox.insert(tk.END, "No carpools found.")
            else:
                for row in rows:
                    carpool_listbox.insert(
                        tk.END,
                        f"Name: {row[0]}, Seats: {row[1]}, Pickup: {row[2]}, Pickup Time: {row[3]}, Dropoff Time: {row[4]}, Status: {row[5]}"
                    )
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error fetching data: {err}")

    def profile():
        # Implement profile functionality
        page_title_label.config(text="Profile")

    def logout():
        carpool_app.destroy()
        cursor.close()
        conn.close()

    # Navbar frame
    navbar_frame = tk.Frame(carpool_app, bg="#ffffff")
    navbar_frame.pack(fill="x")  # Add padding to the bottom

    # Load the image
    logo_image = tk.PhotoImage(file="INTIlogo.png")
    logo_label = tk.Label(navbar_frame, image=logo_image, bg="#ffffff")
    logo_label.pack(side="left", padx=20)

    # Navbar buttons
    button_font = ("Arial", 12, "bold")
    button_bg = "#ffffff"
    button_fg = "#666666"

    home_button = tk.Button(navbar_frame, text="Home", command=show_main_menu, font=button_font, bg=button_bg, fg=button_fg, bd=0)
    home_button.pack(side="left", padx=10, pady=10)

    search_carpool_button = tk.Button(navbar_frame, text="Search Carpool", command=search_carpool, font=button_font, bg=button_bg, fg=button_fg, bd=0)
    search_carpool_button.pack(side="left", padx=10, pady=10)

    create_carpool_nav_button = tk.Button(navbar_frame, text="Create Carpool", command=show_create_carpool_page, font=button_font, bg=button_bg, fg=button_fg, bd=0)
    create_carpool_nav_button.pack(side="left", padx=10, pady=10)

    joined_carpool_button = tk.Button(navbar_frame, text="Joined Carpool", command=joined_carpool, font=button_font, bg=button_bg, fg=button_fg, bd=0)
    joined_carpool_button.pack(side="left", padx=10, pady=10)

    view_carpool_button = tk.Button(navbar_frame, text="View Carpool", command=view_carpool, font=button_font, bg=button_bg, fg=button_fg, bd=0)
    view_carpool_button.pack(side="left", padx=10, pady=10)

    # Dropdown menu for "My Profile"
    profile_menu = tk.Menubutton(navbar_frame, text="My Profile", font=button_font, bg=button_bg, fg=button_fg, bd=0, relief="flat")
    profile_menu.menu = tk.Menu(profile_menu, tearoff=0)
    profile_menu["menu"] = profile_menu.menu

    profile_menu.menu.add_command(label="Manage Carpool", command=manage_carpool)
    profile_menu.menu.add_command(label="Profile", command=profile)
    profile_menu.menu.add_separator()
    profile_menu.menu.add_command(label="Logout", command=logout)

    profile_menu.pack(side="right", padx=(10, 20), pady=10)

    # Move notification icon to the left of the profile menu
    notification_icon = tk.Label(navbar_frame, text="🔔", font=button_font, bg=button_bg, fg=button_fg)
    notification_icon.pack(side="right", padx=10, pady=10)

    # Full-width bar for page title
    title_bar_frame = tk.Frame(carpool_app, bg="#000000")
    title_bar_frame.pack(fill="x", pady=(0, 40))

    page_title_label = tk.Label(title_bar_frame, text="Home", font=("Arial", 14, "bold"), bg="#000000", fg="#ffffff")
    page_title_label.pack(side="left", pady=15, padx=20)

    # Main menu frame
    main_menu_frame = tk.Frame(carpool_app, bg="#ffffff")
    main_menu_frame.pack()
    tk.Label(main_menu_frame, text="Welcome to IICP Carpooling System", font=("Arial", 18, "bold"), bg="#ffffff").pack(pady=20)
    tk.Label(main_menu_frame, text="Connect with fellow IICP students to carpool together to campus, reduce traffic congestion, and lower your carbon footprint!", font=("Arial", 12), bg="#ffffff").pack(pady=10)
    car_image = tk.PhotoImage(file="homeCar.png")
    car_image_label = tk.Label(main_menu_frame, image=car_image, bg="#ffffff")
    car_image_label.pack(pady=20)
    tk.Button(main_menu_frame, text="Search for Carpools", command=search_carpool, font=("Arial", 14), bg="#dd6f6f", fg="#ffffff").pack(pady=20)

    # Create Carpool frame
    create_carpool_frame = tk.Frame(carpool_app, bg="#ffffff")

    # Carpool Name Label and Entry
    carpool_name_label = tk.Label(create_carpool_frame, text="Carpool Name:", font=("Arial", 12), bg="#ffffff")
    carpool_name_label.grid(row=0, column=0, padx=10, pady=5, sticky="e")
    carpool_name_entry = tk.Entry(create_carpool_frame, font=("Arial", 12), width=30)
    carpool_name_entry.grid(row=0, column=1, padx=10, pady=5)

    # Carpool Available Seats Label and Entry
    carpool_available_seat_label = tk.Label(create_carpool_frame, text="Available Seats:", font=("Arial", 12), bg="#ffffff")
    carpool_available_seat_label.grid(row=1, column=0, padx=10, pady=5, sticky="e")
    carpool_available_seat_entry = tk.Entry(create_carpool_frame, font=("Arial", 12), width=30)
    carpool_available_seat_entry.grid(row=1, column=1, padx=10, pady=5)

    # Carpool Pickup Point Label and Entry
    carpool_pickup_point_label = tk.Label(create_carpool_frame, text="Pickup Point:", font=("Arial", 12), bg="#ffffff")
    carpool_pickup_point_label.grid(row=2, column=0, padx=10, pady=5, sticky="e")
    carpool_pickup_point_entry = tk.Entry(create_carpool_frame, font=("Arial", 12), width=30)
    carpool_pickup_point_entry.grid(row=2, column=1, padx=10, pady=5)

    # Carpool Time Label and Entry
    carpool_pickup_time_label = tk.Label(create_carpool_frame, text="Time:", font=("Arial", 12), bg="#ffffff")
    carpool_pickup_time_label.grid(row=3, column=0, padx=10, pady=5, sticky="e")
    carpool_pickup_time_entry = tk.Entry(create_carpool_frame, font=("Arial", 12), width=30)
    carpool_pickup_time_entry.grid(row=3, column=1, padx=10, pady=5)

    # Carpool Dropoff Time Label and Entry
    carpool_dropoff_time_label = tk.Label(create_carpool_frame, text="Dropoff Time:", font=("Arial", 12), bg="#ffffff")
    carpool_dropoff_time_label.grid(row=4, column=0, padx=10, pady=5, sticky="e")
    carpool_dropoff_time_entry = tk.Entry(create_carpool_frame, font=("Arial", 12), width=30)
    carpool_dropoff_time_entry.grid(row=4, column=1, padx=10, pady=5)

    # Create the label for carpool status
    carpool_status_label = tk.Label(create_carpool_frame, text="Status:", font=("Arial", 12), bg="#ffffff")
    carpool_status_label.grid(row=5, column=0, padx=10, pady=5, sticky="e")

    # Define the dropdown options for carpool status
    status_options = ["Available", "Closed"]

    # Create a StringVar to hold the selected status
    selected_status = tk.StringVar()
    selected_status.set(status_options[0])  # Set the default value to "Available"

    # Create the dropdown (OptionMenu) for carpool status
    carpool_status_dropdown = tk.OptionMenu(create_carpool_frame, selected_status, *status_options)
    carpool_status_dropdown.config(font=("Arial", 12), width=27)  # Customize dropdown style
    carpool_status_dropdown.grid(row=5, column=1, padx=10, pady=5)

    # Submit Button
    submit_button = tk.Button(create_carpool_frame, text="Submit", command=create_carpool, font=("Arial", 12), bg="green", fg="white", width=10)
    submit_button.grid(row=6, columnspan=2, pady=10)

<<<<<<< HEAD
=======
        # View Carpool frame
    view_carpool_frame = tk.Frame(carpool_app, bg="#f5f5f5")  # Light background color

    # Title label with enhanced styling
    view_carpool_title_label = tk.Label(
        view_carpool_frame,
        text="Available Carpools",
        font=("Arial", 16, "bold"),
        bg="#f5f5f5",
        fg="#333333"  # Dark gray text
    )
    view_carpool_title_label.pack(pady=(20, 10))

    # Frame to hold the Listbox and scrollbar
    carpool_list_frame = tk.Frame(view_carpool_frame, bg="#f5f5f5")
    carpool_list_frame.pack(pady=10, padx=20)

    # Scrollbar for the Listbox
    scrollbar = tk.Scrollbar(carpool_list_frame)
    scrollbar.pack(side="right", fill="y")

    # Listbox to display carpool data with styled borders and font
    carpool_listbox = tk.Listbox(
        carpool_list_frame,
        font=("Arial", 12),
        width=80,
        height=15,
        bg="#ffffff",
        fg="#333333",
        bd=2,
        relief="groove",  # Border style
        yscrollcommand=scrollbar.set
    )
    carpool_listbox.pack(side="left", fill="both", expand=True)
    scrollbar.config(command=carpool_listbox.yview)

    # Fetch and Display Carpool Data with a Join Button
    def fetch_and_display_carpools():
        carpool_listbox.delete(0, tk.END)  # Clear previous entries
        try:
            query = "SELECT carpool_id, carpool_name, available_seat, pickup_point, pickup_time, status FROM carpool"
            cursor.execute(query)
            results = cursor.fetchall()

            for carpool in results:
                carpool_id, name, seat, pickup, time, status = carpool
                display_text = (
                    f"Carpool ID: {carpool_id} | Name: {name} | Seats: {seat} | "
                    f"Pickup: {pickup} | Time: {time} | Status: {status}"
                )
                carpool_listbox.insert(tk.END, display_text)

        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error fetching data: {err}")

    # Call fetch function to display carpools
    fetch_and_display_carpools()

    # Join Carpool Functionality
    def join_carpool():
        try:
            # Get selected carpool ID from the listbox
            selected_index = carpool_listbox.curselection()
            if not selected_index:
                messagebox.showerror("Selection Error", "Please select a carpool to join.")
                return

            selected_carpool = carpool_listbox.get(selected_index)
            carpool_id = selected_carpool.split('|')[0].split(': ')[1]  # Extract carpool ID from text

            # Insert into carpool_application table
            query = """
                INSERT INTO carpool_application (carpool_id, user_id, status)
                VALUES (%s, %s, %s)
            """
            values = (carpool_id, 1, "Pending")  # Replace `1` with the logged-in user ID
            cursor.execute(query)
            conn.commit()

            messagebox.showinfo("Success", f"You have successfully applied to join Carpool ID {carpool_id}.")

        except mysql.connector.IntegrityError:
            messagebox.showerror("Error", "You have already applied to this carpool.")
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error joining carpool: {err}")

    # Join Carpool Button
    join_carpool_button = tk.Button(
        view_carpool_frame,
        text="Join Selected Carpool",
        command=join_carpool,
        font=("Arial", 12, "bold"),
        bg="#28a745",  # Green background
        fg="white",
        bd=0,
        padx=10,
        pady=5
    )
    join_carpool_button.pack(pady=20)

    # Back to Home Button
    back_to_home_button = tk.Button(
        view_carpool_frame,
        text="Back to Home",
        command=show_main_menu,
        font=("Arial", 12, "bold"),
        bg="#007bff",  # Blue background
        fg="white",
        bd=0,
        padx=10,
        pady=5
    )
    back_to_home_button.pack(pady=10)

   
>>>>>>> 42debf7df002d19f3663381e0403213b5f78f3c3
    # Footer frame
    footer_frame = tk.Frame(carpool_app, bg="red")  
    footer_frame.pack(fill="x", side="bottom")

    footer_label = tk.Label(footer_frame, text="\u00A9 Copyright INTI International College Penang. All Rights Reserved", font=("Arial", 12), bg="red", fg="white")
    footer_label.pack(pady=10)

    carpool_app.mainloop()

    # Close the database connection after app is closed
    cursor.close()
    conn.close()