import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime, timedelta
import calendar
import os

BG_COLOR = "#2c2f33"
FG_COLOR = "#ffffff"
BTN_COLOR = "#7289da"
SELECT_COLOR = "#5865f2"
TODAY_COLOR = "#43b581"
EVENT_COLOR = "#faa61a"
DISABLED_COLOR = "#99aab5"
FILENAME = "timetable.txt"

class BaseCalendar(tk.Tk):
    """Base calendar window with navigation and date selection."""
    def __init__(self):
        super().__init__()
        self.title("📅 Modern Calendar")
        self.configure(bg=BG_COLOR)
        self.today = datetime.today()
        self.current_date = self.today
        self.selected_date = None

        self.date_label = tk.Label(self, text="", bg=BG_COLOR, fg=FG_COLOR, font=("Arial", 14))
        self.date_label.pack(pady=10)

        self.cal_frame = tk.Frame(self, bg=BG_COLOR)
        self.cal_frame.pack()

        nav_frame = tk.Frame(self, bg=BG_COLOR)
        nav_frame.pack(pady=10)

        prev_btn = tk.Button(nav_frame, text="Prev.", command=self.prev_month,
                             bg=BTN_COLOR, fg="white", relief="flat", width=8)
        prev_btn.grid(row=0, column=0, padx=10)

        self.month_var = tk.StringVar()
        self.year_var = tk.StringVar()

        months = list(calendar.month_name)[1:]
        self.month_combo = ttk.Combobox(nav_frame, textvariable=self.month_var, values=months, state="readonly", width=10)
        self.month_combo.grid(row=0, column=1, padx=5)

        years = [str(y) for y in range(1970, 2101)]
        self.year_combo = ttk.Combobox(nav_frame, textvariable=self.year_var, values=years, state="readonly", width=6)
        self.year_combo.grid(row=0, column=2, padx=5)

        go_btn = tk.Button(nav_frame, text="Go", command=self.go_to_month,
                           bg=BTN_COLOR, fg="white", relief="flat", width=6)
        go_btn.grid(row=0, column=3, padx=5)

        next_btn = tk.Button(nav_frame, text="Next", command=self.next_month,
                             bg=BTN_COLOR, fg="white", relief="flat", width=8)
        next_btn.grid(row=0, column=4, padx=10)

    def prev_month(self):
        first = self.current_date.replace(day=1)
        prev_month = first - timedelta(days=1)
        self.current_date = prev_month.replace(day=1)
        self.draw_calendar()

    def next_month(self):
        days_in_month = calendar.monthrange(self.current_date.year, self.current_date.month)[1]
        next_month = self.current_date + timedelta(days=days_in_month)
        self.current_date = next_month.replace(day=1)
        self.draw_calendar()

    def select_date(self, date):
        self.selected_date = date
        self.current_date = date.replace(day=1)
        self.draw_calendar()
        self.show_events(date)

    def go_to_month(self):
        try:
            month = list(calendar.month_name).index(self.month_var.get())
            year = int(self.year_var.get())
            self.current_date = datetime(year, month, 1)
            self.selected_date = self.current_date.date()
            self.draw_calendar()
            self.show_events(self.selected_date)
        except Exception:
            messagebox.showerror("Invalid Selection", "Please choose a valid month and year.")

    def draw_calendar(self):
        # To be overridden in subclass
        pass

    def show_events(self, date):
        # To be overridden in subclass
        pass

class EventManager:
    """Handles loading, saving, and managing events."""
    def __init__(self):
        self.events = self.load_events()

    def load_events(self):
        events = {}
        if os.path.exists(FILENAME):
            with open(FILENAME, "r") as f:
                for line in f:
                    date, time, name = line.strip().split(" | ")
                    if date not in events:
                        events[date] = []
                    events[date].append((time, name))
        return events

    def save_events(self):
        with open(FILENAME, "w") as f:
            for date in self.events:
                for time, name in self.events[date]:
                    f.write(f"{date} | {time} | {name}\n")

class DarkCalendar(BaseCalendar, EventManager):
    """Main calendar app with event management and UI."""
    def __init__(self):
        BaseCalendar.__init__(self)
        EventManager.__init__(self)

        self.event_label = tk.Label(self, text="Events:", bg=BG_COLOR, fg=FG_COLOR, font=("Arial", 12))
        self.event_label.pack(pady=5)

        self.event_list = tk.Listbox(self, width=40, height=6, bg=BG_COLOR, fg=FG_COLOR, selectbackground=SELECT_COLOR)
        self.event_list.pack(pady=5)

        event_btns = tk.Frame(self, bg=BG_COLOR)
        event_btns.pack(pady=5)

        add_event_btn = tk.Button(event_btns, text="Add Event", command=self.add_event,
                                  bg=BTN_COLOR, fg="white", relief="flat", width=12)
        add_event_btn.grid(row=0, column=0, padx=5)

        edit_event_btn = tk.Button(event_btns, text="Edit Event", command=self.edit_event,
                                   bg="#f1c40f", fg="black", relief="flat", width=12)
        edit_event_btn.grid(row=0, column=1, padx=5)

        delete_event_btn = tk.Button(event_btns, text="Delete Event", command=self.delete_event,
                                     bg="#e74c3c", fg="white", relief="flat", width=12)
        delete_event_btn.grid(row=0, column=2, padx=5)

        input_frame = tk.Frame(self, bg=BG_COLOR)
        input_frame.pack(pady=5)

        tk.Label(input_frame, text="Time:", bg=BG_COLOR, fg=FG_COLOR).grid(row=0, column=0, padx=5)

        times = [f"{h:02d}:{m:02d}" for h in range(0, 24) for m in (0, 30)]
        self.time_var = tk.StringVar()
        self.time_combo = ttk.Combobox(input_frame, textvariable=self.time_var, values=times, state="readonly", width=10)
        self.time_combo.grid(row=0, column=1, padx=5)

        tk.Label(input_frame, text="Event:", bg=BG_COLOR, fg=FG_COLOR).grid(row=0, column=2, padx=5)
        self.event_entry = tk.Entry(input_frame, width=20)
        self.event_entry.grid(row=0, column=3, padx=5)

        self.draw_calendar()

    def draw_calendar(self):
        # Draw the calendar grid for the current month
        for widget in self.cal_frame.winfo_children():
            widget.destroy()

        year = self.current_date.year
        month = self.current_date.month
        self.date_label.config(text=self.current_date.strftime("%B %Y"))

        days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        for i, day in enumerate(days):
            tk.Label(self.cal_frame, text=day, bg=BG_COLOR, fg=FG_COLOR, width=6).grid(row=0, column=i)

        cal = calendar.Calendar(firstweekday=0)
        month_days = cal.monthdatescalendar(year, month)

        for row, week in enumerate(month_days, start=1):
            for col, day in enumerate(week):
                if day.month != month:
                    lbl = tk.Label(self.cal_frame, text=day.day, bg=BG_COLOR, fg=DISABLED_COLOR, width=6)
                else:
                    bg = BG_COLOR
                    fg = FG_COLOR
                    date_str = day.strftime("%Y-%m-%d")

                    if self.selected_date and day == self.selected_date:
                        bg = SELECT_COLOR
                        fg = "white"
                    elif day == self.today.date():
                        bg = TODAY_COLOR
                        fg = "white"
                    elif date_str in self.events:
                        bg = EVENT_COLOR
                        fg = "black"

                    lbl = tk.Label(self.cal_frame, text=day.day, bg=bg, fg=fg, width=6)
                    lbl.bind("<Button-1>", lambda e, d=day: self.select_date(d))
                lbl.grid(row=row, column=col, padx=2, pady=2)

        self.month_var.set(calendar.month_name[month])
        self.year_var.set(str(year))

    def show_events(self, date):
        date_str = date.strftime("%Y-%m-%d")
        self.event_list.delete(0, tk.END)
        self.event_list.insert(tk.END, f"📅 {date.strftime('%d-%m-%Y')}")
        self.event_list.insert(tk.END, "-" * 40)
        if date_str in self.events:
            for time, name in sorted(self.events[date_str]):
                self.event_list.insert(tk.END, f" ⏰ {time} - {name}")
        else:
            self.event_list.insert(tk.END, " No events.")

    def add_event(self):
        if not self.selected_date:
            messagebox.showwarning("No Date Selected", "Please select a date first.")
            return

        time = self.time_var.get()
        name = self.event_entry.get()
        date_str = self.selected_date.strftime("%Y-%m-%d")

        if not time or not name:
            messagebox.showwarning("Input Error", "Please enter both time and event name.")
            return

        if date_str not in self.events:
            self.events[date_str] = []
        self.events[date_str].append((time, name))
        self.save_events()
        self.show_events(self.selected_date)
        self.draw_calendar()

        self.time_var.set("")
        self.event_entry.delete(0, tk.END)

    def delete_event(self):
        if not self.selected_date:
            messagebox.showwarning("No Date Selected", "Please select a date first.")
            return

        date_str = self.selected_date.strftime("%Y-%m-%d")

        try:
            selection = self.event_list.curselection()
            if not selection or selection[0] < 2:
                raise IndexError
            event_index = selection[0] - 2
            del self.events[date_str][event_index]
            if not self.events[date_str]:
                del self.events[date_str]
            self.save_events()
            self.show_events(self.selected_date)
            self.draw_calendar()
        except IndexError:
            messagebox.showwarning("No Event Selected", "Please select an event to delete.")

    def edit_event(self):
        if not self.selected_date:
            messagebox.showwarning("No Date Selected", "Please select a date first.")
            return

        selection = self.event_list.curselection()
        if not selection or selection[0] < 2:
            messagebox.showwarning("No Event Selected", "Please select an event to edit.")
            return

        date_str = self.selected_date.strftime("%Y-%m-%d")
        event_index = selection[0] - 2
        old_time, old_name = self.events[date_str][event_index]

        self.time_var.set(old_time)
        self.event_entry.delete(0, tk.END)
        self.event_entry.insert(0, old_name)

        def save_edit():
            new_time = self.time_var.get()
            new_name = self.event_entry.get()
            if not new_time or not new_name:
                messagebox.showwarning("Input Error", "Please enter both time and event name.")
                return
            self.events[date_str][event_index] = (new_time, new_name)
            self.save_events()
            self.show_events(self.selected_date)
            self.draw_calendar()
            edit_window.destroy()

        edit_window = tk.Toplevel(self)
        edit_window.title("Edit Event")
        edit_window.configure(bg=BG_COLOR)

        tk.Label(edit_window, text="Editing Event:", bg=BG_COLOR, fg=FG_COLOR).pack(pady=5)
        tk.Label(edit_window, text=f"{old_time} - {old_name}", bg=BG_COLOR, fg=FG_COLOR).pack(pady=5)
        tk.Button(edit_window, text="Save Changes", command=save_edit,
                  bg=BTN_COLOR, fg="white", relief="flat").pack(pady=10)

def run_calender_app():
    app = DarkCalendar()
    app.mainloop()

if __name__ == "__main__":
    run_calender_app()