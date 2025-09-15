import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
import datetime
import calendar
import json
import os

class ReminderManager:
    def __init__(self, reminder_file="reminders.json"):
        self.REMINDER_FILE = reminder_file
        self.reminders = self.load_reminders()

    def load_reminders(self):
        if os.path.exists(self.REMINDER_FILE):
            with open(self.REMINDER_FILE, "r") as f:
                return json.load(f)
        return []

    def save_reminders(self):
        with open(self.REMINDER_FILE, "w") as f:
            json.dump(self.reminders, f, indent=4)

class ReminderApp(ReminderManager):
    def __init__(self, master):
        super().__init__()
        self.master = master
        self.master.title("Simple Reminder App")
        self.master.geometry("450x420")
        self.master.configure(bg="#f0f8ff")
        self.setup_ui()
        self.check_reminders()

    def open_calendar(self, entry):
        def pick_date(year, month):
            cal_win = tk.Toplevel(self.master)
            cal_win.title("Pick a Date")
            cal_win.configure(bg="#f0f8ff")
            header = tk.Label(cal_win, text=f"{calendar.month_name[month]} {year}", 
                              font=("Arial", 12, "bold"), bg="#f0f8ff")
            header.grid(row=0, column=0, columnspan=7, pady=5)
            days = ["Mo", "Tu", "We", "Th", "Fr", "Sa", "Su"]
            for i, d in enumerate(days):
                tk.Label(cal_win, text=d, bg="#f0f8ff", fg="#2f4f4f").grid(row=1, column=i)
            month_days = calendar.monthcalendar(year, month)
            today = datetime.datetime.now().date()
            for r, week in enumerate(month_days, start=2):
                for c, day in enumerate(week):
                    if day != 0:
                        date_obj = datetime.date(year, month, day)
                        state = tk.NORMAL if date_obj >= today else tk.DISABLED
                        b = tk.Button(cal_win, text=str(day), width=3, state=state,
                                      command=lambda d=day: select_date(year, month, d, cal_win))
                        b.grid(row=r, column=c, padx=2, pady=2)
        def select_date(year, month, day, win):
            date_str = f"{year}-{month:02d}-{day:02d}"
            entry.delete(0, tk.END)
            entry.insert(0, date_str)
            win.destroy()
        now = datetime.datetime.now()
        pick_date(now.year, now.month)

    def setup_ui(self):
        title_label = tk.Label(
            self.master,
            text="📅 Simple Reminder App",
            font=("Arial", 16, "bold"),
            bg="#f0f8ff",
            fg="#2f4f4f"
        )
        title_label.pack(pady=10)
        self.listbox = tk.Listbox(self.master, width=55, height=10, font=("Arial", 11), bg="#ffffff")
        self.listbox.pack(pady=10)
        self.refresh_listbox()
        btn_frame = tk.Frame(self.master, bg="#f0f8ff")
        btn_frame.pack()
        add_btn = tk.Button(btn_frame, text="Add", width=10, bg="#90ee90", command=self.add_reminder)
        add_btn.grid(row=0, column=0, padx=5, pady=5)
        edit_btn = tk.Button(btn_frame, text="Edit", width=10, bg="#87ceeb", command=self.edit_reminder)
        edit_btn.grid(row=0, column=1, padx=5, pady=5)
        delete_btn = tk.Button(btn_frame, text="Delete", width=10, bg="#ffcccb", command=self.delete_reminder)
        delete_btn.grid(row=0, column=2, padx=5, pady=5)
        snooze_btn = tk.Button(btn_frame, text="Snooze", width=10, bg="#f5deb3", command=self.snooze_reminder)
        snooze_btn.grid(row=0, column=3, padx=5, pady=5)
        quit_btn = tk.Button(btn_frame, text="Quit", width=15, bg="red", fg="white", command=self.quit_app)
        quit_btn.grid(row=1, column=0, columnspan=4, pady=10)

    def refresh_listbox(self):
        self.listbox.delete(0, tk.END)
        for i, r in enumerate(self.reminders):
            self.listbox.insert(tk.END, f"{i+1}. {r['task']} at {r['time']}")

    def validate_datetime(self, time_str):
        try:
            dt = datetime.datetime.strptime(time_str, "%Y-%m-%d %H:%M")
            if dt < datetime.datetime.now():
                return False
            return True
        except ValueError:
            return False

    def add_reminder(self):
        win = tk.Toplevel(self.master)
        win.title("Add Reminder")
        win.geometry("300x280")
        win.configure(bg="#f0f8ff")
        tk.Label(win, text="Task:", bg="#f0f8ff").pack(pady=5)
        task_entry = tk.Entry(win, width=30)
        task_entry.pack(pady=5)
        tk.Label(win, text="Date:", bg="#f0f8ff").pack(pady=5)
        date_entry = tk.Entry(win, width=18)
        date_entry.pack(pady=5)
        tk.Button(win, text="📅 Pick Date", command=lambda: self.open_calendar(date_entry)).pack(pady=5)
        tk.Label(win, text="Time (HH:MM):", bg="#f0f8ff").pack(pady=5)
        time_frame = tk.Frame(win, bg="#f0f8ff")
        time_frame.pack(pady=5)
        hour_var = tk.StringVar()
        minute_var = tk.StringVar()
        hour_combo = ttk.Combobox(time_frame, width=5, textvariable=hour_var, values=[f"{i:02d}" for i in range(24)])
        hour_combo.set("12")
        hour_combo.pack(side=tk.LEFT, padx=2)
        minute_combo = ttk.Combobox(time_frame, width=5, textvariable=minute_var, values=[f"{i:02d}" for i in range(60)])
        minute_combo.set("00")
        minute_combo.pack(side=tk.LEFT, padx=2)
        def save_new_reminder():
            task = task_entry.get()
            date_str = date_entry.get()
            hour = hour_var.get()
            minute = minute_var.get()
            time_str = f"{date_str} {hour}:{minute}"
            if task and self.validate_datetime(time_str):
                self.reminders.append({"task": task, "time": time_str})
                self.save_reminders()
                self.refresh_listbox()
                messagebox.showinfo("Reminder Added", "Your reminder was added successfully!")
                win.destroy()
            else:
                messagebox.showerror("Invalid Input", "Please enter a valid task and a future date/time.")
        tk.Button(win, text="Save", bg="#90ee90", command=save_new_reminder).pack(pady=10)

    def edit_reminder(self):
        selection = self.listbox.curselection()
        if selection:
            idx = selection[0]
            current_task = self.reminders[idx]["task"]
            current_time = self.reminders[idx]["time"]
            current_date, current_clock = current_time.split(" ")
            current_hour, current_minute = current_clock.split(":")
            win = tk.Toplevel(self.master)
            win.title("Edit Reminder")
            win.geometry("300x280")
            win.configure(bg="#f0f8ff")
            tk.Label(win, text="Task:", bg="#f0f8ff").pack(pady=5)
            task_entry = tk.Entry(win, width=30)
            task_entry.insert(0, current_task)
            task_entry.pack(pady=5)
            tk.Label(win, text="Date:", bg="#f0f8ff").pack(pady=5)
            date_entry = tk.Entry(win, width=18)
            date_entry.insert(0, current_date)
            date_entry.pack(pady=5)
            tk.Button(win, text="📅 Pick Date", command=lambda: self.open_calendar(date_entry)).pack(pady=5)
            tk.Label(win, text="Time (HH:MM):", bg="#f0f8ff").pack(pady=5)
            time_frame = tk.Frame(win, bg="#f0f8ff")
            time_frame.pack(pady=5)
            hour_var = tk.StringVar(value=current_hour)
            minute_var = tk.StringVar(value=current_minute)
            hour_combo = ttk.Combobox(time_frame, width=5, textvariable=hour_var, values=[f"{i:02d}" for i in range(24)])
            hour_combo.pack(side=tk.LEFT, padx=2)
            minute_combo = ttk.Combobox(time_frame, width=5, textvariable=minute_var, values=[f"{i:02d}" for i in range(60)])
            minute_combo.pack(side=tk.LEFT, padx=2)
            def save_edit_reminder():
                task = task_entry.get()
                date_str = date_entry.get()
                hour = hour_var.get()
                minute = minute_var.get()
                new_time = f"{date_str} {hour}:{minute}"
                if task and self.validate_datetime(new_time):
                    self.reminders[idx] = {"task": task, "time": new_time}
                    self.save_reminders()
                    self.refresh_listbox()
                    win.destroy()
                else:
                    messagebox.showerror("Invalid Input", "Please enter a valid task and a future date/time.")
            tk.Button(win, text="Save", bg="#87ceeb", command=save_edit_reminder).pack(pady=10)
        else:
            messagebox.showwarning("Edit Reminder", "Please select a reminder.")

    def delete_reminder(self):
        selection = self.listbox.curselection()
        if selection:
            idx = selection[0]
            self.reminders.pop(idx)
            self.save_reminders()
            self.refresh_listbox()
        else:
            messagebox.showwarning("Delete Reminder", "Please select a reminder.")

    def snooze_reminder(self):
        selection = self.listbox.curselection()
        if selection:
            idx = selection[0]
            snooze_mins = simpledialog.askinteger("Snooze Reminder", "Enter snooze minutes:", minvalue=1)
            if snooze_mins:
                old_time = datetime.datetime.strptime(self.reminders[idx]["time"], "%Y-%m-%d %H:%M")
                new_time = old_time + datetime.timedelta(minutes=snooze_mins)
                self.reminders[idx]["time"] = new_time.strftime("%Y-%m-%d %H:%M")
                self.save_reminders()
                self.refresh_listbox()
        else:
            messagebox.showwarning("Snooze Reminder", "Please select a reminder.")

    def check_reminders(self):
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        for r in self.reminders:
            if r["time"] == now:
                messagebox.showinfo("Reminder", f"🔔 {r['task']} (at {r['time']})")
        self.master.after(60000, self.check_reminders)

    def quit_app(self):
        self.master.destroy()

def run_reminder_app():
    root = tk.Tk()
    app = ReminderApp(root)
    root.mainloop()

if __name__ == "__main__":
    run_reminder_app()