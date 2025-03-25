import os
import tkinter as tk
from tkinter import ttk, filedialog
from datetime import datetime
import subprocess

def get_subfolders(path):
    subfolders = [f for f in os.listdir(path) if os.path.isdir(os.path.join(path, f))]
    return subfolders

def get_folder_info(path):
    creation_time = os.path.getctime(path)
    modification_time = os.path.getmtime(path)
    return creation_time, modification_time

def format_date(timestamp):
    date = datetime.fromtimestamp(timestamp)
    formatted_date = date.strftime("%Y-%m-%d %H:%M:%S")
    return formatted_date

def update_folder_list():
    main_path = path_entry.get()
    subfolders = get_subfolders(main_path)
    folder_table.delete(*folder_table.get_children())
    for folder in subfolders:
        folder_path = os.path.join(main_path, folder)
        creation_time, modification_time = get_folder_info(folder_path)
        formatted_creation_time = format_date(creation_time)
        formatted_modification_time = format_date(modification_time)
        folder_table.insert("", tk.END, values=(folder, formatted_creation_time, formatted_modification_time))
    
    # Calculate the number of items in the treeview
    item_count = len(subfolders)
    
    # Set the maximum height for the table to show 10 items or fewer if there are fewer items
    max_table_height = min(10 * 20 + 40, item_count * 20 + 40)
    
    # Update the table height dynamically
    folder_table.configure(height=max_table_height)
    
    # Show/hide the scrollbar based on the number of items
    if item_count > 10:
        scrollbar.pack(side="right", fill="y")
        folder_table.configure(yscrollcommand=scrollbar.set)
    else:
        scrollbar.pack_forget()
        folder_table.configure(yscrollcommand=None)

def browse_path():
    selected_path = filedialog.askdirectory()
    if selected_path:
        path_entry.delete(0, tk.END)
        path_entry.insert(tk.END, selected_path)
        update_folder_list()

def open_folder(event):
    item = folder_table.selection()
    if item:
        selected_folder = folder_table.item(item)["values"][0]
        main_path = path_entry.get()
        folder_path = os.path.join(main_path, selected_folder)

        if os.name == "nt":  # Check if running on Windows
            subprocess.Popen(["cmd", "/c", "code", folder_path])
        else:  # Assuming running on macOS or Linux
            subprocess.Popen(["code", folder_path])

# Calculate the window dimensions with a 16:9 aspect ratio
width = 1024
height = int(width * 9 / 16)

# Create the main window with the specified dimensions
window = tk.Tk()
window.title("Sci-Fi Futuristic Interface")
window.geometry(f"{width}x{height}")

# Create a custom style for the interface
style = ttk.Style(window)
style.configure("Futuristic.TFrame", background="#20232d")
style.configure("Futuristic.TLabel", foreground="#ffffff", background="#20232d", font=("Arial", 12, "bold"))
style.configure("Futuristic.Treeview.Heading", foreground="#ffffff", background="#20232d", font=("Arial", 12, "bold"))
style.configure("Futuristic.Treeview", foreground="#ffffff", background="#20232d", fieldbackground="#20232d", font=("Arial", 11))
style.map("Futuristic.Treeview", background=[("selected", "#3498db")])

# Create a frame for the input section
input_frame = ttk.Frame(window, style="Futuristic.TFrame")
input_frame.pack(padx=10, pady=10, anchor="w")

# Create a label for the input path
path_label = ttk.Label(input_frame, text="Main Path:", style="Futuristic.TLabel")
path_label.grid(row=0, column=0, sticky="w")

# Create an entry field for the path
path_entry = ttk.Entry(input_frame, width=50, font=("Arial", 11))
path_entry.grid(row=0, column=1, sticky="w")

# Create a button to browse for the main path
browse_button = ttk.Button(input_frame, text="Browse", command=browse_path)
browse_button.grid(row=0, column=2, padx=(10, 0), sticky="w")

# Create a frame for the list section
list_frame = ttk.Frame(window, style="Futuristic.TFrame")
list_frame.pack(padx=10, pady=10, anchor="w")

# Create a label for the list
list_label = ttk.Label(list_frame, text="Subfolders:", style="Futuristic.TLabel")
list_label.pack(side="top", anchor="w")

# Create a treeview table to display the subfolders
folder_table = ttk.Treeview(list_frame, columns=("Name", "Creation Date", "Last Modified Date"), show="headings", style="Futuristic.Treeview")
folder_table.heading("Name", text="Name", anchor="w")
folder_table.heading("Creation Date", text="Creation Date", anchor="w")
folder_table.heading("Last Modified Date", text="Last Modified Date", anchor="w")
folder_table.pack(side="left", fill="both", expand=True)

# Create a scrollbar for the treeview
scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=folder_table.yview)

# Bind double-click event to open selected folder
folder_table.bind("<Double-1>", open_folder)

# Create a button to update the folder list
update_button = ttk.Button(window, text="Update", command=update_folder_list, style="Futuristic.TButton")
update_button.pack(padx=10, pady=10, anchor="w")

# Run the GUI event loop
window.mainloop()
