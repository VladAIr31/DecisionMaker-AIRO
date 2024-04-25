import sys
sys.path.append('./scrapper')
import data_builder
from pathlib import Path
import os
import time

DATA_PATH=Path("/media/cristi/Data/airo")

class DataSet:
    
    def __init__(self,data):
        self.indx = -1
        if isinstance(data,list):
            self.data_entries = [data_builder.Package(x) for x in data]
        else:
            self.path = Path(f"{DATA_PATH}/{data}")
            with open(self.path / 'seed','r') as f:
                dataset = f.read().split('\n')[:-1]
                self.data_entries = [data_builder.Package(x) for x in dataset]
    
    def seed(self):
        data_set_path = DATA_PATH / f"data_set_{int(time.time())}"
        self.path = data_set_path
        os.mkdir(data_set_path)
        
        with open(data_set_path/'seed','w') as f:
            for data in self.data_entries:
                f.write(f"{data.url}\n")
                
        return data_set_path

    def expand(self):
        data_path = self.path / 'data'
        if not data_path.exists():
            os.mkdir(data_path)
        
        for indx,entry in enumerate(self.data_entries):
            dir = data_path / f"{indx}"
            if not dir.exists():
                os.mkdir(dir)
            
            entry.expand(dir)
            
    def __iter__(self):
        return self
    
    def __next__(self):
        self.indx += 1
        if self.indx < len(self.data_entries):
            return self.data_entries[self.indx]
        raise StopIteration
        
    
    

if __name__ == "__main__":
    # data_set = DataSet(scrape.small_set())
    # data_set.seed()
    # data_set.expand()
    
    data_set = DataSet("data_set_1714046499")
    data_set.expand()
    