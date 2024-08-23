import socket
import os

save_directory = "C:/Users/sudhi/Downloads/keys"  # Replace with the desired directory path

def ensure_directory_exists(directory):
    """Ensure that the save directory exists."""
    if not os.path.exists(directory):
        os.makedirs(directory)

def save_log_file(data, file_index):
    """Save the received log data to a file in the save directory."""
    file_path = os.path.join(save_directory, f"log_{file_index}.txt")
    with open(file_path, 'wb') as log_file:
        log_file.write(data)

def start_server():
    # Ensure the save directory exists
    ensure_directory_exists(save_directory)
    
    # Server setup
    host = '0.0.0.0'  # Listen on all network interfaces
    port = 9999        # Port on which the server is listening
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((host, port))
        server_socket.listen(1)
        print(f"Server is listening on {host}:{port}...")
        
        file_index = 1  # Index for naming log files
        
        while True:
            conn, addr = server_socket.accept()
            print(f"Connected by {addr}")
            
            with conn:
                data = b""
                while True:
                    chunk = conn.recv(1024)
                    if not chunk:
                        break
                    data += chunk
                
                if data:
                    print(f"Received log data, saving to file...")
                    save_log_file(data, file_index)
                    file_index += 1

if __name__ == "__main__":
    start_server()
