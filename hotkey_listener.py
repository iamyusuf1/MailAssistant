import keyboard
import subprocess
import os
import datetime
import ctypes
import sys

# ✅ Full path to your mail assistant script
assistant_path = r"D:\MailAssistant\mail_assistant_launcher.py"  # ⬅️ Replace with actual path if needed

# ✅ Notify user (one-time popup) that listener has started
def show_startup_message():
    ctypes.windll.user32.MessageBoxW(
        0,
        "📬 Mail Assistant is now running in background.\n\nPress Ctrl+Shift+M to hear your latest mail.",
        "Mail Assistant Activated",
        0x40
    )

# ✅ Function triggered when Ctrl+Shift+M is pressed
def run_mail_assistant():
    with open("log.txt", "a") as f:
        f.write(f"[{datetime.datetime.now()}] Ctrl+Shift+M pressed\n")
    
    # ✅ Launch the assistant script with correct working directory
    subprocess.Popen(
        ["python", assistant_path],
        cwd=os.path.dirname(assistant_path),
        creationflags=subprocess.CREATE_NO_WINDOW  # ✅ Hides terminal
    )

# ✅ Show startup message once (can remove if unnecessary)
show_startup_message()

# ✅ Register hotkeys
keyboard.add_hotkey('ctrl+shift+m', run_mail_assistant)
keyboard.add_hotkey('ctrl+shift+x', lambda: sys.exit())  # Optional: exit on Ctrl+Shift+X

# ✅ Wait infinitely until user exits with Ctrl+Shift+X
keyboard.wait()
