# Remote Command and File Transfer Server-Client

This project consists of a server-client architecture for remote command execution and file transfer. It allows a server to send commands to a client, execute them on the client machine, and transfer files between the server and client.

## Features

- **Remote Command Execution**: Execute shell commands on the client machine from the server.
- **File Upload and Download**: Transfer files between the server and client.
- **Keylogger**: Logs key presses on the client machine.

## Requirements

- Python 3.x
- `keyboard` library (for keylogging on the client side)

## Installation

1. **Clone the repository:**

    ```sh
    git clone https://github.com/Fukuiz/Keylogger.git
    cd Keylogger
    ```

2. **Install the `keyboard` library (only required on the client side):**

    ```sh
    pip install keyboard
    ```

## Configuration

1. **Server Configuration:**
   - Replace `YOUR IP` with the server's IP address.
   - Specify the directory path for saving downloaded files in the `download_file` function.

2. **Client Configuration:**
   - Replace `YOUR IP` with the server's IP address.

## Usage

1. **Run the Server:**

    ```sh
    python Server.py
    ```

2. **Run the Client:**

    ```sh
    python Client.py
    ```

## File Descriptions

- **Server.py**: The server script that listens for incoming connections, sends commands, and handles file uploads and downloads.
- **Client.py**: The client script that connects to the server, executes commands, and handles file uploads and downloads.

## Example Commands

- **Execute Command**: Type any shell command in the server terminal.
- **Change Directory**: `cd <directory-path>`
- **Clear Screen**: `clear`
- **Upload File**: `upload <file-path>`
- **Download File**: `download <file-name>`
- **Quit**: `quit`

## Keylogging

The client script includes a keylogger that logs all key presses to a file named `Keyfile.txt`.

## Disclaimer

This software is intended for educational purposes only. Use it responsibly and ensure you have permission to execute commands and transfer files on the target machine.


