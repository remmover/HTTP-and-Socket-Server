# HTTP and Socket Server

This program sets up an HTTP server and a socket server in Python. The HTTP server serves static files and handles GET and POST requests, while the socket server receives data from clients and stores it in a JSON file.

## Requirements
- Python 3.x
- Poetry

## Installation and Setup
1. Clone the repository or download the source code files.
2. Open a terminal or command prompt and navigate to the directory where the program files are located.
3. Run the following command to install the project dependencies using Poetry:
   ```
   poetry install
   ```

## Usage
1. Run the following command to start the HTTP server and the socket server:
   ```
   poetry run python main.py
   ```
   The HTTP server will start running on `http://localhost:3000`, and the socket server will run on `localhost:5000`.
2. Open a web browser and visit `http://localhost:3000` to access the web application.

## Functionality
The program consists of two main components: the HTTP server and the socket server.

### HTTP Server
The HTTP server handles GET and POST requests and serves static files.

- GET requests:
  - Requests to the root URL (`/`) will display the `index.html` file.
  - Requests to the `/message` URL will display the `message.html` file.
  - Requests to other valid static file paths will serve the corresponding file.

- POST requests:
  - When a POST request is made to the `/message` URL, the server receives the form data, extracts the key-value pairs, and stores them in a dictionary with the current timestamp as the key.
  - The server then sends the dictionary to the socket server using UDP.
  - After processing the data, the user is redirected to the root URL (`/`).

### Socket Server
The socket server receives data sent by the HTTP server, parses it as JSON, and stores it in a JSON file.

- The socket server listens on `localhost:5000` for incoming UDP data.
- The received data is decoded and parsed as a JSON object.
- The parsed data is merged with the existing data stored in the `storage/data.json` file.
- The updated data is then saved back to the JSON file.

## Configuration
- The HTTP server is set to run on `http://localhost:3000` by default. You can change the server address by modifying the `server_address` variable in the `run_http_server` function.
- The socket server is set to run on `localhost:5000` by default. You can change the server address by modifying the `server_address` variable in the `run_socket_server` function.
- The storage path for the JSON file is set to `storage/data.json` by default. You can modify the `file_path` variable in the `save_to_json_file` function to change the storage location.

## License
This program is licensed under the [MIT License](LICENSE).

## Acknowledgments
This program is inspired by the basic functionality of HTTP and socket servers in Python.
