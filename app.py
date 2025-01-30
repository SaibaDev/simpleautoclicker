#Autoclicker

#todo
#add custom time
#add option where users can choose the button to autoclick

import time
import threading
from pynput.mouse import Button, Controller
from pynput.keyboard import Listener, KeyCode
import tkinter as tk
from tkinter import messagebox

clicking = False
mouse = Controller()

START_HOTKEY = KeyCode(char='+')  
STOP_HOTKEY = KeyCode(char='-')  


def clicker():
    while True:
        if clicking:
            mouse.click(Button.left, 1)
        time.sleep(0.0001)

def start_clicking():
    global clicking
    clicking = True
    status_label.config(text="Status: Running")

def stop_clicking():
    global clicking
    clicking = False
    status_label.config(text="Status: Stopped")

def on_press(key):
    global START_HOTKEY, STOP_HOTKEY
    if key == START_HOTKEY:
        start_clicking()
    elif key == STOP_HOTKEY:
        stop_clicking()


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


def on_close():
    if messagebox.askokcancel("Quit", "Do you want to exit the autoclicker?"):
        global listener
        listener.stop() 
        root.destroy()
        exit(0)


def start_gui():
    global root, status_label, start_key_entry, stop_key_entry

    root = tk.Tk()
    root.title("Simple Autoclicker")
    root.geometry("400x300")
    root.protocol("WM_DELETE_WINDOW", on_close)

   
    title_label = tk.Label(root, text="Saiba'sAutoclicker", font=("Arial", 16))
    title_label.pack(pady=10)

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

    update_button = tk.Button(
        hotkey_frame, text="Update Hotkeys", command=update_hotkeys, font=("Arial", 12)
    )
    update_button.grid(row=2, columnspan=2, pady=10)

    status_label = tk.Label(root, text="Status: Stopped", font=("Arial", 12))
    status_label.pack(pady=10)

    quit_button = tk.Button(
        root, text="Exit", command=on_close, font=("Arial", 12), bg="red", fg="white"
    )
    quit_button.pack(pady=10)

    root.mainloop()

click_thread = threading.Thread(target=clicker, daemon=True)
click_thread.start()

listener = Listener(on_press=on_press)
listener.start()

start_gui()
