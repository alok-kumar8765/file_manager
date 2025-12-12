# ======================
# Enhanced File Organizer
# ======================

import tkinter as tk
from tkinter import filedialog, ttk
import os, shutil

# --------------------------
# GUI Setup
# --------------------------
root = tk.Tk()
root.title("File Organizer")
root.geometry("500x350")
root.configure(bg="#000")

status_var = tk.StringVar(value="Ready to Organize")

tk.Label(
    root, textvariable=status_var,
    bg="#111", fg="#0ff",
    font=("Arial", 16, "bold"),
    height=2
).pack(fill="x", padx=10, pady=10)

progress_var = tk.DoubleVar(value=0)
progress_bar = ttk.Progressbar(root, maximum=100, variable=progress_var)
progress_bar.pack(fill="x", padx=20, pady=10)

# --------------------------
# File Type Categories
# --------------------------
TYPES = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".tiff", ".bmp"],
    "Docs": [".pdf", ".docx", ".txt", ".pages", ".xlsx", ".pptx"],
    "Videos": [".mp4", ".mov", ".avi", ".flv", ".mkv"],
    "Audio": [".mp3", ".wav", ".aac"],
    "Code": [".py", ".md", ".html", ".js", ".css", ".java"]
}

# --------------------------
# Organize Files Function
# --------------------------
def organize_files(event):
    folder = filedialog.askdirectory()
    if not folder:
        return

    # Gather all files recursively
    file_list = []
    for root_dir, _, files in os.walk(folder):
        for file in files:
            file_list.append(os.path.join(root_dir, file))

    total_files = len(file_list)
    moved_count = 0

    for idx, file_path in enumerate(file_list, 1):
        ext = os.path.splitext(file_path)[1].lower()
        moved = False

        for category, extensions in TYPES.items():
            if ext in extensions:
                target_dir = os.path.join(folder, category)
                os.makedirs(target_dir, exist_ok=True)

                target_path = os.path.join(target_dir, os.path.basename(file_path))
                # Avoid overwriting
                if os.path.exists(target_path):
                    base, extn = os.path.splitext(os.path.basename(file_path))
                    i = 1
                    while os.path.exists(os.path.join(target_dir, f"{base}_{i}{extn}")):
                        i += 1
                    target_path = os.path.join(target_dir, f"{base}_{i}{extn}")

                try:
                    shutil.move(file_path, target_path)
                    moved_count += 1
                    moved = True
                except Exception as e:
                    print(f"Error moving {file_path}: {e}")
                break

        # Update progress bar
        progress_var.set((idx / total_files) * 100)
        root.update_idletasks()

    status_var.set(f"Moved {moved_count} files out of {total_files}")

# --------------------------
# GUI Button
# --------------------------
frame = tk.Frame(root, bg="#000")
frame.pack(pady=20)

btn_widget = tk.Label(
    frame, text="Select Folder",
    font=("Arial", 14, "bold"),
    bg="#F39c12", fg="white",
    relief="flat", padx=20, pady=10
)
btn_widget.bind("<Button-1>", organize_files)
btn_widget.pack()

tk.Label(
    root, text="Sorts: Images, Docs, Videos, Audio, Code",
    bg="#000", fg="#555",
    font=("Arial", 10)
).pack(side="bottom", pady=10)

root.mainloop()
