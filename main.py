from executables.compilers import AiroCompiler,ClangCompiler,GCCCompiler
from executables.executable import Executable
from dataset.dataset import DataSet
from tqdm import tqdm

data_set = DataSet("dataset")
data_set.load()

exes = [Executable(pack,GCCCompiler) for pack in data_set][:10]


for exe in tqdm(exes):
    exe.build()

for indx,exe in enumerate(exes):
    cpu_cycles = exe.benchmark(1)
    print(f"#{indx}:{cpu_cycles}")
