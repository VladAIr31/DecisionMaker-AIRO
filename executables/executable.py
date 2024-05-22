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
    def __init__(self,pack: Package,compiler: Compiler):
        self.pack = pack
        self.compiler = compiler
    
    def build(self):
        try:
            self.exe = self.compiler.compile(self.pack.get_main())
            self.built = True
        except Exception as e:
            print(f"Failed to compile package {e}")
     
    def run_tests(self):
        if not self.built:
            raise Exception("Executable not built...")

        # print(f"Benchmarking {self.pack.get_problem()}")
        cnt = 0
        total_cpu_time = 0
        for input_file in self.pack.tests():
            # with open(output_file, 'r') as file:
            #     expected_output = file.read()

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

            # print(f"CPU Cycles for {input_file}: {cpu_cycles}")
            # print(f"Instructions for {input_file}: {instructions}")

            total_cpu_time += cpu_cycles
            cnt += 1
        if cnt == 0:
            return None

        return total_cpu_time / cnt

    def benchmark(self,times):
        runs = [self.run_tests() for _ in range(times)]
        if None in runs:
            return None
        
        mean = sum(runs) / len(runs)
    
        return mean