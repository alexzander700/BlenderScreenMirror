import time
import threading
import tkinter as tk
from tkinter import simpledialog, messagebox
import screeninfo
import mss
from PIL import Image
import traceback

# Global control variables
running = True
interval = 5  # default interval

# Function to get all monitor screen coordinates
def get_all_monitors():
    monitors = screeninfo.get_monitors()
    if not monitors:
        raise Exception("No monitors detected")
    monitors.sort(key=lambda m: m.x)
    return monitors

# Function to take screenshots with auto-restart on error
def take_screenshots():
    global running, interval
    while running:
        try:
            all_monitors = get_all_monitors()
            with mss.mss() as sct:
                while running:
                    for idx, monitor in enumerate(all_monitors):
                        region = {
                            "top": monitor.y,
                            "left": monitor.x,
                            "width": monitor.width,
                            "height": monitor.height
                        }
                        screenshot = sct.grab(region)

                        try:
                            Image.frombytes('RGB', screenshot.size, screenshot.rgb).save(f"monitor_{idx}.png")
                        except Exception as file_error:
                            print(f"Error saving image file for monitor {idx}:", file_error)

                    time.sleep(interval)
        except Exception as e:
            print("Error occurred in screenshot loop. Restarting...")
            traceback.print_exc()
            time.sleep(1)

# Function to start screenshotting in a thread
def start_screenshotting():
    thread = threading.Thread(target=take_screenshots, daemon=True)
    thread.start()

# Function to stop screenshotting
def stop():
    global running
    running = False
    root.destroy()

# Function to update interval
def update_interval():
    global interval
    try:
        new_interval = int(interval_entry.get())
        if new_interval >= 1:
            interval = new_interval
    except ValueError:
        pass  # Ignore invalid entries

# GUI setup
root = tk.Tk()
root.title("Screenshot Controller")

tk.Label(root, text="Interval (seconds):").pack(pady=5)
interval_entry = tk.Entry(root)
interval_entry.insert(0, str(interval))
interval_entry.pack()

tk.Button(root, text="Update Interval", command=update_interval).pack(pady=5)
tk.Button(root, text="Stop", command=stop).pack(pady=5)

start_screenshotting()
root.mainloop()
