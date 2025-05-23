import bpy

def reload_images():
    for image_name in ["monitor_0.png", "monitor_1.png"]: # CHANGE THIS TO HOWEVER MANY MONITORS YOU HAVE
        img = bpy.data.images.get(image_name)
        if img:
            print(f"Reloading {image_name}")
            img.reload()
        else:
            print(f"Image not found in bpy.data.images: {image_name}")

# Define a timer handler
def refresh_timer():
    reload_images()
    return 2.0  # Repeat every 2 seconds

# Remove existing handler to avoid duplicates
try:
    bpy.app.timers.unregister(refresh_timer)
except ValueError:
    pass  # It wasn't registered yet

# Register the timer
bpy.app.timers.register(refresh_timer)

print("Image auto-refresh script loaded.")
