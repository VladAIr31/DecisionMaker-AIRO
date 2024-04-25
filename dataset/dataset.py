import sys
sys.path.append('../scrapper')
import scrape
import data_builder
from pathlib import Path
import os
import time

DATA_PATH=Path("/media/cristi/Data/airo")

class DataSet:
    
    def __init__(self,data_entries):
        self.data_entries = [data_builder.Package(x) for x in data_entries]
    
    
    def seed(self):
        data_set_path = DATA_PATH / f"data_set_{int(time.time())}"
        self.path = data_set_path
        os.mkdir(data_set_path)
        
        with open(data_set_path/'seed','w') as f:
            for data in self.data_entries:
                f.write(f"{data.url}\n")
                
        return data_set_path

    def expand(self):
        # with open(self.path / 'seed','r') as f:
        #     dataset = f.read().split('\n')[:-1]

        data_path = self.path / 'data'
        if not data_path.exists():
            os.mkdir(data_path)
        
        # TODO: move logic to Package class
        for indx,entry in enumerate(self.data_entries):
            dir = data_path / f"{indx}"
            if dir.exists():
                continue
            os.mkdir(dir)
            
            entry.expand(dir)
            break
            
    
    
    

if __name__ == "__main__":
    data_set = DataSet(scrape.small_set())
    data_set.seed()
    data_set.expand()
    
    