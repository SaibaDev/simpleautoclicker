import time
import threading
from pynput.mouse import Button, Controller
from pynput.keyboard import Listener, KeyCode
import tkinter as tk
from tkinter import messagebox

# Global variables
clicking = False
mouse = Controller()

# Default hotkeys
START_HOTKEY = KeyCode(char='+')
STOP_HOTKEY = KeyCode(char='-')

# Function to handle the autoclicking
def clicker():
    while True:
        if clicking:
            mouse.click(Button.left, 1)
        time.sleep(0.0001)

# Function to start clicking
def start_clicking():
    global clicking
    clicking = True
    status_label.config(text="Status: Running")

# Function to stop clicking
def stop_clicking():
    global clicking
    clicking = False
    status_label.config(text="Status: Stopped")

# Function to handle key press events
def on_press(key):
    if key == START_HOTKEY:
        start_clicking()
    elif key == STOP_HOTKEY:
        stop_clicking()

# Function to update hotkeys
def update_hotkeys():
    global START_HOTKEY, STOP_HOTKEY
    start_key = start_key_entry.get().lower()
    stop_key = stop_key_entry.get().lower()

    if len(start_key) == 1 and len(stop_key) == 1:
        START_HOTKEY = KeyCode(char=start_key)
        STOP_HOTKEY = KeyCode(char=stop_key)
        messagebox.showinfo("Success", f"Hotkeys updated!\nStart: {start_key.upper()}, Stop: {stop_key.upper()}")
    else:
        messagebox.showerror("Error", "Please enter single-character keys for both hotkeys!")

# Function to handle window close event
def on_close():
    if messagebox.askokcancel("Quit", "Do you want to exit the autoclicker?"):
        listener.stop()
        root.destroy()
        exit(0)

# Time set function
def time_set():
    try:
        hours = int(entry1.get())
        minutes = int(entry2.get())
        seconds = int(entry3.get())
        milliseconds = int(entry4.get())
        
        total_time = hours * 3600 + minutes * 60 + seconds + milliseconds / 1000
        messagebox.showinfo("Time Set", f"Time set to {hours}h {minutes}m {seconds}s {milliseconds}ms")
        # You can use total_time to set a delay or other time-related functionality
    except ValueError:
        messagebox.showerror("Error", "Please enter valid numbers for time!")

# Function to start the GUI
def start_gui():
    global root, status_label, start_key_entry, stop_key_entry, entry1, entry2, entry3, entry4

    root = tk.Tk()
    root.title("Saiba's Simple Autoclicker")
    root.geometry("500x200")
    root.protocol("WM_DELETE_WINDOW", on_close)

    # Title label
    title_label = tk.Label(root, text="Saiba's Simple AutoClicker", font=("Arial", 16))
    title_label.pack(pady=10)

    # Entry boxes in a single line
    entry_frame = tk.Frame(root)
    entry_frame.pack(pady=10)

    entry1 = tk.Entry(entry_frame, width=10)
    entry1.grid(row=0, column=0, padx=5)

    entry2 = tk.Entry(entry_frame, width=10)
    entry2.grid(row=0, column=1, padx=5)

    entry3 = tk.Entry(entry_frame, width=10)
    entry3.grid(row=0, column=2, padx=5)

    entry4 = tk.Entry(entry_frame, width=10)
    entry4.grid(row=0, column=3, padx=5)

    set_button = tk.Button(entry_frame, text="Set Time", command=time_set)
    set_button.grid(row=0, column=4, padx=5)

    # Hotkey frame
    hotkey_frame = tk.Frame(root)
    hotkey_frame.pack(pady=10)

    start_key_label = tk.Label(hotkey_frame, text="Start Hotkey:", font=("Arial", 12))
    start_key_label.grid(row=0, column=0, padx=5)
    start_key_entry = tk.Entry(hotkey_frame, font=("Arial", 12), width=5)
    start_key_entry.grid(row=0, column=1, padx=5)
    start_key_entry.insert(0, "+")

    stop_key_label = tk.Label(hotkey_frame, text="Stop Hotkey:", font=("Arial", 12))
    stop_key_label.grid(row=1, column=0, padx=5)
    stop_key_entry = tk.Entry(hotkey_frame, font=("Arial", 12), width=5)
    stop_key_entry.grid(row=1, column=1, padx=5)
    stop_key_entry.insert(0, "-")

    update_button = tk.Button(hotkey_frame, text="Update Hotkeys", command=update_hotkeys, font=("Arial", 12))
    update_button.grid(row=2, columnspan=2, pady=10)

    # Status label
    status_label = tk.Label(root, text="Status: Stopped", font=("Arial", 12))
    status_label.pack(pady=10)

    # Exit button
    quit_button = tk.Button(root, text="Exit", command=on_close, font=("Arial", 12), bg="red", fg="white")
    quit_button.pack(pady=10)

    root.mainloop()

# Start the autoclicker thread
click_thread = threading.Thread(target=clicker, daemon=True)
click_thread.start()

# Start the keyboard listener
listener = Listener(on_press=on_press)
listener.start()

# Start the GUI
start_gui()