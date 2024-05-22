from pathlib import Path
import package
from package import Package
import os

DATA_PATH=Path("/media/cristi/Data/airo")

class DataSet:
    loaded = False
    def __init__(self,data_dir):
        self.indx = -1
        self.data_dir = DATA_PATH / data_dir
        self.source_code_dir = self.data_dir / "source"
        package.TestHelper.path = self.data_dir / "tests"
    
    def load(self):
        self.packages = [Package(self.source_code_dir / str(x)) for x in sorted(map(int,os.listdir(self.source_code_dir)))]
        for package in self.packages:
            package.load()
        self.loaded = all([package.loaded for package in self.packages])
                    
    def __iter__(self):
        return self
    
    def __next__(self):
        self.indx += 1
        if self.indx < len(self.packages):
            return self.packages[self.indx]
        raise StopIteration

if __name__ == "__main__":
    data_set = DataSet("dataset")
    data_set.load()

    