import executables.compilers as compilers
from executables.executable import Executable
from dataset.dataset import DataSet
from tqdm import tqdm
import numpy as np
import concurrent.futures


NUM_WORKERS = 4 # sweet spot for some reason
AiroCompiler = compilers.AIROCompiler(compilers.AIRO)
GccCompiler = compilers.Compiler(compilers.GCC11_4)
ClangCompiler = compilers.Compiler(compilers.CLANG14)

data_set = DataSet("dataset")
data_set.load()

exes = [Executable(pack,ClangCompiler) for pack in data_set][:10]

times = []

# Demo concurrency capability
def run(exe):
    exe.build()
    bench = exe.benchmark(5)
    times.append((int(str(exe.pack.path).split('/')[-1]),bench))

times_dict = {i: [] for i in range(len(exes))}

# warmup??
# with concurrent.futures.ThreadPoolExecutor(max_workers=NUM_WORKERS) as executor:
#         list(tqdm(executor.map(run, exes), total=len(exes)))

# times = []

for _ in range(3):
    with concurrent.futures.ThreadPoolExecutor(max_workers=NUM_WORKERS) as executor:
        list(tqdm(executor.map(run, exes), total=len(exes)))

    times = sorted(times, key=lambda x: x[0])
    
    print([f"{x[1]:.3f}" for x in times])
    
    for indx, performance in times:
        times_dict[indx].append(performance)
    times = []


mean_dict = {k: np.mean(v) for k, v in times_dict.items()}

print("Mean for each entry:")
for k, mean in mean_dict.items():
    print(f"Exe {k}: Mean = {mean:.6f}")

# Calculate error percentage for each component
error_percentage_dict = {}
for k, values in times_dict.items():
    mean = mean_dict[k]
    error_percentages = [abs((value - mean) / mean) * 100 for value in values]
    error_percentage_dict[k] = error_percentages

# Print the error percentage for each component
print("\nError percentages for each component:")
for k, error_percentages in error_percentage_dict.items():
    print(f"Exe {k}: Error Percentages = {error_percentages}")

# Optionally, you can calculate and print the average error percentage for each entry
average_error_percentage_dict = {k: np.mean(v) for k, v in error_percentage_dict.items()}
print("\nAverage error percentage for each entry:")
for k, avg_error in average_error_percentage_dict.items():
    print(f"Exe {k}: Average Error Percentage = {avg_error:.6f}%")

all_errors = [error for errors in error_percentage_dict.values() for error in errors]
overall_average_error = np.mean(all_errors)

print(f"Overall Average Error Percentage = {overall_average_error:.6f}%")

AiroCompiler.stop()
