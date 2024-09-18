import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector

# Connect to MySQL
conn = mysql.connector.connect(
    host="localhost",
    user="root",      # Replace with your MySQL username
    password="1111",  # Replace with your MySQL password
    database="bus_booking"  # Your database name
)
cursor = conn.cursor()

# Classes for Bus and Booking
class Bus:
    def __init__(self, id, ac, capacity):
        self.id = id
        self.ac = ac
        self.capacity = capacity

class Booking:
    bookingid = 0
    
    def __init__(self, bus_id, date, regno):
        self.bus_id = bus_id
        self.date = date
        self.regno = regno

    def available(self):
        cursor.execute(f"SELECT capacity FROM buses WHERE id = {self.bus_id}")
        capacity = cursor.fetchone()[0]
        
        cursor.execute(f"SELECT COUNT(*) FROM bookings WHERE busid = {self.bus_id} AND date = '{self.date}'")
        booked_count = cursor.fetchone()[0]
        
        if booked_count < capacity:
            # Insert booking in MySQL database
            cursor.execute(f"INSERT INTO bookings (busid, date, regno) VALUES ({self.bus_id}, '{self.date}', {self.regno})")
            conn.commit()
            Booking.bookingid += 1
            messagebox.showinfo("Booking", "Booked successfully!")
            self.show_booking_details()
        else:
            messagebox.showwarning("Booking", "Bus is full! You are added to the waiting list.")
            self.add_to_waiting_list()
    
    def show_booking_details(self):
        booking_details_window = tk.Toplevel(window)
        booking_details_window.title("Booking Details")
        booking_details_window.configure(bg="#f0f0f0")
        
        details_label = tk.Label(booking_details_window, text=f"Bus ID: {self.bus_id}, Date: {self.date}, RegNo: {self.regno}",
                                 bg="#f0f0f0", fg="#333", font=("Helvetica", 12))
        details_label.pack(padx=20, pady=20)
    
    def add_to_waiting_list(self):
        cursor.execute(f"INSERT INTO waiting_list (busid, date, regno) VALUES ({self.bus_id}, '{self.date}', {self.regno})")
        conn.commit()

    def cancel(self):
        cursor.execute(f"DELETE FROM bookings WHERE busid = {self.bus_id} AND date = '{self.date}' AND regno = {self.regno}")
        conn.commit()
        messagebox.showinfo("Cancelation", "Booking canceled!")

# Tkinter GUI
def show_bus_details():
    cursor.execute("SELECT * FROM buses")
    buses = cursor.fetchall()

    bus_details_window = tk.Toplevel(window)
    bus_details_window.title("Bus Details")
    bus_details_window.configure(bg="#f0f0f0")

    for bus in buses:
        bus_label = tk.Label(bus_details_window, text=f"Bus ID: {bus[0]}, AC: {bus[1]}, Capacity: {bus[2]}",
                             bg="#f0f0f0", fg="#333", font=("Helvetica", 12))
        bus_label.pack(pady=5)

def book_bus():
    bus_id = int(bus_id_entry.get())
    date = booking_date_entry.get()
    regno = Booking.bookingid

    booking = Booking(bus_id, date, regno)
    booking.available()

def cancel_booking():
    bus_id = int(bus_id_entry.get())
    date = booking_date_entry.get()
    regno = int(regno_entry.get())

    booking = Booking(bus_id, date, regno)
    booking.cancel()

def display_bookings():
    cursor.execute("SELECT * FROM bookings")
    bookings = cursor.fetchall()
    display_window = tk.Toplevel(window)
    display_window.title("Booked History")
    display_window.configure(bg="#f0f0f0")
    
    for booking in bookings:
        booking_label = tk.Label(display_window, text=f"Bus ID: {booking[1]}, Date: {booking[2]}, RegNo: {booking[3]}",
                                bg="#f0f0f0", fg="#333", font=("Helvetica", 12))
        booking_label.pack(pady=5)

def display_waiting_list():
    cursor.execute("SELECT * FROM waiting_list")
    waiting_list = cursor.fetchall()
    waiting_list_window = tk.Toplevel(window)
    waiting_list_window.title("Waiting List")
    waiting_list_window.configure(bg="#f0f0f0")
    
    for waiting in waiting_list:
        waiting_label = tk.Label(waiting_list_window, text=f"Bus ID: {waiting[1]}, Date: {waiting[2]}, RegNo: {waiting[3]}",
                                bg="#f0f0f0", fg="#333", font=("Helvetica", 12))
        waiting_label.pack(pady=5)

# Create the main window
window = tk.Tk()
window.title("Bus Booking System")
window.geometry("400x300")
window.configure(bg="#e0e0e0")  # Light gray background

# Create the booking frame
frame = tk.LabelFrame(window, text="Bus Booking", font=("Helvetica", 14, "bold"), bg="#c0c0c0", fg="#000", padx=20, pady=20)
frame.pack(padx=20, pady=20)

# Bus ID Entry
bus_id_label = tk.Label(frame, text="Bus ID:", font=("Helvetica", 12), bg="#c0c0c0", fg="#000")
bus_id_label.grid(row=0, column=0, pady=5)
bus_id_entry = tk.Entry(frame, font=("Helvetica", 12))
bus_id_entry.grid(row=0, column=1, pady=5)

# Booking Date Entry
booking_date_label = tk.Label(frame, text="Date (YYYY-MM-DD):", font=("Helvetica", 12), bg="#c0c0c0", fg="#000")
booking_date_label.grid(row=1, column=0, pady=5)
booking_date_entry = tk.Entry(frame, font=("Helvetica", 12))
booking_date_entry.grid(row=1, column=1, pady=5)

# Registration No Entry (for canceling bookings)
regno_label = tk.Label(frame, text="RegNo (for Cancel):", font=("Helvetica", 12), bg="#c0c0c0", fg="#000")
regno_label.grid(row=2, column=0, pady=5)
regno_entry = tk.Entry(frame, font=("Helvetica", 12))
regno_entry.grid(row=2, column=1, pady=5)

# Buttons for booking, canceling, and displaying bookings
book_button = tk.Button(frame, text="Book", command=book_bus, bg="#4CAF50", fg="white", font=("Helvetica", 12, "bold"), relief="raised")
book_button.grid(row=3, column=0, pady=10)

cancel_button = tk.Button(frame, text="Cancel", command=cancel_booking, bg="#f44336", fg="white", font=("Helvetica", 12, "bold"), relief="raised")
cancel_button.grid(row=3, column=1, pady=10)

display_button = tk.Button(frame, text="Display Bookings", command=display_bookings, bg="#2196F3", fg="white", font=("Helvetica", 12, "bold"), relief="raised")
display_button.grid(row=4, column=0, pady=10)

waiting_list_button = tk.Button(frame, text="Display Waiting List", command=display_waiting_list, bg="#FF9800", fg="white", font=("Helvetica", 12, "bold"), relief="raised")
waiting_list_button.grid(row=4, column=1, pady=10)

bus_details_button = tk.Button(frame, text="Show Bus Details", command=show_bus_details, bg="#9C27B0", fg="white", font=("Helvetica", 12, "bold"), relief="raised")
bus_details_button.grid(row=5, column=0, columnspan=2, pady=10)

# Run the application
window.mainloop()

# Close MySQL connection when the program exits
conn.close()
