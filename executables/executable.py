import sys
sys.path.append('./scrapper')
sys.path.append('./executables')
import data_builder
import compilers
import subprocess
import re

class Executable:
    def __init__(self,pack: data_builder.Package,compiler: compilers.Compiler):
        self.pack = pack
        self.compiler = compiler
    
    def build(self):
        try:
            self.exe = self.compiler.compile(self.pack.get_main())
        except:
            print("Failed to compile package")
        self.built = True
    
    def run_tests(self):
        if not self.built:
            raise Exception("Executable not built...")

        cnt = 0
        total_cpu_time = 0
        for input_file, output_file in self.pack.gen_in_out():
            # with open(output_file, 'r') as file:
            #     expected_output = file.read()

            perf_command = ["perf", "stat", "-e", "cpu-cycles,instructions", self.exe]
            
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
        
        runs.sort()
        trimmed_runs = runs[1:-1]  # Remove the first and last elements
        mean = sum(trimmed_runs) / len(trimmed_runs)
    
        return mean