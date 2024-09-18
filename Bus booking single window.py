import tkinter as tk
from tkinter import ttk, messagebox

class Bus:
    def __init__(self, id, ac, capacity):
        self.id = id
        self.ac = ac
        self.capacity = capacity

    def display(self):
        return f"ID: {self.id}, AC: {self.ac}, Capacity: {self.capacity}"

class Booking:
    bookingid = 0

    def __init__(self, id, date, regno):
        self.id = id
        self.date = date
        self.regno = regno

    def available(self):
        cap = 0
        for bus in buses:
            if bus.id == self.id:
                cap = bus.capacity

        count = sum(1 for b in bookedhistory if b.id == self.id and b.date == self.date)

        if count < cap:
            bookedhistory.append(self)
            Booking.bookingid += 1
            return "Booking successful!"
        elif len(waiting) < 3:
            waiting.append(self)
            Booking.bookingid += 1
            return "Added to waiting list!"
        else:
            return "No availability. Try another bus or date."

    def cancel(self):
        for i in bookedhistory:
            if i.id == self.id and i.date == self.date and i.regno == self.regno:
                bookedhistory.remove(i)
                if len(waiting) > 0:
                    bookedhistory.append(waiting[0])
                    waiting.pop(0)
                return "Booking canceled!"
        return "No booking found to cancel."

    def display(self):
        return f"Bus ID: {self.id}, Date: {self.date}, Booking ID: {self.regno}"

# Data
buses = [Bus(1, True, 3), Bus(2, True, 4), Bus(3, True, 2)]
bookedhistory = []
waiting = []

# Tkinter GUI
def book_ticket():
    try:
        bus_id = int(bus_id_entry.get())
        date = date_entry.get()

        if not date:
            raise ValueError("Please enter a date!")

        book = Booking(bus_id, date, Booking.bookingid)
        status = book.available()
        messagebox.showinfo("Booking Status", status)
        update_display()

    except ValueError as e:
        messagebox.showerror("Input Error", str(e))

def cancel_ticket():
    try:
        bus_id = int(bus_id_entry.get())
        date = date_entry.get()
        regno = int(booking_id_entry.get())

        book = Booking(bus_id, date, regno)
        status = book.cancel()
        messagebox.showinfo("Cancellation Status", status)
        update_display()

    except ValueError:
        messagebox.showerror("Input Error", "Invalid input. Please check the values.")

def update_display():
    # Clear display area
    booked_text.delete(1.0, tk.END)
    waiting_text.delete(1.0, tk.END)

    # Display booked history
    booked_text.insert(tk.END, "Booked History:\n")
    for b in bookedhistory:
        booked_text.insert(tk.END, b.display() + "\n")

    # Display waiting list
    waiting_text.insert(tk.END, "Waiting List:\n")
    for w in waiting:
        waiting_text.insert(tk.END, w.display() + "\n")

# Main application window
root = tk.Tk()
root.title("Bus Booking System")

# Frame for booking details
frame = tk.Frame(root)
frame.pack(padx=10, pady=10)

bus_id_label = tk.Label(frame, text="Bus ID:")
bus_id_label.grid(row=0, column=0, padx=5, pady=5)

bus_id_entry = tk.Entry(frame)
bus_id_entry.grid(row=0, column=1, padx=5, pady=5)

date_label = tk.Label(frame, text="Date:")
date_label.grid(row=1, column=0, padx=5, pady=5)

date_entry = tk.Entry(frame)
date_entry.grid(row=1, column=1, padx=5, pady=5)

booking_id_label = tk.Label(frame, text="Booking ID (for cancellation):")
booking_id_label.grid(row=2, column=0, padx=5, pady=5)

booking_id_entry = tk.Entry(frame)
booking_id_entry.grid(row=2, column=1, padx=5, pady=5)

# Buttons
book_button = tk.Button(frame, text="Book Ticket", command=book_ticket)
book_button.grid(row=3, column=0, padx=5, pady=5)

cancel_button = tk.Button(frame, text="Cancel Ticket", command=cancel_ticket)
cancel_button.grid(row=3, column=1, padx=5, pady=5)

# Display area for booked history and waiting list
display_frame = tk.Frame(root)
display_frame.pack(padx=10, pady=10)

booked_label = tk.Label(display_frame, text="Booked History:")
booked_label.grid(row=0, column=0, padx=5, pady=5)

booked_text = tk.Text(display_frame, height=10, width=40)
booked_text.grid(row=1, column=0, padx=5, pady=5)

waiting_label = tk.Label(display_frame, text="Waiting List:")
waiting_label.grid(row=0, column=1, padx=5, pady=5)

waiting_text = tk.Text(display_frame, height=10, width=40)
waiting_text.grid(row=1, column=1, padx=5, pady=5)

# Initialize display
update_display()

root.mainloop()


