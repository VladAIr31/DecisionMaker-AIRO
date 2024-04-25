from pathlib import Path
import os

CLANG14 = "/usr/bin/clang++"
GCC11_4 = "/usr/bin/g++"
AIRO = "/home/cristi/Desktop/uni/licenta/llvm-AIRO/build/llvm/bin/clang"

CFLAGS = "-O2"

class Compiler:
    def __init__(self,path):
        self.path = Path(path)

    def compile(self,file):
        exe = os.path.splitext(file)[0]
        cmd = f"{self.path} {CFLAGS} {file} -o {exe}"
        os.system(cmd)
        return exe
        
        
AiroCompiler = Compiler(AIRO)
ClangCompiler = Compiler(CLANG14)
GCCCompiler = Compiler(GCC11_4)
