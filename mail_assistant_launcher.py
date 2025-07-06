import keyboard
from read_email import get_latest_email
from summarize_email import summarize_email
from speak import speak

import datetime

with open("launch_log.txt", "a") as f:
    f.write(f"[{datetime.datetime.now()}] Launcher script started.\n")


def trigger_assistant():
    subject, body = get_latest_email()
    if subject and body:
        summary = summarize_email(subject, body)
        speak(summary)

print("✅ Mail Assistant is running... Press Ctrl + Shift + M to activate.")

# Hotkey to trigger the assistant
keyboard.add_hotkey("ctrl+shift+m", trigger_assistant)

# Keep the script running
keyboard.wait("esc")  # Press ESC to stop the script
