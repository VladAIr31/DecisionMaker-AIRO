import os
import select
import threading
import json

class IPCServer:
    def __init__(self, server_pipe, request_handler):
        self.server_pipe = server_pipe
        self.request_handler = request_handler
        self.shutdown_flag = False
        self.threads = []

        # Ensure the pipe exists
        if not os.path.exists(self.server_pipe):
            os.mkfifo(self.server_pipe)
        
        self.server_thread = None

    def handle_client(self, client_pipe, message):
        message_dict = json.loads(message)
        # print(f"Handling client: {client_pipe}")
        # print(f"Received message: \n{message_dict}")
        response = self.request_handler(message_dict)  # Use the provided callback
        with open(client_pipe, 'w') as f:
            f.write(response)

    def server_loop(self):
        with open(self.server_pipe, 'r') as f:
            os.set_blocking(f.fileno(), False)  # Set to non-blocking mode
            while not self.shutdown_flag:
                ready, _, _ = select.select([f], [], [], 1.0)  # 1.0-second timeout
                if ready:
                    line = f.readline().strip()
                    if line:
                        parts = line.split(' ', 1)
                        if len(parts) == 2 and "client_pipe" in parts[0]:
                            client_pipe, message = parts
                            thread = threading.Thread(target=self.handle_client, args=(client_pipe, message))
                            thread.start()
                            self.threads.append(thread)
                else:
                    print("Waiting for input...")

    def start(self):
        print("Starting server...")
        self.server_thread = threading.Thread(target=self.server_loop)
        self.server_thread.start()
        self.running = True
    def stop(self):
        if not self.running:
            return
        
        print("Shutting down server...")
        self.shutdown_flag = True
        if self.server_thread is not None:
            self.server_thread.join()

        # Join all client handler threads
        for thread in self.threads:
            thread.join()
        self.running = False
            
    def __del__(self):
        self.stop()

def default_request_handler(message_dict):
    return "1"
