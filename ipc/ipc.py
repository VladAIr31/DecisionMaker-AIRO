import os
import select
import threading
import time
import json

server_pipe = '/tmp/decision-maker'

# Ensure the pipe exists
if not os.path.exists(server_pipe):
    os.mkfifo(server_pipe)

shutdown_flag = False
threads = []

def handle_client(client_pipe, message):
    message_dict = json.loads(message)
    print(f"Handling client: {client_pipe}")
    print(f"Loop is \n{message_dict}")
    response = "5"  # hardcoded value
    with open(client_pipe, 'w') as f:
        f.write(response)

def server_loop():
    global shutdown_flag
    with open(server_pipe, 'r') as f:
        os.set_blocking(f.fileno(), False)  # Set to non-blocking mode
        while not shutdown_flag:
            ready, _, _ = select.select([f], [], [], 1.0)  # 1.0-second timeout
            if ready:
                line = f.readline().strip()
                if line:
                    parts = line.split(' ', 1)
                    if len(parts) == 2 and "client_pipe" in parts[0]:
                        client_pipe, message = parts
                        thread = threading.Thread(target=handle_client, args=(client_pipe, message))
                        thread.start()
                        threads.append(thread)
            else:
                print("Waiting for input...")

def start_server():
    global shutdown_flag
    print("Starting server...")
    server_thread = threading.Thread(target=server_loop)
    server_thread.start()

    try:
        while server_thread.is_alive():
            server_thread.join(timeout=1.0)
    except KeyboardInterrupt:
        print("Shutting down server...")
        shutdown_flag = True
        server_thread.join()

    # Join all client handler threads
    for thread in threads:
        thread.join()

if __name__ == '__main__':
    start_server()
