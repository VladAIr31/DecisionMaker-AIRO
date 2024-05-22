from pathlib import Path
import subprocess
import os

CLANG14 = "/usr/bin/clang++"
GCC11_4 = "/usr/bin/g++"
AIRO = "/home/cristi/Desktop/uni/licenta/llvm-AIRO/build/llvm/bin/clang"

CFLAGS = ""

class Compiler:
    def __init__(self, path):
        self.path = Path(path)

    def compile(self, file):
        exe = os.path.splitext(file)[0]
        cmd = [str(self.path), file, "-o", exe]
        
        try:
            result = subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            return exe
        except subprocess.CalledProcessError as e:
            raise Exception(f"Compilation failed with error: {e.stderr}")
        
        
AiroCompiler = Compiler(AIRO)
ClangCompiler = Compiler(CLANG14)
GCCCompiler = Compiler(GCC11_4)
