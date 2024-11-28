
import tkinter as tk
from tkinter import messagebox
from tkcalendar import DateEntry  # Import DateEntry from tkcalendar
import mysql.connector
from datetime import datetime  # Import datetime module
from tkintermapview import TkinterMapView
from geopy.geocoders import Nominatim 
import requests
from create_carpool_form import create_carpool_form  # Import the create_carpool_form function
from search_carpool_form import search_carpool_form  # Import the search_carpool_form function
from profile_form import create_profile_form  # Import the create_profile_form function

GOOGLE_API_KEY = "AIzaSyC4GMTOjpDLoMQsQKBc1y64bPTwJFsPgBg"

# MySQL Database Configuration
DB_HOST = "localhost"  # Replace with your database host
DB_USER = "root"       # Replace with your MySQL username
DB_PASSWORD = ""  # Replace with your MySQL password
DB_NAME = "carpool_system"    # Replace with your database name

def open_student_page(user_id):
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
        hide_all_frames()
        main_menu_frame.pack()
        page_title_label.config(text="Home")

    def show_create_carpool_page():
        hide_all_frames()
        create_carpool_frame.pack()
        page_title_label.config(text="Create Carpool")

    def show_search_carpool_page():
        hide_all_frames()
        search_carpool_frame.pack()
        page_title_label.config(text="Search Carpool")

    def show_profile_page():
        hide_all_frames()
        profile_frame.pack()
        page_title_label.config(text="My Profile")
        fetch_and_display_user_data(user_id)

    def hide_all_frames():
        main_menu_frame.pack_forget()
        create_carpool_frame.pack_forget()
        search_carpool_frame.pack_forget()
        profile_frame.pack_forget()

    def create_carpool():
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

            # Insert data into the database
            query = """
                INSERT INTO carpool (carpool_name, available_seat, pickup_point, pickup_datetime, dropoff_time, status)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            values = (carpool_name, available_seat, pickup_point, pickup_datetime, dropoff_time, status)
            cursor.execute(query, values)
            conn.commit()

            messagebox.showinfo("Success", "Carpool created successfully!")
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error inserting data: {err}")

    # Function to search for the place and show it on the map
    def search_from_google_map():
        google_map_page = tk.Toplevel(create_carpool_frame)
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

    def fetch_and_display_user_data(user_id):
        try:
            # Fetch user data from the database
            query = "SELECT username, email, contact FROM User WHERE id = %s"
            cursor.execute(query, (user_id,))
            result = cursor.fetchone()

            if result:
                user_data = {
                    "username": result[0],
                    "email": result[1],
                    "contact": result[2]
                }
                # Populate the profile form with user data
                profile_form_entries["user_name_entry"].config(state=tk.NORMAL)
                profile_form_entries["user_name_entry"].delete(0, tk.END)
                profile_form_entries["user_name_entry"].insert(0, user_data["username"])
                profile_form_entries["user_name_entry"].config(state=tk.DISABLED)

                profile_form_entries["email_entry"].config(state=tk.NORMAL)
                profile_form_entries["email_entry"].delete(0, tk.END)
                profile_form_entries["email_entry"].insert(0, user_data["email"])
                profile_form_entries["email_entry"].config(state=tk.DISABLED)

                profile_form_entries["phone_entry"].config(state=tk.NORMAL)
                profile_form_entries["phone_entry"].delete(0, tk.END)
                profile_form_entries["phone_entry"].insert(0, user_data["contact"])
                profile_form_entries["phone_entry"].config(state=tk.DISABLED)
            else:
                messagebox.showerror("Error", "User data not found")
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error fetching user data: {err}")

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

    search_carpool_button = tk.Button(navbar_frame, text="Search Carpool", command=show_search_carpool_page, font=button_font, bg=button_bg, fg=button_fg, bd=0)
    search_carpool_button.pack(side="left", padx=10, pady=10)

    create_carpool_nav_button = tk.Button(navbar_frame, text="Create Carpool", command=show_create_carpool_page, font=button_font, bg=button_bg, fg=button_fg, bd=0)
    create_carpool_nav_button.pack(side="left", padx=10, pady=10)

    joined_carpool_button = tk.Button(navbar_frame, text="Joined Carpool", command=joined_carpool, font=button_font, bg=button_bg, fg=button_fg, bd=0)
    joined_carpool_button.pack(side="left", padx=10, pady=10)

    # Dropdown menu for "My Profile"
    profile_menu = tk.Menubutton(navbar_frame, text="My Profile", font=button_font, bg=button_bg, fg=button_fg, bd=0, relief="flat")
    profile_menu.menu = tk.Menu(profile_menu, tearoff=0)
    profile_menu["menu"] = profile_menu.menu

    profile_menu.menu.add_command(label="Manage Carpool", command=manage_carpool)
    profile_menu.menu.add_command(label="Profile", command=show_profile_page)
    profile_menu.menu.add_separator()
    profile_menu.menu.add_command(label="Logout", command=logout)

    profile_menu.pack(side="right", padx=(10, 20), pady=10)

    # Move notification icon to the left of the profile menu
    notification_icon = tk.Label(navbar_frame, text="🔔", font=button_font, bg=button_bg, fg=button_fg)
    notification_icon.pack(side="right", padx=10, pady=10)

    # Full-width bar for page title
    title_bar_frame = tk.Frame(carpool_app, bg="#000000")
    title_bar_frame.pack(fill="x", pady=(0,40))

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
    carpool_form_entries = create_carpool_form(create_carpool_frame, create_carpool, search_from_google_map)

    # Search Carpool frame
    search_carpool_frame = tk.Frame(carpool_app, bg="#ffffff")
    search_carpool_form_entries = search_carpool_form(search_carpool_frame)

    # Profile frame
    profile_frame = tk.Frame(carpool_app, bg="#ffffff")
    profile_form_entries = create_profile_form(profile_frame, user_id=user_id)

    # Footer frame
    footer_frame = tk.Frame(carpool_app, bg="red")
    footer_frame.pack(fill="x", side="bottom")

    footer_label = tk.Label(footer_frame, text="\u00A9 Copyright INTI International College Penang. All Rights Reserved", font=("Arial", 12), bg="red", fg="white")
    footer_label.pack(pady=10)

    carpool_app.mainloop()
    cursor.close()
    conn.close()