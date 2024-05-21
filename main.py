from executables.compilers import AiroCompiler,ClangCompiler,GCCCompiler
from executables.executable import Executable
import dataset.dataset as ds


data_set = ds.DataSet("data_set_1714148547")
data_set.expand()

exes = [Executable(pack,ClangCompiler) for pack in data_set]


for exe in exes:
    exe.build()

for indx,exe in enumerate(exes):
    cpu_cycles = exe.benchmark(20)
    print(f"#{indx}:{cpu_cycles}")
