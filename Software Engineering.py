import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import student_page
import mysql.connector

# Database connection
mysqldb = mysql.connector.connect(host="localhost", user="root", password="", database="carpool_system")
mysqlcursor = mysqldb.cursor()

#create carpool_application table
# mysqlcursor.execute("create table Carpool_Application(id INT,user_id INT,carpool_id INT)")
#Create Carpool table
#mysqlcursor.execute("create table Carpool(id INT,driver_id INT,carpool_name VARCHAR(30),available_seat INT,pickup_point VARCHAR(30),pickup_time VARCHAR(30),dropoff_time VARCHAR(30),status VARCHAR(30))")
#mysqlcursor.execute("ALTER TABLE Carpool ADD CONSTRAINT fk_driver_id FOREIGN KEY (driver_id) REFERENCES user(id) ON DELETE CASCADE ON UPDATE CASCADE")
#Create User table
#mysqlcursor.execute("create table User(id INT,email VARCHAR(30),username VARCHAR(30),password VARCHAR(30),contact VARCHAR(30),car_type VARCHAR(30),car_name VARCHAR(30),car_plate VARCHAR(30))")
#create feedback table
#mysqlcursor.execute("create table Carpool_Application(id INT,user_id INT,carpool_id INT)")
# mysqlcursor.execute("ALTER TABLE Carpool_Application ADD COLUMN status VARCHAR(30)")
##
#mysqlcursor.execute("ALTER TABLE Carpool_Application ADD COLUMN feedback INT")
##
#mysqlcursor.execute("ALTER TABLE Car CHANGE car_id id INT")

user_id = None



# Function to handle login
def check_login():
    global user_id
    username = username_entry.get()
    password = password_entry.get()

    if username == "nimda" and password == "321":
        messagebox.showinfo("Admin Login", "Welcome, Admin!")
        app.destroy()
        import admin_page
        admin_page.open_admin_page()
        return

    if not username or not password:
        messagebox.showerror("Login Failed", "Username and Password cannot be empty")
        return

    try:
        query = "SELECT id FROM User WHERE username = %s AND password = %s"
        mysqlcursor.execute(query, (username, password))
        result = mysqlcursor.fetchone()

        if result:
            user_id = result[0]
            messagebox.showinfo("Login Successful", f"Welcome, {username}")
            app.destroy()
            import student_page
            student_page.open_student_page(user_id)
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")
    except mysql.connector.Error as e:
        messagebox.showerror("Database Error", f"An error occurred: {e}")

# Function to exit fullscreen
def exit_fullscreen(event=None):
    app.attributes('-fullscreen', False)

# Function to open "Create Account" window
def open_create_account_window():
    create_account_window = tk.Toplevel(app)
    create_account_window.title("Create Account")
    create_account_window.geometry("400x400")
    create_account_window.configure(bg="#ffffff")

    title_label = tk.Label(create_account_window, text="Create Account", font=("Arial", 16, "bold"), bg="#ffffff")
    title_label.pack(pady=10)

    frame = ttk.Frame(create_account_window)
    frame.pack(pady=10)

    email_label = tk.Label(frame, text="Email:", font=("Arial", 12), bg="#ffffff")
    email_label.grid(row=0, column=0, padx=10, pady=5, sticky="e")
    email_entry = ttk.Entry(frame, font=("Arial", 12), width=30)
    email_entry.grid(row=0, column=1, padx=10, pady=5)

    username_label = tk.Label(frame, text="Username:", font=("Arial", 12), bg="#ffffff")
    username_label.grid(row=1, column=0, padx=10, pady=5, sticky="e")
    username_entry = ttk.Entry(frame, font=("Arial", 12), width=30)
    username_entry.grid(row=1, column=1, padx=10, pady=5)

    password_label = tk.Label(frame, text="Password:", font=("Arial", 12), bg="#ffffff")
    password_label.grid(row=2, column=0, padx=10, pady=5, sticky="e")
    password_entry = ttk.Entry(frame, show="*", font=("Arial", 12), width=30)
    password_entry.grid(row=2, column=1, padx=10, pady=5)

    contact_label = tk.Label(frame, text="Contact:", font=("Arial", 12), bg="#ffffff")
    contact_label.grid(row=3, column=0, padx=10, pady=5, sticky="e")
    contact_entry = ttk.Entry(frame, font=("Arial", 12), width=30)
    contact_entry.grid(row=3, column=1, padx=10, pady=5)

    def create_account():
        email = email_entry.get()
        username = username_entry.get()
        password = password_entry.get()
        contact = contact_entry.get()

        if not email.endswith('@student.newinti.edu.my'):
            messagebox.showerror("Invalid Email", "Email must end with '@student.newinti.edu.my'")
            return

        if not username or not password:
            messagebox.showerror("Input Error", "Username and Password cannot be empty")
            return

        try:
            sql = "INSERT INTO User (email, username, password, contact) VALUES (%s, %s, %s, %s)"
            values = (email, username, password, contact)
            mysqlcursor.execute(sql, values)
            mysqldb.commit()
            messagebox.showinfo("Account Created", "Your account has been successfully created.")
            create_account_window.destroy()
        except Exception as e:
            messagebox.showerror("Database Error", f"Failed to create account: {e}")

    create_account_button = tk.Button(create_account_window, text="Create Account", font=("Arial", 12),
                                       bg="#dd6f6f", fg="white", command=create_account, relief="flat", bd=3)
    create_account_button.pack(pady=20)

# Function to open "Forgot Password" window
def open_forgot_password_window():
    forgot_password_window = tk.Toplevel(app)
    forgot_password_window.title("Forgot Password")
    forgot_password_window.geometry("300x200")
    forgot_password_window.configure(bg="#ffffff")

    label = tk.Label(forgot_password_window, text="Enter your email to reset password:", font=("Arial", 12), bg="#ffffff")
    label.pack(pady=10)

    email_entry = ttk.Entry(forgot_password_window, font=("Arial", 12), width=30)
    email_entry.pack(pady=5)

    def reset_password():
        email = email_entry.get()
        if not email.endswith('@student.newinti.edu.my'):
            messagebox.showerror("Invalid Email", "Email must end with '@student.newinti.edu.my'")
        else:
            messagebox.showinfo("Password Reset", f"Password reset instructions sent to {email}")
            forgot_password_window.destroy()

    reset_button = tk.Button(forgot_password_window, text="Reset Password", font=("Arial", 12),
                             bg="#dd6f6f", fg="white", command=reset_password, relief="flat", bd=3)
    reset_button.pack(pady=20)

# Main application window
app = tk.Tk()
app.title("INTI Carpool Login")
app.attributes('-fullscreen', True)
app.configure(bg="#f7f7f7")

# Create two-column layout
main_frame = tk.Frame(app, bg="#f7f7f7")
main_frame.pack(fill="both", expand=True)

# Left column for the logo, title, and login form
left_frame = tk.Frame(main_frame, bg="#ffffff", bd=10, relief="solid", padx=20, pady=20)
left_frame.pack(side="left", fill="both", expand=True)

# Logo
try:
    logo_image = Image.open("INTIlogo.png")  # Ensure this path is correct
    logo_image = logo_image.resize((200, 100))  # Resize to match the logo size in the image
    logo_image = ImageTk.PhotoImage(logo_image)
    logo_label = tk.Label(left_frame, image=logo_image, bg="#ffffff")
    logo_label.pack(pady=30)
except Exception as e:
    messagebox.showerror("Error", f"Failed to load image: {e}")

title_label = tk.Label(left_frame, text="INTI Student Login", font=("Arial", 20, "bold"), fg="#333333", bg="#ffffff")
title_label.pack(pady=20)

frame = ttk.Frame(left_frame)
frame.pack(pady=10)

username_label = ttk.Label(frame, text="Username:", font=("Arial", 12))
username_label.grid(row=0, column=0, padx=10, pady=5, sticky="e")
username_entry = ttk.Entry(frame, font=("Arial", 12), width=30)
username_entry.grid(row=0, column=1, padx=10, pady=5)

password_label = ttk.Label(frame, text="Password:", font=("Arial", 12))
password_label.grid(row=1, column=0, padx=10, pady=5, sticky="e")
password_entry = ttk.Entry(frame, show="*", font=("Arial", 12), width=30)
password_entry.grid(row=1, column=1, padx=10, pady=5)

login_button = tk.Button(left_frame, text="Login", command=check_login, font=("Arial", 12), bg="#dd6f6f", fg="white", relief="flat", bd=3)
login_button.pack(pady=20)

# Image hyperlink (clickable image)
try:
    hyperlink_image = tk.PhotoImage(file="small_guy.png")  # Replace with your actual image file
    image_link = tk.Label(app, image=hyperlink_image, cursor="hand2", bg="#ffffff")

    # Place the image at the bottom-right corner
    image_link.place(relx=1.0, rely=1.0, anchor='se', x=-20, y=-20)  # Use negative x, y offsets to position away from edges

    # Bind click event to open a new window
    image_link.bind("<Button-1>", lambda e: direct_login())

except Exception as e:
    messagebox.showerror("Error", f"Failed to load hyperlink image: {e}")

def direct_login():
    import admin_page
    app.destroy()  # Close the login window
    admin_page.open_admin_page()  # Open the student page

create_account_link = tk.Label(left_frame, text="Create Account", font=("Arial", 10), fg="red", cursor="hand2", bg="#ffffff")
create_account_link.pack(pady=5)
create_account_link.bind("<Button-1>", lambda e: open_create_account_window())

forgot_password_link = tk.Label(left_frame, text="Forgot Password?", font=("Arial", 10), fg="red", cursor="hand2", bg="#ffffff")
forgot_password_link.pack(pady=5)
forgot_password_link.bind("<Button-1>", lambda e: open_forgot_password_window())

# Right column for background image
right_frame = tk.Frame(main_frame, bg="#ffffff", bd=10, relief="solid", padx=20, pady=20)
right_frame.pack(side="right", fill="both", expand=True)

# Image
try:
    img = Image.open("carpool.jpg")
    img = img.resize((400, 400))  # Resize to fit the window
    img = ImageTk.PhotoImage(img)
    img_label = tk.Label(right_frame, image=img, bg="#ffffff")
    img_label.pack(pady=20)
except Exception as e:
    messagebox.showerror("Error", f"Failed to load image: {e}")

# Bind escape key to exit fullscreen
app.bind("<Escape>", exit_fullscreen)

# Start the app
app.mainloop()
