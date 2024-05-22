import sys
from ipc.ipc import IPCServer
from pathlib import Path
import subprocess
import os
import json
import atexit

CLANG14 = "/usr/bin/clang++"
GCC11_4 = "/usr/bin/g++"
AIRO = "/home/cristi/Desktop/uni/licenta/llvm-AIRO/build/llvm/bin/clang++"

CFLAGS = ["-O2"]

class Compiler:
    def __init__(self, path):
        self.path = Path(path)

    def compile(self, file):
        exe = os.path.splitext(file)[0]
        cmd = [str(self.path), file, *CFLAGS, "-o", exe]
        
        try:
            result = subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            return exe
        except subprocess.CalledProcessError as e:
            raise Exception(f"Compilation failed with error: {e.stderr}")

class AIROCompiler(Compiler):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(AIROCompiler, cls).__new__(cls)
        return cls._instance

    def __init__(self, path):
        if hasattr(self, 'initialized') and self.initialized:
            return
        super().__init__(path)
        self.initialized = True
        self.ipc_server = IPCServer('/tmp/decision-maker', self.handle_request)
        print("Constructor")
        self.ipc_server.start()

    def handle_request(self, message_dict):
        # print(f"AIROCompiler handling request: {message_dict}")
        return "2"
    
    def stop(self):
        if hasattr(self, 'ipc_server'):
            self.ipc_server.stop()

