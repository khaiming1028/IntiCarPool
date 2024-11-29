import tkinter as tk
from tkinter import ttk

def join_carpool_form(parent_frame):
    # Treeview/Table for carpool details
    columns = (
        "Name", "Contact Number", "Car Details","Pickup Date & Time", "Departure Time", "Pickup Point","Status", "Action"
    )
    carpool_table = ttk.Treeview(parent_frame, columns=columns, show="headings", height=10)
    carpool_table.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
    # Define column headings with bold styling and set background color for the title row
    style = ttk.Style()
    
    # Update style to force header background color to #666666 and text color to white
    style.configure("Treeview.Heading",font=("Arial", 10, "bold"),background="#666666",foreground="white")
    
    # Use a different theme to avoid OS default style interfering (if needed)
    style.theme_use('clam')

    for col in columns:
        carpool_table.heading(col, text=col)
        carpool_table.column(col, anchor="center", stretch=True)

    # Example data
    data = [
        ["Tan Mei Ling", "016-8762536", "PPP1234 SAGA (Sedan)",
         "20/11/24 11.00AM", "12.00PM", "Jelutong", "Pending"],
        ["Lim Yong Xiang", "012-7834912", "PAA8643 MYVI (Sedan)",
         "21/11/24 10.00AM", "10.30AM", "Sungai Dua", "3/4"],
        ["Razak bin Osman", "012-9172634", "PBB8125 SERENA (MPV)",
         "4/11/24 1.00PM", "1.30PM", "Gelugor", "Completed"]
    ]

    # Add data and dynamically insert buttons
    action_buttons = []  # To store buttons for proper management
    for i, row in enumerate(data):
        # Insert row data (except for Action column)
        row_id = carpool_table.insert("", "end", iid=i, values=row[:-1])

        # Create Action Button dynamically
        status = row[-1]

        if status == "3/4":  # Add Leave button for 3/4 status
            btn = tk.Button(
                parent_frame,text="Leave",font=("Arial", 10),bg="#E21A22",fg="white",command=lambda r=row: leave_action(r),width=8)
            action_buttons.append((i, btn))

        elif status == "Completed":  # Add Rate button for Completed status
            btn = tk.Button(parent_frame,text="Rate",font=("Arial", 10),bg="#0056D2",fg="white",command=lambda r=row: rate_action(r),width=8)
            action_buttons.append((i, btn))

    # Place Action buttons in the correct positions
    def update_button_positions():
        for i, btn in action_buttons:
            bbox = carpool_table.bbox(i, column=len(columns) - 1)  # Get Action column's bbox
            if bbox:
                x, y, width, height = bbox
                btn.place(x=x + carpool_table.winfo_x(), y=y + carpool_table.winfo_y(), width=width, height=height)

    # Update button positions on resize or scroll
    carpool_table.bind("<Configure>", lambda event: update_button_positions())
    carpool_table.bind("<Motion>", lambda event: update_button_positions())

    # Define button actions
    def leave_action(row):
        print(f"Leave button clicked for: {row[0]} ({row[2]})")

    def rate_action(row):
        print(f"Rate button clicked for: {row[0]} ({row[2]})")

# Example for creating a standalone window
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Join Carpool")
    root.geometry("1000x600")
    root.configure(bg="#ffffff")

    # Create a frame for the carpool page
    carpool_frame = tk.Frame(root, bg="#ffffff")
    carpool_frame.pack(fill="both", expand=True)

    join_carpool_form(carpool_frame)

    root.mainloop()
