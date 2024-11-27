import tkinter as tk
from tkinter import messagebox
import carpool_form  # Import the renamed module
import carpool_list
import mysql.connector


# MySQL Database Configuration
DB_HOST = "localhost"  # Replace with your database host
DB_USER = "root"       # Replace with your MySQL username
DB_PASSWORD = ""  # Replace with your MySQL password
DB_NAME = "carpool_system"    # Replace with your database name

def open_admin_page():
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

    def open_student_list():
        # Create a new window for displaying the student list
        student_list_window = tk.Toplevel(carpool_app)
        student_list_window.title("Student List")
        student_list_window.geometry("500x400")

        # Add a scrollbar
        scrollbar = tk.Scrollbar(student_list_window)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Create a listbox for displaying usernames and car names
        listbox = tk.Listbox(student_list_window, font=("Arial", 12), width=50)
        listbox.pack(fill=tk.BOTH, expand=True)
        listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=listbox.yview)

        button_frame = tk.Frame(student_list_window)
        button_frame.pack(fill=tk.X, pady=10)

        

        # Connect to the database
        try:
            conn = mysql.connector.connect(
                host=DB_HOST,
                user=DB_USER,
                password=DB_PASSWORD,
                database=DB_NAME
            )
            cursor = conn.cursor()

            # Fetch usernames and car names from the User table
            query = "SELECT username, car_name FROM User"
            cursor.execute(query)
            results = cursor.fetchall()

            # Populate the listbox with results
            for row in results:
                username, car_name = row
                car_name = car_name if car_name else "No Car Info"  # Handle missing car names
                listbox.insert(tk.END, f"Username: {username} | Car: {car_name}")

        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")

        # Delete user function
        def delete_user():
            selected_index = listbox.curselection()
            if not selected_index:
                messagebox.showwarning("No Selection", "Please select a user to delete.")
                return

            # Get the username from the selected index
            selected_entry = listbox.get(selected_index[0])
            username = selected_entry.split(" | ")[0].replace("Username: ", "").strip()

            # Confirm deletion
            confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this user?")
            if confirm:
                try:
                    # Debugging: Print username to ensure correctness
                    print(f"Attempting to delete user: {username}")

                    # Delete the user from the database
                    delete_query = "DELETE FROM User WHERE username = %s"
                    cursor.execute(delete_query, (username,))
                
                    # Commit changes to the database
                    conn.commit()

                    # Check if any row was affected
                    if cursor.rowcount > 0:
                        # Remove the user from the listbox
                        listbox.delete(selected_index[0])
                        messagebox.showinfo("Success", f"User '{username}' deleted successfully.")
                    else:
                        messagebox.showerror("Error", f"No user found with username '{username}'. Deletion failed.")

                except mysql.connector.Error as err:
                    messagebox.showerror("Database Error", f"Error: {err}")
                except Exception as e:
                    messagebox.showerror("Error", f"Unexpected error: {e}")

        # Add Delete Button
        delete_button = tk.Button(button_frame, text="Delete User", command=delete_user, font=("Arial", 12), bg="red", fg="white")
        delete_button.pack(side=tk.LEFT, padx=10)

        # Close database connection when window is closed
        def on_close():
            if cursor:
                cursor.close()
            if conn:
                conn.close()
            student_list_window.destroy()

        student_list_window.protocol("WM_DELETE_WINDOW", on_close)

    def search_carpool():
        # Implement search carpool functionality
        page_title_label.config(text="Search Carpool")

    def joined_carpool():
        # Implement joined carpool functionality
        page_title_label.config(text="Joined Carpool")

    def manage_carpool():
        # Implement manage carpool functionality
        page_title_label.config(text="Manage Carpool")

    def profile():
        # Implement profile functionality
        page_title_label.config(text="Profile")

    def logout():
        carpool_app.destroy()

    # Function to fetch counts
    def fetch_counts():
        try:
            # Fetch total users
            cursor.execute("SELECT COUNT(*) FROM User")
            total_users = cursor.fetchone()[0]

            # Fetch total carpools
            cursor.execute("SELECT COUNT(*) FROM carpool")
            total_carpools = cursor.fetchone()[0]

            return total_users, total_carpools
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error fetching data: {err}")
            return 0, 0

    # Fetch the counts
    total_users, total_carpools = fetch_counts()

    # Navbar frame
    navbar_frame = tk.Frame(carpool_app, bg="#ffffff")
    navbar_frame.pack(fill="x", pady=(0,5))  # Add padding to the bottom

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

    student_list_button = tk.Button(navbar_frame, text="Student List", command=open_student_list, font=button_font, bg=button_bg, fg=button_fg, bd=0)
    student_list_button.pack(side="left", padx=10, pady=10)

    # Dropdown menu for "My Profile"
    profile_menu = tk.Menubutton(navbar_frame, text="My Profile", font=button_font, bg=button_bg, fg=button_fg, bd=0, relief="flat")
    profile_menu.menu = tk.Menu(profile_menu, tearoff=0)
    profile_menu["menu"] = profile_menu.menu

    profile_menu.menu.add_command(label="Manage Carpool", command=manage_carpool)
    profile_menu.menu.add_command(label="Profile", command=profile)
    profile_menu.menu.add_separator()
    profile_menu.menu.add_command(label="Logout", command=logout)

    profile_menu.pack(side="right", padx=(10, 20), pady=10)

   # Main Content Frame (Background for the white area)
    main_content_frame = tk.Frame(carpool_app, bg="#f5f5f5")
    main_content_frame.pack(fill="both", expand=True)

    # Box Frame (For Total Users and Total Carpools Boxes)
    box_frame = tk.Frame(main_content_frame, bg="#f5f5f5")  # Light gray background
    box_frame.place(relx=0.5, rely=0.5, anchor="center")  # Center the boxes in the middle of the frame

    # Total Users Box
    users_frame = tk.Frame(box_frame, bg="#ffffff", relief="solid", bd=1)  # White background, bordered box
    users_frame.grid(row=0, column=0, padx=20, pady=10)  # Add spacing between boxes

    users_label = tk.Label(users_frame, text="Total Users", font=("Arial", 12), bg="#ffffff")
    users_label.pack(pady=(10, 0))  # Padding at the top only

    users_count_label = tk.Label(users_frame, text="2", font=("Arial", 24, "bold"), bg="#ffffff")
    users_count_label.pack(pady=(0, 10))  # Padding at the bottom only

    # Total Carpools Box
    carpools_frame = tk.Frame(box_frame, bg="#ffffff", relief="solid", bd=1)  # White background, bordered box
    carpools_frame.grid(row=0, column=1, padx=20, pady=10)  # Add spacing between boxes

    carpools_label = tk.Label(carpools_frame, text="Total Carpools", font=("Arial", 12), bg="#ffffff")
    carpools_label.pack(pady=(10, 0))  # Padding at the top only

    carpools_count_label = tk.Label(carpools_frame, text="3", font=("Arial", 24, "bold"), bg="#ffffff")
    carpools_count_label.pack(pady=(0, 10))  # Padding at the bottom only

    # Move notification icon to the left of the profile menu
    notification_icon = tk.Label(navbar_frame, text="🔔", font=button_font, bg=button_bg, fg=button_fg)
    notification_icon.pack(side="right", padx=10, pady=10)

    # Full-width bar for page title
    title_bar_frame = tk.Frame(carpool_app, bg="#000000")
    title_bar_frame.pack(fill="x", pady=0)

    page_title_label = tk.Label(title_bar_frame, text="Home", font=("Arial", 14, "bold"), bg="#000000", fg="#ffffff")
    page_title_label.pack(side="left", pady=15, padx=5)

    # Main menu frame
    main_menu_frame = tk.Frame(carpool_app, bg="#ffffff")
    main_menu_frame.pack(fill="both", expand=True, pady=(10, 0))  # Adjust top margin

    # # Option 1: View Carpool
    # view_carpool_button = tk.Button(main_menu_frame, text="View Carpool", font=("Arial", 12), bg="blue", fg="white", width=20)
    # view_carpool_button.pack(pady=10)

    # # Option 2: Join Carpool
    # join_carpool_button = tk.Button(main_menu_frame, text="Join Carpool", font=("Arial", 12), bg="blue", fg="white", width=20)
    # join_carpool_button.pack(pady=10)

    # # Option 3: Create Carpool
    # create_carpool_button = tk.Button(main_menu_frame, text="Create Carpool", command=create_carpool, font=("Arial", 12), bg="blue", fg="white", width=20)
    # create_carpool_button.pack(pady=10)

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


    # Footer frame
    footer_frame = tk.Frame(carpool_app, bg="red")
    footer_frame.pack(fill="x", side="bottom")

    footer_label = tk.Label(footer_frame, text="\u00A9 Copyright INTI International College Penang. All Rights Reserved", font=("Arial", 12), bg="red", fg="white")
    footer_label.pack(pady=10)

    carpool_app.mainloop()
    cursor.close()
    conn.close()
