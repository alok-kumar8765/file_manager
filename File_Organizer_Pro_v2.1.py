# ==========================
# File Organizer Pro v2.1
# ==========================

import tkinter as tk
from tkinter import filedialog, ttk, simpledialog, messagebox
import os, shutil

# --------------------------
# GUI Setup
# --------------------------
root = tk.Tk()
root.title("File Organizer Pro v2.1")
root.geometry("700x600")
root.configure(bg="#111")

status_var = tk.StringVar(value="Ready to Organize")
tk.Label(root, textvariable=status_var,
         bg="#222", fg="#0ff",
         font=("Arial", 16, "bold"), height=2).pack(fill="x", padx=10, pady=10)

progress_var = tk.DoubleVar(value=0)
progress_bar = ttk.Progressbar(root, maximum=100, variable=progress_var)
progress_bar.pack(fill="x", padx=20, pady=10)

# --------------------------
# Default File Type Categories
# --------------------------
TYPES = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".tiff", ".bmp"],
    "Docs": [".pdf", ".docx", ".txt", ".pages", ".xlsx", ".pptx"],
    "Videos": [".mp4", ".mov", ".avi", ".flv", ".mkv"],
    "Audio": [".mp3", ".wav", ".aac"],
    "Code": [".py", ".md", ".html", ".js", ".css", ".java"]
}

# Undo history for multi-level undo
undo_history = []

# Selected folder
selected_folder = tk.StringVar(value="Drop folder here or click to select")

# Files selected for moving
file_selection = []

# --------------------------
# Functions
# --------------------------
def add_category():
    name = simpledialog.askstring("New Category", "Enter category name:")
    if not name: return
    if name in TYPES:
        messagebox.showinfo("Info", "Category already exists!")
        return
    TYPES[name] = []
    update_category_list()
    
def add_extension():
    cat = category_listbox.get(tk.ACTIVE)
    if not cat: return
    cat_name = cat.split(":")[0]
    ext = simpledialog.askstring("New Extension", f"Enter extension for {cat_name} (with dot):")
    if not ext or not ext.startswith("."): return
    if ext in TYPES[cat_name]:
        messagebox.showinfo("Info", "Extension already exists!")
        return
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

def preview_files(folder):
    global file_selection
    file_selection = []
    preview_listbox.delete(0, tk.END)
    
    for root_dir, _, files in os.walk(folder):
        for file in files:
            file_path = os.path.join(root_dir, file)
            file_selection.append(file_path)
            preview_listbox.insert(tk.END, file_path)

def organize_files():
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
        for category, extensions in TYPES.items():
            if ext in extensions:
                target_dir = os.path.join(folder, category)
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
                except Exception as e:
                    print(f"Error moving {file_path}: {e}")
                break

        progress_var.set((idx / total_files) * 100)
        root.update_idletasks()

    if moved_files:
        undo_history.append(moved_files)
    status_var.set(f"Moved {moved_count} files out of {total_files}")
    preview_files(folder)  # refresh preview after moving

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
            except Exception as e:
                print(f"Undo error: {e}")
    status_var.set("Undo completed!")
    preview_files(selected_folder.get())

# Drag-and-drop folder
def drop_folder(event):
    path = root.tk.splitlist(event.data)[0]
    if os.path.isdir(path):
        selected_folder.set(path)
        preview_files(path)

# --------------------------
# GUI Elements
# --------------------------
top_frame = tk.Frame(root, bg="#111")
top_frame.pack(pady=5)

folder_label = tk.Label(top_frame, textvariable=selected_folder,
                        bg="#333", fg="#0ff", font=("Arial", 12), width=70, height=2)
folder_label.pack(pady=5)
folder_label.bind("<Button-1>", lambda e: select_folder())

# Enable drag-and-drop (Windows)
try:
    import tkinterdnd2 as tkdnd
    dnd = tkdnd.TkinterDnD.Tk()
    folder_label.drop_target_register(tkdnd.DND_FILES)
    folder_label.dnd_bind('<<Drop>>', drop_folder)
except:
    pass  # fallback if tkinterdnd2 not installed

# Categories listbox
frame = tk.Frame(root, bg="#111")
frame.pack(pady=5)

tk.Label(frame, text="Categories & Extensions:", bg="#111", fg="#0ff").pack()
category_listbox = tk.Listbox(frame, width=60, height=8)
category_listbox.pack(pady=5)
update_category_list()

btn_frame = tk.Frame(frame, bg="#111")
btn_frame.pack(pady=5)
tk.Button(btn_frame, text="Add Category", command=add_category, bg="#F39c12", fg="white").grid(row=0, column=0, padx=5)
tk.Button(btn_frame, text="Add Extension", command=add_extension, bg="#F39c12", fg="white").grid(row=0, column=1, padx=5)
tk.Button(btn_frame, text="Undo Last Move", command=undo_move, bg="#E74C3C", fg="white").grid(row=0, column=2, padx=5)

# File preview and selective move
tk.Label(root, text="File Preview & Select for Move:", bg="#111", fg="#0ff").pack(pady=5)
preview_listbox = tk.Listbox(root, selectmode=tk.MULTIPLE, width=100, height=15)
preview_listbox.pack(pady=5)

sort_btn = tk.Button(root, text="Organize Selected Files", command=organize_files, bg="#27AE60", fg="white", font=("Arial", 14))
sort_btn.pack(pady=10)

tk.Label(root, text="Drag-and-drop folder OR click folder label to select.\nMulti-level undo supported.", bg="#111", fg="#555").pack(side="bottom", pady=10)

root.mainloop()
