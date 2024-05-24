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

    def handle_client(self, client_pipe):
        def response_fn(response):
            nonlocal client_pipe
            with open(client_pipe + "_in", 'w') as f_w:
                f_w.write(str(response))
        try:
            with open(client_pipe + "_out", 'r') as f:
                while True:
                    line = f.readline().strip()
                    if line == "END":
                        response_fn(0)
                        break
                    if line:
                        message_dict = json.loads(line)
                        self.request_handler(message_dict, response_fn)
        except Exception as e:
            print(f"Error handling client pipe {client_pipe}: {e}")

    def server_loop(self):
        with open(self.server_pipe, 'r') as f:
            os.set_blocking(f.fileno(), False)  # Set to non-blocking mode
            while not self.shutdown_flag:
                ready, _, _ = select.select([f], [], [], 1.0)  # 1.0-second timeout
                if ready:
                    line = f.readline().strip()
                    if line:
                        parts = line.split(' ', 1)
                        if len(parts) == 2:
                            _, client_pipe = parts
                            thread = threading.Thread(target=self.handle_client, args=(client_pipe,))
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


def default_request_handler(message_dict, response_fn):
    response_fn(1)

if __name__ == "__main__":
    server_pipe = "/tmp/airo/decision-maker"
    server = IPCServer(server_pipe, default_request_handler)
    server.start()

    try:
        while True:
            pass  # Keep the main thread alive
    except KeyboardInterrupt:
        server.stop()
        print("Server stopped.")

