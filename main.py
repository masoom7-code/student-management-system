import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageTk

FILE_NAME = "students.txt"

def validate_roll(input):
    if input == "":
        return True
    if input.isdigit():
        return True
    return False

def validate_name(input):
    if input == "":
        return True
    if input.replace(" ", "").isalpha():
        return True
    return False

def add_student():
    roll = roll_var.get()
    name = name_var.get()
    physics = physics_var.get()
    chemistry = chemistry_var.get()
    maths = maths_var.get()

    if roll == "" or name == "" or physics == "" or chemistry == "" or maths == "":
        messagebox.showwarning("Input Error", "Please fill all fields!")
        return

    if not roll.isdigit():
        messagebox.showwarning("Input Error", "Roll No must contain only numbers!")
        return

    if not name.replace(" ", "").isalpha():
        messagebox.showwarning("Input Error", "Name must contain only letters!")
        return
    
    try:
        physics_val = float(physics)
        chemistry_val = float(chemistry)
        maths_val = float(maths)
        
        if not (0 <= physics_val <= 100 and 0 <= chemistry_val <= 100 and 0 <= maths_val <= 100):
            messagebox.showwarning("Input Error", "Marks must be between 0 and 100!")
            return
    except ValueError:
        messagebox.showwarning("Input Error", "Marks must be numbers!")
        return

    with open(FILE_NAME, "a") as f:
        f.write(f"{roll},{name},{physics},{chemistry},{maths}\n")

    messagebox.showinfo("Success", "Student added successfully!")
    clear_fields()
    show_students()

def show_students():
    for row in tree.get_children():
        tree.delete(row)
    try:
        with open(FILE_NAME, "r") as f:
            for line in f:
                data = line.strip().split(",")
                if len(data) >= 5:
                    roll, name, physics, chemistry, maths = data[:5]
                    
                    pcm_avg = (float(physics) + float(chemistry) + float(maths)) / 3
                    status = "Eligible" if pcm_avg >= 50 else "Failed"
                    tree.insert("", "end", values=(roll, name, physics, chemistry, maths, f"{pcm_avg:.1f}%", status))
    except FileNotFoundError:
        open(FILE_NAME, "w").close()

def search_student():
    search_roll = roll_var.get()
    found = False
    for row in tree.get_children():
        tree.delete(row)
    try:
        with open(FILE_NAME, "r") as f:
            for line in f:
                data = line.strip().split(",")
                if len(data) >= 5:
                    roll, name, physics, chemistry, maths = data[:5]
                    if roll == search_roll:
                        
                        pcm_avg = (float(physics) + float(chemistry) + float(maths)) / 3
                        status = "Eligible" if pcm_avg >= 50 else "Failed"
                        tree.insert("", "end", values=(roll, name, physics, chemistry, maths, f"{pcm_avg:.1f}%", status))
                        found = True
        if not found:
            messagebox.showinfo("Result", "No student found with that Roll Number.")
    except FileNotFoundError:
        messagebox.showwarning("Error", "No data file found.")

def delete_student():
    roll_to_delete = roll_var.get()
    if roll_to_delete == "":
        messagebox.showwarning("Input Error", "Enter Roll Number to delete!")
        return

    deleted = False
    try:
        with open(FILE_NAME, "r") as f:
            lines = f.readlines()
        with open(FILE_NAME, "w") as f:
            for line in lines:
                data = line.strip().split(",")
                if len(data) >= 5:
                    roll = data[0]
                    if roll != roll_to_delete:
                        f.write(line)
                    else:
                        deleted = True
        if deleted:
            messagebox.showinfo("Deleted", "Record deleted successfully!")
        else:
            messagebox.showinfo("Not Found", "Roll Number not found.")
        show_students()
    except FileNotFoundError:
        messagebox.showwarning("Error", "No data file found.")

def clear_fields():
    roll_var.set("")
    name_var.set("")
    physics_var.set("")
    chemistry_var.set("")
    maths_var.set("")

root = tk.Tk()
root.title("Student Management System - PCM")
root.geometry("800x550")  
root.resizable(True, True)
root.configure(bg="#f5f6fa")

roll_var = tk.StringVar()
name_var = tk.StringVar()
physics_var = tk.StringVar()
chemistry_var = tk.StringVar()
maths_var = tk.StringVar()

header_frame = tk.Frame(root, bg="#2c3e50", height=70)
header_frame.pack(fill="x", padx=15, pady=(15, 10))
header_frame.pack_propagate(False)

tk.Label(header_frame, text="Student Management System - PCM", 
         font=("Arial", 16, "bold"), bg="#2c3e50", fg="white").pack(expand=True)

main_frame = tk.Frame(root, bg="#f5f6fa")
main_frame.pack(fill="both", expand=True, padx=15, pady=10)

input_frame = tk.LabelFrame(main_frame, text="Student Information", 
                           font=("Arial", 10, "bold"), bg="#f5f6fa", fg="#2c3e50",
                           relief="solid", bd=1)
input_frame.pack(fill="x", pady=(0, 15))

form_image_frame = tk.Frame(input_frame, bg="#f5f6fa")
form_image_frame.pack(fill="x", padx=10, pady=10)

form_frame = tk.Frame(form_image_frame, bg="#f5f6fa")
form_frame.pack(side="left", fill="both", expand=True)

fields = [
    ("Roll No:", roll_var),
    ("Name:", name_var),
    ("Physics:", physics_var),
    ("Chemistry:", chemistry_var),
    ("Maths:", maths_var)
]

for i, (label_text, var) in enumerate(fields):
    tk.Label(form_frame, text=label_text, bg="#f5f6fa", fg="#2c3e50", 
             font=("Arial", 9, "bold")).grid(row=i, column=0, sticky="e", padx=(15, 8), pady=8)
    
    entry = tk.Entry(form_frame, textvariable=var, width=30, font=("Arial", 9),
                    relief="solid", bd=1, bg="white")
    entry.grid(row=i, column=1, sticky="w", padx=(0, 15), pady=8)

info_frame = tk.Frame(form_frame, bg="#f5f6fa")
info_frame.grid(row=5, column=0, columnspan=2, pady=5)
tk.Label(info_frame, text="Eligibility: PCM Average ≥ 50%", 
         font=("Arial", 8, "italic"), bg="#f5f6fa", fg="#e74c3c").pack()

image_frame = tk.Frame(form_image_frame, bg="#f5f6fa")
image_frame.pack(side="right", padx=20)

try:
    image = Image.open("walchand.jpg")
    image = image.resize((120, 120), Image.Resampling.LANCZOS)
    photo = ImageTk.PhotoImage(image)
    image_label = tk.Label(image_frame, image=photo, bg="#f5f6fa")
    image_label.image = photo  
    image_label.pack(pady=10)
    
    tk.Label(image_frame, text="Walchand College", 
             font=("Arial", 10, "bold"), bg="#f5f6fa", fg="#2c3e50").pack()
    
except Exception as e:
    tk.Label(image_frame, text="Image\nNot Found", 
             font=("Arial", 10), bg="#f5f6fa", fg="#7f8c8d", 
             relief="solid", bd=1, width=15, height=8).pack(pady=10)
    tk.Label(image_frame, text="walchand.jpg", 
             font=("Arial", 8), bg="#f5f6fa", fg="#7f8c8d").pack()

btn_frame = tk.Frame(main_frame, bg="#f5f6fa")
btn_frame.pack(fill="x", pady=15)

button_configs = [
    ("Add", "#27ae60", "#2ecc71", add_student),
    ("Search", "#2980b9", "#3498db", search_student),
    ("Delete", "#c0392b", "#e74c3c", delete_student),
    ("Clear", "#f39c12", "#f1c40f", clear_fields)
]

for i, (text, color, hover_color, command) in enumerate(button_configs):
    btn = tk.Button(btn_frame, text=text, command=command, 
                   bg=color, fg="white", font=("Arial", 10, "bold"),
                   relief="flat", bd=0, padx=18, pady=8, width=10,
                   cursor="hand2")
    
    def on_enter(e, btn=btn, color=hover_color):
        btn['bg'] = color
    def on_leave(e, btn=btn, color=color):
        btn['bg'] = color
        
    btn.bind("<Enter>", on_enter)
    btn.bind("<Leave>", on_leave)
    
    btn.grid(row=0, column=i, padx=6)

tree_frame = tk.LabelFrame(main_frame, text="Student Records - PCM", 
                          font=("Arial", 10, "bold"), bg="#f5f6fa", fg="#2c3e50",
                          relief="solid", bd=1)
tree_frame.pack(fill="both", expand=True, pady=(10, 0))

tree_scroll = ttk.Scrollbar(tree_frame)
tree_scroll.pack(side="right", fill="y")

style = ttk.Style()
style.theme_use("clam")
style.configure("Treeview", 
                background="white",
                foreground="black",
                rowheight=25,
                fieldbackground="white",
                font=("Arial", 9))
style.configure("Treeview.Heading",
                font=("Arial", 9, "bold"),
                background="#34495e",
                foreground="white",
                relief="flat")

tree = ttk.Treeview(tree_frame, columns=("Roll", "Name", "Physics", "Chemistry", "Maths", "PCM Avg", "Status"), 
                   show="headings", height=12, yscrollcommand=tree_scroll.set)

tree.heading("Roll", text="Roll No")
tree.heading("Name", text="Name")
tree.heading("Physics", text="Physics")
tree.heading("Chemistry", text="Chemistry")
tree.heading("Maths", text="Maths")
tree.heading("PCM Avg", text="PCM Average")
tree.heading("Status", text="Status")

tree.column("Roll", width=80, anchor="center")
tree.column("Name", width=150, anchor="w")
tree.column("Physics", width=70, anchor="center")
tree.column("Chemistry", width=80, anchor="center")
tree.column("Maths", width=70, anchor="center")
tree.column("PCM Avg", width=90, anchor="center")
tree.column("Status", width=80, anchor="center")

tree.pack(fill="both", expand=True, padx=8, pady=8)
tree_scroll.config(command=tree.yview)

footer_frame = tk.Frame(root, bg="#ecf0f1", height=30)
footer_frame.pack(fill="x", side="bottom", padx=15, pady=(0, 10))
footer_frame.pack_propagate(False)

tk.Label(footer_frame, text="Student Management System - PCM v1.0", 
         font=("Arial", 8), bg="#ecf0f1", fg="#7f8c8d").pack(side="right", padx=10)

show_students()

root.mainloop()