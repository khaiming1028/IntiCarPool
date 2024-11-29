import tkinter as tk
from tkinter import messagebox
from datetime import datetime  # Import datetime for fetching current time
import mysql.connector
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


# MySQL Database Configuration
DB_HOST = "localhost"  # Replace with your database host
DB_USER = "root"       # Replace with your MySQL username
DB_PASSWORD = ""  # Replace with your MySQL password
DB_NAME = "carpool_system"    # Replace with your database name

# Function to fetch and update the current time
def update_time_label():
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Format: Year-Month-Day Hour:Minute:Second
    time_label.config(text=current_time)  # Update the time label
    time_label.after(1000, update_time_label)  # Refresh the time every second

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
    
    # Function to open the carpool list window and connect to the database
    def open_carpool_list():
        # Create a new top-level window (this is the new window)
        carpool_list_window = tk.Toplevel()
        carpool_list_window.title("Carpool List")  # Title of the new window
        carpool_list_window.geometry("600x400")  # Set the size of the window (optional)

        # Create the listbox to display the carpool list
        carpool_listbox = tk.Listbox(carpool_list_window, height=10, width=80)
        carpool_listbox.pack(pady=20)

        # Create a scroll bar for the listbox
        scrollbar = tk.Scrollbar(carpool_list_window, orient="vertical", command=carpool_listbox.yview)
        carpool_listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        # Connect to the MySQL database
        try:
            conn = mysql.connector.connect(
                host=DB_HOST,
                user=DB_USER,
                password=DB_PASSWORD,
                database=DB_NAME
            )
            cursor = conn.cursor()

            # Fetch carpool data from the database
            query = "SELECT id, carpool_name, available_seat, pickup_point, pickup_datetime, status FROM carpool"
            cursor.execute(query)
            rows = cursor.fetchall()

            # Insert carpool data into the listbox
            for row in rows:
                carpool_listbox.insert(tk.END, f"ID: {row[0]} | Name: {row[1]} | Seats: {row[2]} | Pickup: {row[3]} | Time: {row[4]} | Status: {row[5]}")

        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error fetching data: {err}")

        def fetch_and_display_carpools():
            carpool_listbox.delete(0, tk.END)  # Clear previous entries
            try:
                query = "SELECT id, carpool_name, available_seat, pickup_point, pickup_datetime, status FROM carpool"
                cursor.execute(query)
                rows = cursor.fetchall()

                if not rows:
                    carpool_listbox.insert(tk.END, "No carpools available.")
                else:
                    for carpool in rows:
                        id, name, seat, pickup, time, status = carpool
                        display_text = (
                            f"Carpool ID: {id} | Name: {name} | Seats: {seat} | "
                            f"Pickup: {pickup} | Time: {time} | Status: {status}"
                        )
                        carpool_listbox.insert(tk.END, display_text)  # Insert into listbox
            except mysql.connector.Error as err:
                messagebox.showerror("Database Error", f"Error fetching data: {err}")


        # Function to delete a selected carpool from the list and database
        def delete_carpool():
            try:
                # Ensure a carpool is selected
                selected_index = carpool_listbox.curselection()
                if not selected_index:
                    messagebox.showerror("Selection Error", "Please select a carpool to delete.")
                    return

                # Get the selected carpool and extract the carpool ID
                selected_carpool = carpool_listbox.get(selected_index)
                print(f"Selected Carpool for Deletion: {selected_carpool}")  # Debugging
                carpool_id = selected_carpool.split('|')[0].split(': ')[1].strip()
                print(f"Carpool ID: {carpool_id}")  # Debugging

                # Check if carpool_id is valid (not empty or None)
                if not carpool_id:
                    messagebox.showerror("Error", "Invalid Carpool ID.")
                    return
        
                # Connect to the database and delete the carpool
                conn = mysql.connector.connect(
                    host=DB_HOST,
                    user=DB_USER,
                    password=DB_PASSWORD,
                    database=DB_NAME
                )
                cursor = conn.cursor()

                # Delete query
                delete_query = "DELETE FROM carpool WHERE id = %s"
                cursor.execute(delete_query, (carpool_id,))

                # Commit the changes
                conn.commit()

                # Check if a row was actually deleted
                if cursor.rowcount == 0:
                    messagebox.showwarning("No Deletions", "No carpool found with the selected ID.")
                else:
                    messagebox.showinfo("Success", "Carpool successfully deleted.")

                # Refresh the carpool list after deletion
                fetch_and_display_carpools()

            except mysql.connector.Error as err:
                messagebox.showerror("Database Error", f"Error deleting carpool: {err}")
            finally:
                # Close the connection
                if conn.is_connected():
                    cursor.close()
                    conn.close()


        # Function to edit a selected carpool
        def open_edit_carpool_window(carpool_id):
            # Open the edit carpool window
            edit_window = tk.Toplevel()  # Creates a new top-level window
            edit_window.title("Edit Carpool")

            # Set the window size (width x height)
            edit_window.geometry("400x400")

            # Fetch carpool details from the database based on carpool_id
            cursor.execute("SELECT carpool_name, available_seat, pickup_point, pickup_datetime, status FROM carpool WHERE id = %s", (carpool_id,))
            carpool = cursor.fetchone()
    
            if carpool is None:
                messagebox.showerror("Error", "Carpool not found.")
                return

            # Unpack the values returned from the query
            carpool_name, available_seat, pickup_point, pickup_datetime, status = carpool

            # Create Labels and Entries for editing
            carpool_name_label = tk.Label(edit_window, text="Carpool Name:")
            carpool_name_label.grid(row=0, column=0, sticky="e", padx=10, pady=10)
            carpool_name_entry = tk.Entry(edit_window)
            carpool_name_entry.grid(row=0, column=1, padx=10, pady=10)
            carpool_name_entry.insert(0, carpool_name)

            available_seat_label = tk.Label(edit_window, text="Available Seats:")
            available_seat_label.grid(row=1, column=0, sticky="e", padx=10, pady=10)
            available_seat_entry = tk.Entry(edit_window)
            available_seat_entry.grid(row=1, column=1, padx=10, pady=10)
            available_seat_entry.insert(0, available_seat)

            pickup_point_label = tk.Label(edit_window, text="Pickup Point:")
            pickup_point_label.grid(row=2, column=0, sticky="e", padx=10, pady=10)
            pickup_point_entry = tk.Entry(edit_window)
            pickup_point_entry.grid(row=2, column=1, padx=10, pady=10)
            pickup_point_entry.insert(0, pickup_point)

            pickup_time_label = tk.Label(edit_window, text="Pickup Time:")
            pickup_time_label.grid(row=3, column=0, padx=10, pady=10)
            pickup_time_entry = tk.Entry(edit_window)
            pickup_time_entry.grid(row=3, column=1, padx=10, pady=10)
            pickup_time_entry.insert(0, pickup_datetime)


            # The Save Changes button
            save_button = tk.Button(edit_window, text="Save Changes", command=lambda: save_changes(carpool_id, carpool_name_entry, available_seat_entry, pickup_point_entry))
            save_button.grid(row=3, columnspan=2, pady=20)  # Place button in the grid

            


            def save_changes():
                new_carpool_name = carpool_name_entry.get()
                new_available_seat = available_seat_entry.get()
                new_pickup_point = pickup_point_entry.get()
                new_pickup_time = pickup_time_entry.get()
                # Validate the fields
                if not new_carpool_name or not new_available_seat or not new_pickup_point or not new_pickup_time:
                    messagebox.showerror("Error", "All fields are required!")
                    return
        
                # Update the carpool in the database
                try:
                    cursor.execute("""
                        UPDATE carpool
                        SET carpool_name = %s, available_seat = %s, pickup_point = %s, pickup_datetime = %s, status = %s
                        WHERE id = %s
                    """, (new_carpool_name, new_available_seat, new_pickup_point, new_pickup_time, carpool_id))
                    conn.commit()  # Commit the changes to the database
                    messagebox.showinfo("Success", "Carpool updated successfully.")
                    edit_window.destroy()  # Close the edit window after saving
                    fetch_and_display_carpools()  # Refresh the carpool list

                except mysql.connector.Error as err:
                    messagebox.showerror("Database Error", f"Error updating carpool: {err}")




        # This function is called when the "Edit" button is pressed in the main window.
        def edit_carpool():
            # Ensure a carpool is selected
            selected_index = carpool_listbox.curselection()
            if not selected_index:
                messagebox.showerror("Selection Error", "Please select a carpool to edit.")
                return

            selected_carpool = carpool_listbox.get(selected_index)
            carpool_id = int(selected_carpool.split('|')[0].split(': ')[1].strip())  # Extract carpool ID from the selected text

            # Open the edit window for the selected carpool
            open_edit_carpool_window(carpool_id)


        # Create Delete and Edit Buttons
        delete_button = tk.Button(carpool_list_window, text="Delete Carpool", command=delete_carpool)
        delete_button.pack(pady=10)

        edit_button = tk.Button(carpool_list_window, text="Edit Carpool", command=edit_carpool)
        edit_button.pack(pady=10)

        # Add a button to close the window
        close_button = tk.Button(carpool_list_window, text="Close", command=carpool_list_window.destroy)
        close_button.pack(pady=10)

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
        
    def create_graph(total_users, total_carpools):
        # Create a bar chart
        categories = ['Total Users', 'Total Carpools']
        values = [total_users, total_carpools]

        fig, ax = plt.subplots(figsize=(5, 3))
        ax.bar(categories, values, color=['#007bff', '#28a745'])
        ax.set_title('Carpool System Overview')
        ax.set_ylabel('Counts')
        ax.set_ylim(0, max(values) + 10)  # Add some space above the highest bar

        return fig

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

    carpool_list_button = tk.Button(navbar_frame, text="Carpool List", command=open_carpool_list, font=button_font, bg=button_bg, fg=button_fg, bd=0)
    carpool_list_button.pack(side="left", padx=10, pady=10)

    student_list_button = tk.Button(navbar_frame, text="Student List", command=open_student_list, font=button_font, bg=button_bg, fg=button_fg, bd=0)
    student_list_button.pack(side="left", padx=10, pady=10)

    # Dropdown menu for "My Profile"
    profile_menu = tk.Menubutton(navbar_frame, text="My Profile", font=button_font, bg=button_bg, fg=button_fg, bd=0, relief="flat")
    profile_menu.menu = tk.Menu(profile_menu, tearoff=0)
    profile_menu["menu"] = profile_menu.menu

    profile_menu.menu.add_command(label="Profile", command=profile)
    profile_menu.menu.add_separator()
    profile_menu.menu.add_command(label="Logout", command=logout)

    profile_menu.pack(side="right", padx=(10, 20), pady=10)

   # Main content frame
    main_content_frame = tk.Frame(carpool_app, bg="#f5f5f5")
    main_content_frame.pack(fill="both", expand=True, pady=20)

    # Box Frame (For Total Users and Total Carpools Boxes)
    box_frame = tk.Frame(main_content_frame, bg="#f5f5f5")  # Light gray background
    box_frame.pack(pady=20)

    # Box Style
    box_style = {
        "bg": "#ffffff",
        "relief": "solid",
        "bd": 1,
        "highlightthickness": 2,
        "highlightbackground": "#d1d1d1"
    }

    # Current Time Box
    time_frame = tk.Frame(box_frame, **box_style)
    time_frame.grid(row=0, column=2, padx=40, pady=10)

    time_label_title = tk.Label(time_frame, text="Current Date and Time", font=("Arial", 12), bg="#ffffff")
    time_label_title.pack(pady=(10, 0))

    # Dynamic Time Label
    global time_label
    time_label = tk.Label(time_frame, text="", font=("Arial", 24, "bold"), bg="#ffffff")
    time_label.pack(pady=(0, 10))

    # Initialize time update
    update_time_label()

    # Total Users Box
    users_frame = tk.Frame(box_frame, **box_style)
    users_frame.grid(row=0, column=0, padx=40, pady=10)  # Increased padding

    users_label = tk.Label(users_frame, text="Total Users", font=("Arial", 12), bg="#ffffff")
    users_label.pack(pady=(10, 0))  # Padding at the top only

    users_count_label = tk.Label(users_frame, text=str(total_users), font=("Arial", 24, "bold"), bg="#ffffff")
    users_count_label.pack(pady=(0, 10))  # Padding at the bottom only

    # Total Carpools Box
    carpools_frame = tk.Frame(box_frame, **box_style)
    carpools_frame.grid(row=0, column=1, padx=40, pady=10)  # Add spacing between boxes

    carpools_label = tk.Label(carpools_frame, text="Total Carpools", font=("Arial", 12), bg="#ffffff")
    carpools_label.pack(pady=(10, 0))  # Padding at the top only

    carpools_count_label = tk.Label(carpools_frame, text="3", font=("Arial", 24, "bold"), bg="#ffffff")
    carpools_count_label.pack(pady=(0, 10))  # Padding at the bottom only

    # Graph Frame
    graph_frame = tk.Frame(main_content_frame, bg="#f5f5f5")
    graph_frame.pack(pady=20)  # Add padding above the graph

    # Matplotlib graph integration
    figure = plt.Figure(figsize=(5, 3), dpi=100)
    ax = figure.add_subplot(111)
    ax.bar(["Total Users", "Total Carpools"], [total_users, total_carpools], color=["blue", "green"])
    ax.set_title("Carpool System Overview")
    ax.set_ylabel("Counts")

    canvas = FigureCanvasTkAgg(figure, master=graph_frame)
    canvas.get_tk_widget().pack()

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

    # Footer frame
    footer_frame = tk.Frame(carpool_app, bg="red")
    footer_frame.pack(fill="x", side="bottom")

    footer_label = tk.Label(footer_frame, text="\u00A9 Copyright INTI International College Penang. All Rights Reserved", font=("Arial", 12), bg="red", fg="white")
    footer_label.pack(pady=10)

    carpool_app.mainloop()
    cursor.close()
    conn.close()
