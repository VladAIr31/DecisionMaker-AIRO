import sys
sys.path.append('./dataset')
sys.path.append('./executables')
from compilers import Compiler
from dataset.package import Package
import subprocess
from pathlib import Path
import os
import mmap
import time
import numpy as np
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
        total_cpu_cycles = 0

        for input_file in self.pack.tests():
            perf_command = f"perf stat -e cpu-cycles {self.exe} < {input_file}"
            
            proc = subprocess.run(perf_command, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, text=True)
            
            stderr = proc.stderr
            cpu_cycles = 0

            for line in stderr.split('\n'):
                cpu_cycles_match = re.search(r'(\d+)\s+cpu-cycles', line.replace('.', ''))
                if cpu_cycles_match:
                    cpu_cycles = int(cpu_cycles_match.group(1))

            total_cpu_cycles += cpu_cycles
            cnt += 1

        if cnt == 0:
            return None

        avg_cpu_cycles = total_cpu_cycles / cnt

        return avg_cpu_cycles

    def benchmark(self, time_limit, outlier_threshold=1):
        start_time = time.time()
        runs = []

        while (time.time() - start_time) < time_limit:
            result = self.run_tests()
            
            if result is not None:
                runs.append(result)

        if not runs:
            return None

        runs = np.array(runs)

        mean = np.mean(runs)
        std_dev = np.std(runs)

        filtered_runs = runs[(runs >= mean - outlier_threshold * std_dev) & (runs <= mean + outlier_threshold * std_dev)]
        # print(f"Ran {len(runs)}, dropped{len(runs) - len(filtered_runs)}")

        if len(filtered_runs) == 0:
            return None

        filtered_mean = np.mean(filtered_runs)
        return filtered_mean
