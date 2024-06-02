import executables.compilers as compilers
from executables.executable import Executable
from dataset.dataset import DataSet
from RL.model import MM
from tqdm import tqdm
import json
import os

NUM_WORKERS = 1
AiroCompiler = compilers.AIROCompiler(compilers.AIRO)
data_set = DataSet("dataset")
data_set.load()

trimmed_dataset = [pack for pack in data_set][:20]

exes = [Executable(pack, AiroCompiler) for pack in trimmed_dataset]
exes_pre = [Executable(pack, AiroCompiler) for pack in trimmed_dataset]


CACHE_FILE = "../cache/normalization_factors.json"

def save_normalization_factors(factors, filepath):
    with open(filepath, 'w') as f:
        json.dump({str(exe): factor for exe, factor in factors.items()}, f)

def load_normalization_factors(filepath):
    with open(filepath, 'r') as f:
        data = json.load(f)
    return {str(exe): factor for exe, factor in data.items()}

if os.path.exists(CACHE_FILE):
    print("Loading normalization factors from cache")
    normalization_factors = load_normalization_factors(CACHE_FILE)
else:
    print("Prerun for normalization")
    prerun_scores = {str(exe): [] for exe in exes}
    for exe, exe_key in tqdm(zip(exes_pre, exes)):
        exe.build()
        scores = [exe.benchmark(5) / 1e6 for _ in range(5)]
        print(scores)
        prerun_scores[str(exe_key)].extend(scores)
    
    # Calculate the normalization factor as the mean of prerun scores
    normalization_factors = {str(exe): sum(scores) / len(scores) for exe, scores in prerun_scores.items()}
    
    # Save the normalization factors to a file
    save_normalization_factors(normalization_factors, CACHE_FILE)

epoch_scores = {str(exe): [] for exe in exes}
accumulated_performance = {str(exe): 0 for exe in exes}

epoch_scores = {str(exe): [] for exe in exes}
accumulated_performance = {str(exe): 0 for exe in exes}

for epoch in range(25):
    print(f"Epoch {epoch + 1}")
    perf = []
    for exe in tqdm(exes):
        exe.build()
        scores = [exe.benchmark(2) / 1e6 for _ in range(2)]
        avg_score = sum(scores) / len(scores)
        normalized_score = avg_score / normalization_factors[str(exe)]
        perf.append(normalized_score)
        MM.evaluate_run(normalized_score)
        epoch_scores[str(exe)].append(normalized_score)
        accumulated_performance[str(exe)] += normalized_score
        
    formatted_perf = [f"{score:.3f}" for score in perf]
    print(f"perf: {formatted_perf}")




