import executables.compilers as compilers
from executables.executable import Executable
from dataset.dataset import DataSet
from tqdm import tqdm
import concurrent.futures

AiroCompiler = compilers.AIROCompiler(compilers.AIRO)
GccCompiler = compilers.Compiler(compilers.GCC11_4)
ClangCompiler = compilers.Compiler(compilers.CLANG14)

data_set = DataSet("dataset")
data_set.load()

exes = [Executable(pack,AiroCompiler) for pack in data_set][:10]

for exe in exes:
    exe.build()


# Demo concurrency capability
# def build_exe(exe):
#     exe.build()

# with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
#     list(tqdm(executor.map(build_exe, exes), total=len(exes)))

# print("All builds complete.")

# times = []

# for indx,exe in enumerate(tqdm(exes)):
#     cpu_cycles = exe.benchmark(1,method="time")
#     times.append(cpu_cycles)
    
# print(times)

AiroCompiler.stop()
