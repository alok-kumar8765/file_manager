# ================================
# File Organizer Ultimate Pro v3
# ================================

import tkinter as tk
from tkinter import filedialog, ttk, simpledialog, messagebox
import os, shutil
import datetime

# --------------------------
# Config & Globals
# --------------------------
root = tk.Tk()
root.title("File Organizer Ultimate Pro v3")
root.geometry("800x700")

# Default theme: dark
THEMES = {"Dark": {"bg": "#111", "fg": "#0ff", "entry_bg": "#333"},
          "Light": {"bg": "#eee", "fg": "#111", "entry_bg": "#fff"}}
current_theme = "Dark"

root.configure(bg=THEMES[current_theme]["bg"])

status_var = tk.StringVar(value="Ready to Organize")
progress_var = tk.DoubleVar(value=0)

TYPES = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".tiff", ".bmp"],
    "Docs": [".pdf", ".docx", ".txt", ".pages", ".xlsx", ".pptx"],
    "Videos": [".mp4", ".mov", ".avi", ".flv", ".mkv"],
    "Audio": [".mp3", ".wav", ".aac"],
    "Code": [".py", ".md", ".html", ".js", ".css", ".java"]
}

undo_history = []
selected_folder = tk.StringVar(value="Drop folder here or click to select")
file_selection = []

# Log file path
LOG_FILE = "file_organizer_log.txt"

# --------------------------
# Utility Functions
# --------------------------
def apply_theme():
    theme = THEMES[current_theme]
    root.configure(bg=theme["bg"])
    for widget in root.winfo_children():
        if isinstance(widget, (tk.Label, tk.Button, tk.Listbox, tk.Entry, tk.Frame)):
            widget.configure(bg=theme["bg"], fg=theme["fg"])
    preview_listbox.configure(bg=theme["entry_bg"])

def toggle_theme():
    global current_theme
    current_theme = "Light" if current_theme == "Dark" else "Dark"
    apply_theme()

def add_category():
    name = simpledialog.askstring("New Category", "Enter category name:")
    if not name or name in TYPES:
        messagebox.showinfo("Info", "Category already exists or invalid!")
        return
    TYPES[name] = []
    update_category_list()

def add_extension():
    cat = category_listbox.get(tk.ACTIVE)
    if not cat: return
    cat_name = cat.split(":")[0]
    ext = simpledialog.askstring("New Extension", f"Enter extension for {cat_name} (with dot):")
    if not ext or not ext.startswith(".") or ext in TYPES[cat_name]: return
    TYPES[cat_name].append(ext)
    update_category_list()

def update_category_list():
    category_listbox.delete(0, tk.END)
    for cat, exts in TYPES.items():
        category_listbox.insert(tk.END, f"{cat}: {', '.join(exts)}")

def select_folder():
    folder = filedialog.askdirectory()
    if folder:
        selected_folder.set(folder)
        preview_files(folder)

def preview_files(folder, filter_type=None, date_from=None, date_to=None):
    global file_selection
    file_selection = []
    preview_listbox.delete(0, tk.END)
    
    for root_dir, _, files in os.walk(folder):
        for file in files:
            file_path = os.path.join(root_dir, file)
            ext = os.path.splitext(file)[1].lower()
            mod_time = datetime.datetime.fromtimestamp(os.path.getmtime(file_path))
            
            # Filter by type/extension
            if filter_type and ext not in filter_type: 
                continue
            # Filter by date range
            if date_from and mod_time < date_from:
                continue
            if date_to and mod_time > date_to:
                continue
            
            file_selection.append(file_path)
            preview_listbox.insert(tk.END, f"{file_path} | {mod_time.strftime('%Y-%m-%d %H:%M')}")

def organize_files(rule="category"):
    folder = selected_folder.get()
    if not folder or not os.path.exists(folder):
        messagebox.showwarning("Warning", "Please select a valid folder first!")
        return

    selected_files = [file_selection[i] for i in preview_listbox.curselection()]
    if not selected_files:
        messagebox.showinfo("Info", "No files selected for organizing!")
        return

    total_files = len(selected_files)
    moved_count = 0
    moved_files = {}

    for idx, file_path in enumerate(selected_files, 1):
        ext = os.path.splitext(file_path)[1].lower()
        target_dir = folder

        # Determine folder based on rule
        if rule == "category":
            for category, extensions in TYPES.items():
                if ext in extensions:
                    target_dir = os.path.join(folder, category)
                    break
        elif rule == "date":
            date_folder = datetime.datetime.fromtimestamp(os.path.getmtime(file_path)).strftime("%Y-%m-%d")
            target_dir = os.path.join(folder, date_folder)
        elif rule == "size":
            size = os.path.getsize(file_path)
            if size < 1024*1024:
                size_folder = "Small (<1MB)"
            elif size < 10*1024*1024:
                size_folder = "Medium (1-10MB)"
            else:
                size_folder = "Large (>10MB)"
            target_dir = os.path.join(folder, size_folder)

        os.makedirs(target_dir, exist_ok=True)
        target_path = os.path.join(target_dir, os.path.basename(file_path))

        if os.path.exists(target_path):
            base, extn = os.path.splitext(os.path.basename(file_path))
            i = 1
            while os.path.exists(os.path.join(target_dir, f"{base}_{i}{extn}")):
                i += 1
            target_path = os.path.join(target_dir, f"{base}_{i}{extn}")

        try:
            shutil.move(file_path, target_path)
            moved_files[file_path] = target_path
            moved_count += 1
            # Log move
            with open(LOG_FILE, "a") as f:
                f.write(f"{datetime.datetime.now()} | {file_path} -> {target_path}\n")
        except Exception as e:
            print(f"Error moving {file_path}: {e}")

        progress_var.set((idx / total_files) * 100)
        root.update_idletasks()

    if moved_files:
        undo_history.append(moved_files)
    status_var.set(f"Moved {moved_count} files using '{rule}' rule")
    preview_files(folder)

def undo_move():
    if not undo_history:
        messagebox.showinfo("Undo", "Nothing to undo!")
        return
    last_move = undo_history.pop()
    for orig, dest in last_move.items():
        if os.path.exists(dest):
            os.makedirs(os.path.dirname(orig), exist_ok=True)
            try:
                shutil.move(dest, orig)
                with open(LOG_FILE, "a") as f:
                    f.write(f"{datetime.datetime.now()} | Undo: {dest} -> {orig}\n")
            except Exception as e:
                print(f"Undo error: {e}")
    status_var.set("Undo completed!")
    preview_files(selected_folder.get())

# --------------------------
# GUI Elements
# --------------------------
tk.Label(root, textvariable=status_var, bg=THEMES[current_theme]["bg"],
         fg=THEMES[current_theme]["fg"], font=("Arial", 16, "bold")).pack(pady=5)
ttk.Progressbar(root, maximum=100, variable=progress_var).pack(fill="x", padx=20, pady=5)

folder_label = tk.Label(root, textvariable=selected_folder, bg=THEMES[current_theme]["entry_bg"],
                        fg=THEMES[current_theme]["fg"], font=("Arial", 12), width=80, height=2)
folder_label.pack(pady=5)
folder_label.bind("<Button-1>", lambda e: select_folder())

frame = tk.Frame(root, bg=THEMES[current_theme]["bg"])
frame.pack(pady=5)

tk.Label(frame, text="Categories & Extensions:", bg=THEMES[current_theme]["bg"], fg=THEMES[current_theme]["fg"]).pack()
category_listbox = tk.Listbox(frame, width=70, height=6)
category_listbox.pack(pady=5)
update_category_list()

btn_frame = tk.Frame(frame, bg=THEMES[current_theme]["bg"])
btn_frame.pack(pady=5)
tk.Button(btn_frame, text="Add Category", command=add_category, bg="#F39c12", fg="white").grid(row=0, column=0, padx=5)
tk.Button(btn_frame, text="Add Extension", command=add_extension, bg="#F39c12", fg="white").grid(row=0, column=1, padx=5)
tk.Button(btn_frame, text="Undo", command=undo_move, bg="#E74C3C", fg="white").grid(row=0, column=2, padx=5)
tk.Button(btn_frame, text="Toggle Theme", command=toggle_theme, bg="#3498DB", fg="white").grid(row=0, column=3, padx=5)

tk.Label(root, text="File Preview & Select for Move:", bg=THEMES[current_theme]["bg"], fg=THEMES[current_theme]["fg"]).pack(pady=5)
preview_listbox = tk.Listbox(root, selectmode=tk.MULTIPLE, width=100, height=15)
preview_listbox.pack(pady=5)

# Organize buttons with rules
rule_frame = tk.Frame(root, bg=THEMES[current_theme]["bg"])
rule_frame.pack(pady=5)
tk.Button(rule_frame, text="Organize by Category", command=lambda: organize_files("category"), bg="#27AE60", fg="white").grid(row=0, column=0, padx=5)
tk.Button(rule_frame, text="Organize by Date", command=lambda: organize_files("date"), bg="#2980B9", fg="white").grid(row=0, column=1, padx=5)
tk.Button(rule_frame, text="Organize by Size", command=lambda: organize_files("size"), bg="#8E44AD", fg="white").grid(row=0, column=2, padx=5)

tk.Label(root, text="Drag-and-drop folder OR click label to select. Logs saved in 'file_organizer_log.txt'", bg=THEMES[current_theme]["bg"], fg="#555").pack(side="bottom", pady=5)

root.mainloop()
