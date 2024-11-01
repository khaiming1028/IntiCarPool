import tkinter as tk
from tkinter import ttk

def open_carpool_window():
    # Create the main window for carpool information
    carpool_window = tk.Tk()
    carpool_window.title("Carpool Information")
    carpool_window.geometry("600x500")
    carpool_window.configure(bg="#f0f0f0")

    style = ttk.Style()
    style.theme_use("clam")
    style.configure("TLabel", background="#f0f0f0", font=("Helvetica", 12))
    style.configure("TEntry", font=("Helvetica", 12))
    style.configure("TButton", font=("Helvetica", 12), padding=6)
    style.configure("TCombobox", font=("Helvetica", 12))

    # Navigation Bar
    nav_frame = tk.Frame(carpool_window, bg="#808080")
    nav_frame.grid(column=0, row=0, columnspan=2, pady=10, sticky="ew")

    home_button = tk.Button(nav_frame, text="Home", bg="#a0a0a0", fg="white", font=("Helvetica", 12, "bold"), bd=0, padx=10, pady=5, activebackground="#808080", activeforeground="white")
    home_button.pack(side="left", padx=5)

    profile_button = tk.Button(nav_frame, text="Profile", bg="#a0a0a0", fg="white", font=("Helvetica", 12, "bold"), bd=0, padx=10, pady=5, activebackground="#808080", activeforeground="white")
    profile_button.pack(side="left", padx=5)

    settings_button = tk.Button(nav_frame, text="Settings", bg="#a0a0a0", fg="white", font=("Helvetica", 12, "bold"), bd=0, padx=10, pady=5, activebackground="#808080", activeforeground="white")
    settings_button.pack(side="left", padx=5)

    # Carpool Name
    carpool_name_label = ttk.Label(carpool_window, text="Carpool Name:")
    carpool_name_label.grid(column=0, row=1, padx=10, pady=10, sticky=tk.W)
    carpool_name = tk.StringVar()
    carpool_name_entry = ttk.Entry(carpool_window, textvariable=carpool_name)
    carpool_name_entry.grid(column=1, row=1, padx=10, pady=10)

    # Car Type
    car_type_label = ttk.Label(carpool_window, text="Car Type:")
    car_type_label.grid(column=0, row=2, padx=10, pady=10, sticky=tk.W)
    car_type = tk.StringVar()
    car_type_combobox = ttk.Combobox(carpool_window, textvariable=car_type)
    car_type_combobox['values'] = ("Sedan", "MPV", "SUV", "Hatchback", "Coupe")
    car_type_combobox.grid(column=1, row=2, padx=10, pady=10)
    car_type_combobox.current(0)
    car_type.trace("w", lambda *args: update_person_limit(car_type_combobox, person_limit_combobox))

    # Person Limit
    person_limit_label = ttk.Label(carpool_window, text="Person Limit:")
    person_limit_label.grid(column=0, row=3, padx=10, pady=10, sticky=tk.W)
    person_limit = tk.StringVar()
    person_limit_combobox = ttk.Combobox(carpool_window, textvariable=person_limit)
    person_limit_combobox.grid(column=1, row=3, padx=10, pady=10)
    update_person_limit(car_type_combobox, person_limit_combobox)

    # Starting Point
    starting_point_label = ttk.Label(carpool_window, text="Starting Point:")
    starting_point_label.grid(column=0, row=4, padx=10, pady=10, sticky=tk.W)
    starting_point = tk.StringVar()
    starting_point_entry = ttk.Entry(carpool_window, textvariable=starting_point)
    starting_point_entry.grid(column=1, row=4, padx=10, pady=10)

    # Pickup Time
    starting_time_label = ttk.Label(carpool_window, text="Starting Time:")
    starting_time_label.grid(column=0, row=5, padx=10, pady=10, sticky=tk.W)
    starting_time = tk.StringVar()
    starting_time_entry = ttk.Entry(carpool_window, textvariable=starting_time)
    starting_time_entry.grid(column=1, row=5, padx=10, pady=10)

    # Dropoff Time
    ending_time_label = ttk.Label(carpool_window, text="Ending Time:")
    ending_time_label.grid(column=0, row=6, padx=10, pady=10, sticky=tk.W)
    ending_time = tk.StringVar()
    ending_time_entry = ttk.Entry(carpool_window, textvariable=ending_time)
    ending_time_entry.grid(column=1, row=6, padx=10, pady=10)

    # Submit Button
    submit_button = ttk.Button(carpool_window, text="Submit", command=lambda: submit(carpool_name, car_type, person_limit, starting_point, starting_time, ending_time))
    submit_button.grid(column=1, row=7, padx=10, pady=20)


def update_person_limit(car_type_combobox, person_limit_combobox):
    car = car_type_combobox.get()
    if car == "Sedan":
        person_limit_combobox["values"] = tuple(range(1, 5))
    elif car == "MPV":
        person_limit_combobox["values"] = tuple(range(1, 11))
    elif car == "Coupe":
        person_limit_combobox["values"] = (1,)
    else:
        person_limit_combobox["values"] = tuple(range(1, 8))
    person_limit_combobox.current(0)

def submit(carpool_name, car_type, person_limit, starting_point, starting_time, ending_time):
    print("Carpool Name:", carpool_name.get())
    print("Car Type:", car_type.get())
    print("Person Limit:", person_limit.get())
    print("Starting Point:", starting_point.get())
    print("Pickup Time:", starting_time.get())
    print("Dropoff Time:", ending_time.get())
