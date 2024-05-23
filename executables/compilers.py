import sys
from ipc.ipc import IPCServer
from RL.model import compiler_hook
from pathlib import Path
import subprocess
import os
import json
import atexit

CLANG14 = "/usr/bin/clang++"
GCC11_4 = "/usr/bin/g++"
AIRO = "/home/cristi/Desktop/uni/licenta/llvm-AIRO/build/llvm/bin/clang++"

CFLAGS_DEFAULT = ["-O2"]

class Compiler:
    def __init__(self, path, flags=CFLAGS_DEFAULT):
        self.path = Path(path)
        self.flags = flags

    def compile(self, file):
        exe = os.path.splitext(file)[0]
        cmd = [str(self.path), file, *self.flags, "-o", exe]
        
        try:
            result = subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            return exe
        except subprocess.CalledProcessError as e:
            raise Exception(f"Compilation failed with error: {e.stderr}")

class AIROCompiler(Compiler):
    def __init__(self, path,flags = CFLAGS_DEFAULT):
        if hasattr(self, 'initialized') and self.initialized:
            return
        super().__init__(path,flags)
        self.initialized = True
        self.ipc_server = IPCServer('/tmp/decision-maker', self.handle_request)
        self.ipc_server.start()

    def handle_request(self, message_dict):
        compiler_hook(message_dict)
        return "2"
    
    def stop(self):
        if hasattr(self, 'ipc_server'):
            self.ipc_server.stop()

