import executables.compilers as compilers
from executables.executable import Executable
from dataset.dataset import DataSet
from tqdm import tqdm

AiroCompiler = compilers.AIROCompiler(compilers.AIRO)
GccCompiler = compilers.Compiler(compilers.GCC11_4)
ClangCompiler = compilers.Compiler(compilers.CLANG14)

data_set = DataSet("dataset")
data_set.load()

exes = [Executable(pack,AiroCompiler) for pack in data_set][:10]


for exe in tqdm(exes):
    exe.build()

times = []

for indx,exe in enumerate(tqdm(exes)):
    cpu_cycles = exe.benchmark(1)
    times.append(cpu_cycles)
    
print(times)


AiroCompiler.stop()
