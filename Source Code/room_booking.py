import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import json
import os

class BookingManager:
    """Handles booking data and file operations."""
    def __init__(self, bookings_file="bookings.json"):
        self.bookings_file = bookings_file
        self.bookings = self.load_bookings()

    def load_bookings(self):
        if os.path.exists(self.bookings_file):
            try:
                with open(self.bookings_file, 'r') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                messagebox.showwarning("Data Load Error", "Could not load booking data. File might be corrupted. Starting with empty bookings.")
                return []
        return []

    def save_bookings(self):
        try:
            with open(self.bookings_file, 'w') as f:
                json.dump(self.bookings, f, indent=4)
        except IOError:
            messagebox.showerror("Data Save Error", "Could not save booking data to file.")

class DiscussionRoomBookingApp(BookingManager):
    def __init__(self, master):
        super().__init__()  # BookingManager init
        self.master = master
        master.title("Discussion Room Booking System")
        master.geometry("800x700")

        self.venues = ["Library Discussion Room", "Cyber Centre Meeting Room"]
        self.time_slots = [
            "09:00 - 10:00", "10:00 - 11:00", "11:00 - 12:00",
            "12:00 - 13:00", "13:00 - 14:00", "14:00 - 15:00",
            "15:00 - 16:00", "16:00 - 17:00"
        ]

        self.editing_booking_idx = -1
        self.availability_chart_window = None

        style = ttk.Style()
        style.configure("TFrame", background="#f0f0f0")
        style.configure("TLabel", background="#f0f0f0", font=("Arial", 10))
        style.configure("TButton", font=("Arial", 10, "bold"), padding=5)
        style.configure("TCombobox", font=("Arial", 10))
        style.configure("TEntry", font=("Arial", 10))
        style.configure("Treeview.Heading", font=("Arial", 10, "bold"))
        style.configure("Treeview", font=("Arial", 10), rowheight=25)
        style.configure("Green.TLabel", background="#a8e6cf", foreground="black", font=("Arial", 9, "bold"))
        style.configure("Red.TLabel", background="#ffadad", foreground="black", font=("Arial", 9, "bold"))
        style.configure("Gray.TLabel", background="#d0d0d0", foreground="black", font=("Arial", 9))

        self.main_frame = ttk.Frame(master, padding="20", style="TFrame")
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        self.form_frame = ttk.LabelFrame(self.main_frame, text="Book a Room", padding="15")
        self.form_frame.pack(pady=10, padx=10, fill=tk.X)

        ttk.Label(self.form_frame, text="Select Venue:").grid(row=0, column=0, sticky="w", pady=5, padx=5)
        self.venue_combobox = ttk.Combobox(self.form_frame, values=self.venues, state="readonly")
        self.venue_combobox.set(self.venues[0])
        self.venue_combobox.grid(row=0, column=1, sticky="ew", pady=5, padx=5)

        ttk.Label(self.form_frame, text="Select Date (YYYY-MM-DD):").grid(row=1, column=0, sticky="w", pady=5, padx=5)
        self.date_entry = ttk.Entry(self.form_frame)
        self.date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
        self.date_entry.grid(row=1, column=1, sticky="ew", pady=5, padx=5)

        ttk.Label(self.form_frame, text="Select Time Slot:").grid(row=2, column=0, sticky="w", pady=5, padx=5)
        self.time_combobox = ttk.Combobox(self.form_frame, values=self.time_slots, state="readonly")
        self.time_combobox.set(self.time_slots[0])
        self.time_combobox.grid(row=2, column=1, sticky="ew", pady=5, padx=5)

        ttk.Label(self.form_frame, text="Your Name:").grid(row=3, column=0, sticky="w", pady=5, padx=5)
        self.name_entry = ttk.Entry(self.form_frame)
        self.name_entry.grid(row=3, column=1, sticky="ew", pady=5, padx=5)

        self.book_button = ttk.Button(self.form_frame, text="Book Room", command=self.book_room)
        self.book_button.grid(row=4, column=0, columnspan=2, pady=15)
        self.form_frame.grid_columnconfigure(1, weight=1)

        self.bookings_frame = ttk.LabelFrame(self.main_frame, text="Current Bookings", padding="15")
        self.bookings_frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

        columns = ("Venue", "Date", "Time", "Booked By", "Booked On")
        self.bookings_tree = ttk.Treeview(self.bookings_frame, columns=columns, show="headings")
        self.bookings_tree.pack(side="left", fill="both", expand=True)

        self.bookings_tree.heading("Venue", text="Venue", anchor=tk.W)
        self.bookings_tree.heading("Date", text="Date", anchor=tk.CENTER)
        self.bookings_tree.heading("Time", text="Time Slot", anchor=tk.CENTER)
        self.bookings_tree.heading("Booked By", text="Booked By", anchor=tk.W)
        self.bookings_tree.heading("Booked On", text="Booked On", anchor=tk.CENTER)

        self.bookings_tree.column("Venue", width=150, stretch=tk.YES)
        self.bookings_tree.column("Date", width=90, stretch=tk.NO, anchor=tk.CENTER)
        self.bookings_tree.column("Time", width=100, stretch=tk.NO, anchor=tk.CENTER)
        self.bookings_tree.column("Booked By", width=120, stretch=tk.YES)
        self.bookings_tree.column("Booked On", width=130, stretch=tk.NO, anchor=tk.CENTER)

        tree_scrollbar = ttk.Scrollbar(self.bookings_frame, orient="vertical", command=self.bookings_tree.yview)
        tree_scrollbar.pack(side="right", fill="y")
        self.bookings_tree.configure(yscrollcommand=tree_scrollbar.set)

        self.action_buttons_frame = ttk.Frame(self.main_frame, style="TFrame")
        self.action_buttons_frame.pack(pady=10, padx=10, fill=tk.X)

        self.edit_button = ttk.Button(self.action_buttons_frame, text="Edit Booking", command=self.edit_booking_setup, state="disabled")
        self.edit_button.pack(side=tk.LEFT, padx=5, expand=True)

        self.cancel_button = ttk.Button(self.action_buttons_frame, text="Cancel Booking", command=self.cancel_booking, state="disabled")
        self.cancel_button.pack(side=tk.LEFT, padx=5, expand=True)

        self.bookings_tree.bind("<<TreeviewSelect>>", self.on_tree_select)

        self.chart_button_frame = ttk.Frame(self.main_frame, style="TFrame")
        self.chart_button_frame.pack(pady=10, padx=10, fill=tk.X)
        self.show_chart_button = ttk.Button(self.chart_button_frame, text="Show Availability Chart", command=self.create_availability_chart_window)
        self.show_chart_button.pack(pady=5)

        master.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.update_bookings_display()

    def on_closing(self):
        self.save_bookings()
        self.master.destroy()

    def on_tree_select(self, event):
        selected_item = self.bookings_tree.selection()
        if selected_item:
            self.edit_button.config(state="normal")
            self.cancel_button.config(state="normal")
        else:
            self.edit_button.config(state="disabled")
            self.cancel_button.config(state="disabled")

    def validate_booking_inputs(self, venue, date_str, time_slot, name):
        if not venue or not date_str or not time_slot or not name:
            messagebox.showwarning("Input Error", "All fields must be filled.")
            return False

        try:
            booking_date = datetime.strptime(date_str, "%Y-%m-%d").date()
            if booking_date < datetime.now().date():
                messagebox.showwarning("Invalid Date", "Booking date cannot be in the past.")
                return False
        except ValueError:
            messagebox.showwarning("Invalid Date", "Please enter date in YYYY-MM-DD format.")
            return False
        return True

    def book_room(self):
        venue = self.venue_combobox.get()
        date_str = self.date_entry.get()
        time_slot = self.time_combobox.get()
        name = self.name_entry.get().strip()

        if not self.validate_booking_inputs(venue, date_str, time_slot, name):
            return

        for booking in self.bookings:
            if (booking["venue"] == venue and
                booking["date"] == date_str and
                booking["time_slot"] == time_slot):
                messagebox.showerror("Booking Conflict", f"The room {venue} is already booked for {date_str} at {time_slot}.")
                return

        new_booking = {
            "venue": venue,
            "date": date_str,
            "time_slot": time_slot,
            "name": name,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        self.bookings.append(new_booking)
        self.save_bookings()
        self.update_bookings_display()
        self.update_chart_if_open()
        messagebox.showinfo("Booking Confirmed", "Your room has been successfully booked!")
        self.name_entry.delete(0, tk.END)

    def edit_booking_setup(self):
        selected_item = self.bookings_tree.selection()
        if not selected_item:
            messagebox.showwarning("No Selection", "Please select a booking to edit.")
            return

        item_id = selected_item[0]
        self.editing_booking_idx = int(item_id)
        booking_to_edit = self.bookings[self.editing_booking_idx]

        self.venue_combobox.set(booking_to_edit["venue"])
        self.date_entry.delete(0, tk.END)
        self.date_entry.insert(0, booking_to_edit["date"])
        self.time_combobox.set(booking_to_edit["time_slot"])
        self.name_entry.delete(0, tk.END)
        self.name_entry.insert(0, booking_to_edit["name"])

        self.book_button.config(text="Save Changes", command=self.save_edited_booking)
        self.form_frame.config(text=f"Edit Booking (ID: {self.editing_booking_idx + 1})")
        messagebox.showinfo("Edit Mode", "Form loaded with selected booking. Make changes and click 'Save Changes'.")

    def save_edited_booking(self):
        if self.editing_booking_idx == -1:
            messagebox.showerror("Error", "No booking selected for editing. Please select one first.")
            return

        venue = self.venue_combobox.get()
        date_str = self.date_entry.get()
        time_slot = self.time_combobox.get()
        name = self.name_entry.get().strip()

        if not self.validate_booking_inputs(venue, date_str, time_slot, name):
            return

        for i, booking in enumerate(self.bookings):
            if i != self.editing_booking_idx:
                if (booking["venue"] == venue and
                    booking["date"] == date_str and
                    booking["time_slot"] == time_slot):
                    messagebox.showerror("Booking Conflict", f"The room {venue} is already booked for {date_str} at {time_slot} by another booking.")
                    return

        self.bookings[self.editing_booking_idx].update({
            "venue": venue,
            "date": date_str,
            "time_slot": time_slot,
            "name": name,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })

        self.save_bookings()
        self.update_bookings_display()
        self.update_chart_if_open()
        messagebox.showinfo("Edit Confirmed", "Booking successfully updated!")
        self.reset_form()

    def cancel_booking(self):
        selected_item = self.bookings_tree.selection()
        if not selected_item:
            messagebox.showwarning("No Selection", "Please select a booking to cancel.")
            return

        item_id = selected_item[0]
        booking_idx = int(item_id)

        confirm = messagebox.askyesno(
            "Confirm Cancellation",
            f"Are you sure you want to cancel the booking for:\n"
            f"Venue: {self.bookings[booking_idx]['venue']}\n"
            f"Date: {self.bookings[booking_idx]['date']}\n"
            f"Time: {self.bookings[booking_idx]['time_slot']}\n"
            f"By: {self.bookings[booking_idx]['name']}?"
        )

        if confirm:
            del self.bookings[booking_idx]
            self.save_bookings()
            self.update_bookings_display()
            self.update_chart_if_open()
            messagebox.showinfo("Cancellation Confirmed", "Booking successfully cancelled.")
            self.reset_form()

    def reset_form(self):
        self.venue_combobox.set(self.venues[0])
        self.date_entry.delete(0, tk.END)
        self.date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
        self.time_combobox.set(self.time_slots[0])
        self.name_entry.delete(0, tk.END)
        self.book_button.config(text="Book Room", command=self.book_room)
        self.form_frame.config(text="Book a Room")
        self.editing_booking_idx = -1
        self.edit_button.config(state="disabled")
        self.cancel_button.config(state="disabled")
        self.bookings_tree.selection_remove(self.bookings_tree.selection())

    def update_bookings_display(self):
        for i in self.bookings_tree.get_children():
            self.bookings_tree.delete(i)

        if not self.bookings:
            pass
        else:
            for i, booking in enumerate(self.bookings):
                self.bookings_tree.insert("", "end", iid=str(i), values=(
                    booking["venue"],
                    booking["date"],
                    booking["time_slot"],
                    booking["name"],
                    booking["timestamp"]
                ))
        self.reset_form()

    def update_chart_if_open(self):
        if self.availability_chart_window and self.availability_chart_window.winfo_exists():
            self.update_availability_chart_display(
                self.chart_display_frame, self.chart_date_entry.get()
            )

    def create_availability_chart_window(self):
        if self.availability_chart_window and self.availability_chart_window.winfo_exists():
            self.availability_chart_window.lift()
            return

        self.availability_chart_window = tk.Toplevel(self.master)
        self.availability_chart_window.title("Room Availability Chart")
        self.availability_chart_window.geometry("800x400")
        self.availability_chart_window.transient(self.master)
        self.availability_chart_window.grab_set()

        chart_controls_frame = ttk.Frame(self.availability_chart_window, padding="10")
        chart_controls_frame.pack(pady=5, fill=tk.X)

        ttk.Label(chart_controls_frame, text="Select Date for Chart (YYYY-MM-DD):").pack(side=tk.LEFT, padx=5)
        self.chart_date_entry = ttk.Entry(chart_controls_frame, width=15)
        self.chart_date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
        self.chart_date_entry.pack(side=tk.LEFT, padx=5)

        chart_update_button = ttk.Button(chart_controls_frame, text="Show Chart",
                                        command=lambda: self.update_availability_chart_display(
                                            self.chart_display_frame, self.chart_date_entry.get()
                                        ))
        chart_update_button.pack(side=tk.LEFT, padx=5)

        self.chart_display_frame = ttk.Frame(self.availability_chart_window, padding="10", relief="groove", borderwidth=2)
        self.chart_display_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.update_availability_chart_display(self.chart_display_frame, datetime.now().strftime("%Y-%m-%d"))

        self.availability_chart_window.protocol("WM_DELETE_WINDOW", self.on_chart_window_close)

    def on_chart_window_close(self):
        if self.availability_chart_window:
            self.availability_chart_window.grab_release()
            self.availability_chart_window.destroy()
            self.availability_chart_window = None

    def update_availability_chart_display(self, chart_frame, selected_date_str):
        for widget in chart_frame.winfo_children():
            widget.destroy()

        try:
            selected_date = datetime.strptime(selected_date_str, "%Y-%m-%d").date()
        except ValueError:
            messagebox.showwarning("Invalid Date", "Please enter a valid date in YYYY-MM-DD format for the chart.")
            return

        ttk.Label(chart_frame, text="", style="Gray.TLabel", relief="solid", borderwidth=1).grid(row=0, column=0, sticky="nsew", padx=1, pady=1)
        for col_idx, time_slot in enumerate(self.time_slots):
            ttk.Label(chart_frame, text=time_slot, style="Gray.TLabel", relief="solid", borderwidth=1).grid(row=0, column=col_idx + 1, sticky="nsew", padx=1, pady=1)
            chart_frame.grid_columnconfigure(col_idx + 1, weight=1)

        for row_idx, venue in enumerate(self.venues):
            ttk.Label(chart_frame, text=venue, style="Gray.TLabel", relief="solid", borderwidth=1).grid(row=row_idx + 1, column=0, sticky="nsew", padx=1, pady=1)
            chart_frame.grid_rowconfigure(row_idx + 1, weight=1)

            for col_idx, time_slot in enumerate(self.time_slots):
                is_booked = False
                booked_by = ""
                for booking in self.bookings:
                    if (booking["venue"] == venue and
                        booking["date"] == selected_date_str and
                        booking["time_slot"] == time_slot):
                        is_booked = True
                        booked_by = booking["name"]
                        break

                display_text = "Booked" if is_booked else "Available"
                tooltip_text = f"Venue: {venue}\nDate: {selected_date_str}\nTime: {time_slot}\n"
                if is_booked:
                    tooltip_text += f"Booked by: {booked_by}"
                    bg_color =  "#ffadad"
                else:
                    bg_color = "#a8e6cf"

                availability_label = ttk.Label(chart_frame, text=display_text, background=bg_color,
                                               relief="solid", borderwidth=1)
                availability_label.grid(row=row_idx + 1, column=col_idx + 1, sticky="nsew", padx=1, pady=1)
                self.create_tooltip(availability_label, tooltip_text)

    def create_tooltip(self, widget, text):
        tooltip_window = None
        id = None

        def show_tooltip(event):
            nonlocal tooltip_window, id
            x, y, cx, cy = widget.bbox("insert")
            x = x + widget.winfo_rootx() + 25
            y = y + widget.winfo_rooty() + 20

            tooltip_window = tk.Toplevel(widget)
            tooltip_window.wm_overrideredirect(True)
            tooltip_window.wm_geometry(f"+{x}+{y}")

            label = tk.Label(tooltip_window, text=text, background="#ffffe0", relief="solid",
                             borderwidth=1, wraplength=200, justify=tk.LEFT)
            label.pack(ipadx=1)
            id = widget.after(500, lambda: None)

        def hide_tooltip(event):
            nonlocal tooltip_window, id
            if tooltip_window:
                tooltip_window.destroy()
                tooltip_window = None
            if id:
                widget.after_cancel(id)
                id = None

        widget.bind("<Enter>", show_tooltip)
        widget.bind("<Leave>", hide_tooltip)

def run_booking_app():
    root = tk.Tk()
    app = DiscussionRoomBookingApp(root)
    root.mainloop()

if __name__ == "__main__":
    run_booking_app()