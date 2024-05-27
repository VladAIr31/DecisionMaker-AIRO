import executables.compilers as compilers
from executables.executable import Executable
from dataset.dataset import DataSet
from RL.model import MM
from tqdm import tqdm

NUM_WORKERS = 1
AiroCompiler = compilers.AIROCompiler(compilers.AIRO)
data_set = DataSet("dataset")
data_set.load()

exes = [Executable(pack,AiroCompiler) for pack in data_set][:10]


epoch_scores = {exe: [] for exe in exes}
accumulated_performance = {exe: 0 for exe in exes}
for epoch in range(25):
    print(f"Epoch {epoch + 1}")
    perf = []
    for exe in tqdm(exes):
        exe.build()
        score = exe.benchmark(2) / 1e6
        perf.append(score)
        MM.evaluate_run(score)
        epoch_scores[exe].append(score)
        accumulated_performance[exe] += score
        
    formatted_perf = [f"{score:.3f}" for score in perf]
    print(f"perf: {formatted_perf}")




