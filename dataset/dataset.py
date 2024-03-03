import sys
sys.path.append('../scrapper')
import scrape
from pathlib import Path
import os
import time

DATA_PATH=Path("/media/cristi/Data/airo")

def seed_data_set(data_set):
    data_set_path = DATA_PATH / f"data_set_{int(time.time())}"
    os.mkdir(data_set_path)
    
    with open(data_set_path/'seed','w') as f:
        for data in data_set:
            f.write(f"{data}\n")
            
    return data_set_path

def expand_data_set(path):
    with open(path / 'seed','r') as f:
        dataset = f.read().split('\n')[:-1]

    data_path = path / 'data'
    if not data_path.exists():
        os.mkdir(data_path)
    
    # TODO: move logic to Package class
    for indx,entry in enumerate(dataset):
        dir = data_path / f"{indx}"
        if dir.exists():
            break
        os.mkdir(dir)
        
        package = scrape.seed_to_package(entry)
        with open(dir / "main.cpp","w") as f:
            f.write(package.source_code)
    
    
    

if __name__ == "__main__":
    data_set = scrape.small_set()
    path = seed_data_set(data_set)   
    
    expand_data_set(Path(path))