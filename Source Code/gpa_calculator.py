import tkinter as tk
from tkinter import messagebox, filedialog, ttk

class Course:
    #create new object
    def __init__(self, name: str, credit: int, marks: int):
        self.name = name
        self.credit = credit
        self.marks = marks
        self.grade, self.grade_point = self.convert_marks_to_grade(marks)

    #convert marks to grade
    def convert_marks_to_grade(self, marks):
        if 80 <= marks <= 100:
            return "A", 4.0000
        elif 75 <= marks <= 79:
            return "A-", 3.7500
        elif 70 <= marks <= 74:
            return "B+", 3.5000
        elif 65 <= marks <= 69:
            return "B", 3.0000
        elif 60 <= marks <= 64:
            return "B-", 2.7500
        elif 55 <= marks <= 59:
            return "C+", 2.5000
        elif 50 <= marks <= 54:
            return "C", 2.0000
        elif 0 <= marks <= 49:
            return "F", 0.0000
        else:
            return "Invalid", 0.0000

    # convert full format
    def __str__(self):
        return f"{self.name} ({self.credit} credits) - Marks: {self.marks}, Grade: {self.grade}, GP: {self.grade_point}"


class Student(Course):
    # create new student
    def __init__(self, name: str):
        self.student_name = name
        self.courses = []

    #add new course
    def add_course(self, course: Course):
        self.courses.append(course)

    #calculate student gpa
    def calculate_gpa(self):
        total_points = 0
        total_credits = 0
        for course in self.courses:
            total_points += course.grade_point * course.credit
            total_credits += course.credit
        if total_credits == 0:
            return 0.0
        return round(total_points / total_credits, 4)

    #get student total credits
    def total_credits(self):
        return sum(course.credit for course in self.courses)

    #save data to txt file
    def save_to_file(self, filename="gpa_data.txt"):
        try:
            with open(filename, "w") as f:
                for course in self.courses:
                    f.write(f"{course.name},{course.credit},{course.marks}\n")
            messagebox.showinfo("Saved", f"Data saved to {filename}")
        except:
            messagebox.showerror("Error", "Unable to save file. Please try again.")

    #load data from txt file
    def load_from_file(self, filename="gpa_data.txt"):
        try:
            self.courses.clear()
            with open(filename, "r") as f:
                for line in f:
                    name, credit, marks = line.strip().split(",")
                    self.add_course(Course(name, int(credit), int(marks)))
            messagebox.showinfo("Loaded", f"Data loaded from {filename}")
        except FileNotFoundError:
            messagebox.showwarning("Warning", "No saved data found!")
        except:
            messagebox.showerror("Error", "Unable to load file. Please check the file and try again.")


class GPAApp:
    #create new window
    def __init__(self, root):
        self.student = Student("John Doe")
        self.root = root
        self.root.title("GPA Calculator")
        self.root.geometry("580x500")

        grade_text = """GRADE | MARKS RANGE | GRADE POINT
A     | 80 – 100    | 4.0000
A-    | 75 – 79     | 3.7500
B+    | 70 – 74     | 3.5000
B     | 65 – 69     | 3.0000
B-    | 60 – 64     | 2.7500
C+    | 55 – 59     | 2.5000
C     | 50 – 54     | 2.0000
F     | 0 – 49      | 0.0000"""

        grade_frame = tk.Frame(root)
        grade_frame.pack(pady=5)
        tk.Label(grade_frame, text="GRADE TABLE", font=("Arial", 12, "bold")).pack()
        grade_box = tk.Text(grade_frame, width=60, height=9, font=("Courier", 11))
        grade_box.tag_configure("center", justify='center')
        grade_box.pack()
        grade_box.insert(tk.END, grade_text, "center")
        grade_box.config(state=tk.DISABLED)

        input_frame = tk.Frame(root)
        input_frame.pack(pady=10)
        tk.Label(input_frame, text="Course Name:").grid(row=0, column=0, padx=5)
        self.course_entry = tk.Entry(input_frame, width=15)
        self.course_entry.grid(row=0, column=1, padx=5)
        tk.Label(input_frame, text="Credit Hours:").grid(row=0, column=2, padx=5)
        self.credit_entry = tk.Entry(input_frame, width=5)
        self.credit_entry.grid(row=0, column=3, padx=5)
        tk.Label(input_frame, text="Marks (0-100):").grid(row=0, column=4, padx=5)
        self.marks_entry = tk.Entry(input_frame, width=5)
        self.marks_entry.grid(row=0, column=5, padx=5)
        tk.Button(input_frame, text="Add Course", command=self.add_course).grid(row=0, column=6, padx=10)

        self.courses_list = tk.Listbox(root, width=90, height=10)
        self.courses_list.pack(pady=5)

        bottom_frame = tk.Frame(root)
        bottom_frame.pack(fill="x", pady=5, padx=20)
        left_frame = tk.Frame(bottom_frame)
        left_frame.pack(side="left", anchor="w")
        tk.Button(left_frame, text="Delete Selected Course", command=self.delete_course).pack(side="left", padx=5)
        tk.Button(left_frame, text="Edit Selected Course", command=self.edit_course).pack(side="left", padx=5)

        right_frame = tk.Frame(bottom_frame)
        right_frame.pack(side="right", anchor="e")
        tk.Button(right_frame, text="Save Data", command=self.save_data).pack(side="left", padx=5)
        tk.Button(right_frame, text="Load Data", command=self.load_data).pack(side="left", padx=5)

        tk.Button(root, text="Calculate GPA", command=self.show_gpa).pack(pady=10)

    #add new courses 
    def add_course(self):
        name = self.course_entry.get().strip()
        credit_text = self.credit_entry.get().strip()
        marks_text = self.marks_entry.get().strip()
        if not name:
            messagebox.showerror("Input Error", "Course name cannot be empty")
            return
        try:
            credit = int(credit_text)
            if credit <= 0: raise ValueError
        except ValueError:
            messagebox.showerror("Input Error", "Credit hours must be positive")
            return
        try:
            marks = int(marks_text)
            if not (0 <= marks <= 100): raise ValueError
        except ValueError:
            messagebox.showerror("Input Error", "Marks must be 0-100")
            return
        course = Course(name, credit, marks)
        self.student.add_course(course)
        self.courses_list.insert(tk.END, str(course))
        self.course_entry.delete(0, tk.END)
        self.credit_entry.delete(0, tk.END)
        self.marks_entry.delete(0, tk.END)

    #delete added courses
    def delete_course(self):
        try:
            idx = self.courses_list.curselection()[0]
            self.courses_list.delete(idx)
            del self.student.courses[idx]
        except IndexError:
            messagebox.showwarning("Delete Error", "Select a course first")

    #edit added courses
    def edit_course(self):
        try:
            idx = self.courses_list.curselection()[0]
        except IndexError:
            messagebox.showwarning("Edit Error", "Select a course first")
            return

        course = self.student.courses[idx]

        edit_win = tk.Toplevel(self.root)
        edit_win.title("Edit Course")
        edit_win.geometry("300x230")
        edit_win.grab_set()

        tk.Label(edit_win, text="Course Name:").pack(pady=5)
        name_entry = tk.Entry(edit_win)
        name_entry.insert(0, course.name)
        name_entry.pack(pady=5)

        tk.Label(edit_win, text="Credit Hours:").pack(pady=5)
        credit_entry = tk.Entry(edit_win)
        credit_entry.insert(0, str(course.credit))
        credit_entry.pack(pady=5)

        tk.Label(edit_win, text="Marks:").pack(pady=5)
        marks_entry = tk.Entry(edit_win)
        marks_entry.insert(0, str(course.marks))
        marks_entry.pack(pady=5)

        #save edited changes
        def save_changes():
            try:
                new_name = name_entry.get().strip()
                new_credit = int(credit_entry.get().strip())
                new_marks = int(marks_entry.get().strip())

                if not new_name or new_credit <= 0 or not (0 <= new_marks <= 100):
                    raise ValueError

                # Update course object
                self.student.courses[idx] = Course(new_name, new_credit, new_marks)

                # Update listbox display
                self.courses_list.delete(idx)
                self.courses_list.insert(idx, str(self.student.courses[idx]))

                edit_win.destroy()
            except ValueError:
                messagebox.showerror("Invalid Input", "Please enter valid course data")

        tk.Button(edit_win, text="Save Changes", command=save_changes).pack(pady=10)

    #show final gpa
    def show_gpa(self):
        gpa = self.student.calculate_gpa()
        total_credits = self.student.total_credits()

        result_window = tk.Toplevel(self.root)
        result_window.title("GPA Result")
        result_window.geometry("650x500")
        result_window.resizable(False, False)
        result_window.grab_set()

        chart_frame = tk.Frame(result_window)
        chart_frame.pack(pady=5)
        canvas = tk.Canvas(chart_frame, width=560, height=150, bg="white")
        canvas.pack()

        grade_counts = {"A":0, "A-":0, "B+":0, "B":0, "B-":0, "C+":0, "C":0, "F":0}
        colors = {"A":"green","A-":"lime","B+":"blue","B":"cyan","B-":"orange","C+":"yellow","C":"pink","F":"red"}
        for c in self.student.courses:
            if c.grade in grade_counts:
                grade_counts[c.grade] += 1

        max_count = max(grade_counts.values()) if grade_counts.values() else 1
        bar_width = 60
        spacing = 10
        x_start = 10
        for grade in grade_counts:
            count = grade_counts[grade]
            bar_height = (count / max_count) * 120 if max_count > 0 else 0
            canvas.create_rectangle(x_start, 140-bar_height, x_start+bar_width, 140, fill=colors[grade])
            canvas.create_text(x_start+bar_width/2, 145, text=grade)
            canvas.create_text(x_start+bar_width/2, 140-bar_height-10, text=str(count))
            x_start += bar_width + spacing

        courses_frame = tk.Frame(result_window)
        courses_frame.pack(pady=10, padx=10, fill="both", expand=True)

        tree_scroll = tk.Scrollbar(courses_frame)
        tree_scroll.pack(side="right", fill="y")

        tree = ttk.Treeview(courses_frame, yscrollcommand=tree_scroll.set, columns=("Name", "Grade"), show="headings", height=12)
        tree.pack(fill="both", expand=True)
        tree_scroll.config(command=tree.yview)

        tree.heading("Name", text="COURSE NAME")
        tree.heading("Grade", text="GRADE")

        for course in self.student.courses:
            tree.insert("", tk.END, values=(course.name.upper(), course.grade.upper()))

        bottom_frame = tk.Frame(result_window)
        bottom_frame.pack(pady=10, fill="x")
        tk.Label(bottom_frame, text=f"GPA: {gpa}", font=("Helvetica", 10)).pack(side="left", anchor="w", padx=10)
        tk.Label(bottom_frame, text=f"TOTAL CREDITS: {total_credits}", font=("Helvetica", 10)).pack(side="right", anchor="e", padx=10)

    #save txt file
    def save_data(self):
        if not self.student.courses:
            messagebox.showwarning("No Data", "There are no courses to save!")
            return
        filename = filedialog.asksaveasfilename(defaultextension=".txt")
        if filename:
            self.student.save_to_file(filename)

    #load save file
    def load_data(self):
        filename = filedialog.askopenfilename(defaultextension=".txt")
        if not filename:
            return 
        try:
            self.student.courses.clear()
            valid_lines = 0
            try:
                with open(filename, "r", encoding="utf-8") as f:
                    for line in f:
                        parts = line.strip().split(",")
                        if len(parts) != 3:
                            messagebox.showwarning("Invalid File", f"Skipping invalid line: {line.strip()}")
                            continue
                        name, credit_text, marks_text = parts
                        try:
                            credit = int(credit_text)
                            marks = int(marks_text)
                            self.student.add_course(Course(name, credit, marks))
                            valid_lines += 1
                        except ValueError:
                            messagebox.showwarning("Invalid Data", f"Skipping line with invalid credit or marks: {line.strip()}")
            except UnicodeDecodeError:
                messagebox.showerror("Invalid File", "Cannot read this file. Make sure it is a valid text file.")
                return

            if valid_lines == 0:
                messagebox.showwarning("Empty File", "No valid course data found in the file.")
                return

            self.courses_list.delete(0, tk.END)
            for course in self.student.courses:
                self.courses_list.insert(tk.END, str(course))

            messagebox.showinfo("Loaded", f"Data loaded from {filename}")
        except Exception as e:
            messagebox.showerror("Error", f"Unable to load file: {e}")

#import run file
def run_calculator():
    root = tk.Tk()
    app = GPAApp(root)
    root.mainloop()

if __name__ == "__main__":
    run_calculator()