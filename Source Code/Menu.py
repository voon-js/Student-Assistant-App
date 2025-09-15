import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime, timedelta
import gpa_calculator
import calendar_app
import simple_reminder_app
import room_booking


# --- Main Application Class ---
class TARUMTApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Intranet")
        self.root.geometry("800x600")
        self.root.configure(bg="#e0f7fa") # Light cyan background

        self.frames = {}
        self._create_main_menu()

    def _create_main_menu(self):
        # Clear existing content
        for widget in self.root.winfo_children():
            widget.destroy()

        main_frame = tk.Frame(self.root, bg="#e0f7fa", bd=10, relief="raised")
        main_frame.pack(pady=50, padx=50, fill="both", expand=True)

        tk.Label(main_frame, text="Student Intranet", font=("Arial", 24, "bold"), bg="#e0f7fa", fg="#00796b").pack(pady=20)

        button_style = {"font": ("Arial", 16), "bg": "#4db6ac", "fg": "white", "width": 25, "height": 2, "relief": "raised", "bd": 5}

        tk.Button(main_frame, text="Discussion Room Booking 📚", command=self._show_room_booking, **button_style).pack(pady=15)
        tk.Button(main_frame, text="GPA Calculator 📈", command=self._show_gpa_calculator, **button_style).pack(pady=15)
        tk.Button(main_frame, text="Basic Calendar/Timetable 🗓️", command=self._show_calendar, **button_style).pack(pady=15)
        tk.Button(main_frame, text="Simple Reminder App 🔔", command=self._show_reminder, **button_style).pack(pady=15)

    def _show_frame(self, frame_class):
        # Destroy current active frame if any
        for frame in self.root.winfo_children():
            if frame.winfo_class() == "Frame" and frame != self.main_frame: # Avoid destroying main menu if it's there
                frame.destroy()

        # Create or show the requested frame
        if frame_class not in self.frames:
            new_frame = frame_class(self.root, self._show_main_menu)
            self.frames[frame_class] = new_frame
        else:
            new_frame = self.frames[frame_class]
            new_frame.show() # Call a show method if available in sub-app

    def _show_room_booking(self):
        room_booking.run_booking_app()

    def _show_gpa_calculator(self):
        gpa_calculator.run_calculator()

    def _show_calendar(self):
        calendar_app.run_calender_app()

    def _show_reminder(self):
        simple_reminder_app.run_reminder_app()

    def _show_main_menu(self):
        self._create_main_menu()
        
        self.frames = {}


# --- Application Entry Point ---
if __name__ == "__main__":
    root = tk.Tk()
    app = TARUMTApp(root)
    root.mainloop()
