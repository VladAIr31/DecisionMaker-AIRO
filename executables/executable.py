import sys
sys.path.append('./dataset')
sys.path.append('./executables')
from compilers import Compiler
from dataset.package import Package
import subprocess
from pathlib import Path
import os
import re

class Executable:
    def __init__(self, pack: Package, compiler: Compiler):
        self.pack = pack
        self.compiler = compiler
    
    def build(self):
        try:
            self.exe = self.compiler.compile(self.pack.get_main())
            self.built = True
        except Exception as e:
            print(f"Failed to compile package {e}")
    
    def run_tests(self):
        if not hasattr(self, "built") or not self.built:
            raise Exception("Executable not built...")

        cnt = 0
        total_cpu_time = 0
        for input_file in self.pack.tests():
            perf_command = ["perf", "stat", "-e", "cpu-cycles,instructions", self.exe]
            
            if not Path('/tmp/airo').exists():
                os.mkdir('/tmp/airo')
            with open(input_file, 'r') as stdin, open('/tmp/airo/out', 'w') as stdout:
                proc = subprocess.Popen(perf_command, stdin=stdin, stdout=stdout, stderr=subprocess.PIPE, text=True)
                _, stderr = proc.communicate()
            cpu_cycles = instructions = 0

            for line in stderr.split('\n'):
                if "cpu-cycles" in line:
                    match = re.search(r'(\d+(?:\.\d+)*)\s+cpu-cycles', line)
                    if match:
                        cpu_cycles = int(match.group(1).replace(".", ""))
                elif "instructions" in line:
                    match = re.search(r'(\d+(?:\.\d+)*)\s+instructions', line)
                    if match:
                        instructions = int(match.group(1).replace(".", ""))

            total_cpu_time += cpu_cycles
            cnt += 1
        if cnt == 0:
            return None

        return total_cpu_time / cnt

    def benchmark(self, times, method="perf"):
        if method == "perf":
            runs = [self.run_tests() for _ in range(times)]
        elif method == "time":
            runs = [self.benchmark_with_time() for _ in range(times)]
        else:
            raise ValueError("Invalid benchmarking method specified.")

        if None in runs:
            return None
        
        mean = sum(runs) / len(runs)
        return mean

    def benchmark_with_time(self):
        if not hasattr(self, "built") or not self.built:
            raise Exception("Executable not built...")

        cnt = 0
        total_time = 0
        for input_file in self.pack.tests():
            time_command = ["/usr/bin/time", "-f", "%e", self.exe]

            if not Path('/tmp/airo').exists():
                os.mkdir('/tmp/airo')
            with open(input_file, 'r') as stdin, open('/tmp/airo/out', 'w') as stdout, open('/tmp/airo/time_output', 'w') as stderr:
                proc = subprocess.Popen(time_command, stdin=stdin, stdout=stdout, stderr=stderr, text=True)
                proc.communicate()

            with open('/tmp/airo/time_output', 'r') as f:
                elapsed_time = float(f.read().strip())

            total_time += elapsed_time
            cnt += 1
        if cnt == 0:
            return None

        return total_time / cnt