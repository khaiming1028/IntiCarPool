import tkinter as tk
from tkinter import messagebox
import student_page


def check_login():
    username = username_entry.get()
    password = password_entry.get()

    # Check if username and password fields are not empty (basic validation)
    if username and password:
        messagebox.showinfo("Login Successful", f"Welcome, {username}")
        app.destroy()  # Close the login window
        student_page.open_student_page()  # Open the carpool window
    else:
        messagebox.showerror("Login Failed", "Username and Password cannot be empty")

def exit_fullscreen(event=None):
    # Exit full-screen mode
    app.attributes('-fullscreen', False)

def open_create_account_window():
    # Create a new window for creating an account
    create_account_window = tk.Toplevel(app)
    create_account_window.title("Create Account")
    create_account_window.geometry("400x350")
    create_account_window.configure(bg="#ffffff")  # Set background to white

    # Add title label
    title_label = tk.Label(create_account_window, text="Create Account", font=("Arial", 16, "bold"), bg="#ffffff")
    title_label.pack(pady=10)

    # Frame for input fields
    frame = tk.Frame(create_account_window, bg="#ffffff")
    frame.pack(pady=10)

    # Email Label and Entry
    email_label = tk.Label(frame, text="Email:", font=("Arial", 12), bg="#ffffff")
    email_label.grid(row=0, column=0, padx=10, pady=5, sticky="e")
    email_entry = tk.Entry(frame, font=("Arial", 12), width=30)
    email_entry.grid(row=0, column=1, padx=10, pady=5)

    # Username Label and Entry
    username_label = tk.Label(frame, text="Username:", font=("Arial", 12), bg="#ffffff")
    username_label.grid(row=1, column=0, padx=10, pady=5, sticky="e")
    username_entry = tk.Entry(frame, font=("Arial", 12), width=30)
    username_entry.grid(row=1, column=1, padx=10, pady=5)

    # Password Label and Entry
    password_label = tk.Label(frame, text="Password:", font=("Arial", 12), bg="#ffffff")
    password_label.grid(row=2, column=0, padx=10, pady=5, sticky="e")
    password_entry = tk.Entry(frame, show="*", font=("Arial", 12), width=30)
    password_entry.grid(row=2, column=1, padx=10, pady=5)

    # Function to handle account creation
    def create_account():
        email = email_entry.get()
        username = username_entry.get()
        password = password_entry.get()

        # Check if the email ends with '@student.newinti.edu.my'
        if not email.endswith('@student.newinti.edu.my'):
            messagebox.showerror("Invalid Email", "Email must end with '@student.newinti.edu.my'")
            return
        
        # Check if username and password fields are not empty
        if not username or not password:
            messagebox.showerror("Input Error", "Username and Password cannot be empty")
            return

        # Account creation successful
        messagebox.showinfo("Account Created", "Your account has been successfully created.")
        create_account_window.destroy()  # Close the account creation window

    # Create Account Button
    create_account_button = tk.Button(create_account_window, text="Create Account", font=("Arial", 12),
                                      bg="green", fg="white", command=create_account)
    create_account_button.pack(pady=20)

def open_forgot_password_window():
    # Create a pop-up window for "Forgot Password"
    forgot_password_window = tk.Toplevel(app)
    forgot_password_window.title("Forgot Password")
    forgot_password_window.geometry("300x200")
    forgot_password_window.configure(bg="#ffffff")  # Set background to white

    # Add a label and entry for email input
    label = tk.Label(forgot_password_window, text="Enter your email to reset password:", font=("Arial", 12), bg="#ffffff")
    label.pack(pady=10)

    email_entry = tk.Entry(forgot_password_window, font=("Arial", 12), width=30)
    email_entry.pack(pady=5)

    # Function to handle password reset
    def reset_password():
        email = email_entry.get()
        if not email.endswith('@student.newinti.edu.my'):
            messagebox.showerror("Invalid Email", "Email must end with '@student.newinti.edu.my'")
        else:
            messagebox.showinfo("Password Reset", f"Password reset instructions sent to {email}")
            forgot_password_window.destroy()  # Close the forgot password window

    # Reset Password Button
    reset_button = tk.Button(forgot_password_window, text="Reset Password", font=("Arial", 12),
                             bg="blue", fg="white", command=reset_password)
    reset_button.pack(pady=20)


# Create the main window
app = tk.Tk()
app.title("INTI Student Login")
app.attributes('-fullscreen', True)  # Set to full-screen
app.configure(bg="#ffffff")  # Set background color to white

# Load the image (make sure 'logo.png' is in the same directory or specify the path)
try:
    logo_image = tk.PhotoImage(file="logo.png")
    logo_label = tk.Label(app, image=logo_image, bg="#ffffff")  # Match the background color
    logo_label.pack(pady=10)
except Exception as e:
    messagebox.showerror("Error", f"Failed to load image: {e}")

# Add a title label
title_label = tk.Label(app, text="INTI Student Login", font=("Arial", 16, "bold"), bg="#ffffff")
title_label.pack(pady=10)

# Frame for username and password
frame = tk.Frame(app, bg="#ffffff")
frame.pack(pady=10)

# Username Label and Entry
username_label = tk.Label(frame, text="Username:", font=("Arial", 12), bg="#ffffff")
username_label.grid(row=0, column=0, padx=10, pady=5, sticky="e")
username_entry = tk.Entry(frame, font=("Arial", 12), width=30)
username_entry.grid(row=0, column=1, padx=10, pady=5)

# Password Label and Entry
password_label = tk.Label(frame, text="Password:", font=("Arial", 12), bg="#ffffff")
password_label.grid(row=1, column=0, padx=10, pady=5, sticky="e")
password_entry = tk.Entry(frame, show="*", font=("Arial", 12), width=30)
password_entry.grid(row=1, column=1, padx=10, pady=5)

# Login Button with red background
login_button = tk.Button(app, text="Login", command=check_login, font=("Arial", 12), bg="red", fg="white", width=10)
login_button.pack(pady=10)

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
    app.destroy()  # Close the login window
    student_page.open_student_page()  # Open the student page

# "Forgot Password?" as clickable text (hyperlink)
forgot_password_link = tk.Label(app, text="Forgot Password?", font=("Arial", 10), fg="blue", cursor="hand2", bg="#ffffff")
forgot_password_link.pack(pady=5)
forgot_password_link.bind("<Button-1>", lambda e: open_forgot_password_window())

# Create Account as clickable text (hyperlink)
create_account_link = tk.Label(app, text="Create Account", font=("Arial", 10), fg="blue", cursor="hand2", bg="#ffffff")
create_account_link.pack(pady=5)
create_account_link.bind("<Button-1>", lambda e: open_create_account_window())

# Bind the escape key to exit full-screen mode
app.bind("<Escape>", exit_fullscreen)

# Run the application
app.mainloop()
