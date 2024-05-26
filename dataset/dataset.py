from pathlib import Path
import package
from package import Package
import os
import shutil

DATA_PATH=Path("/media/cristi/New Volume/airo")

class DataSet:
    loaded = False
    
    def __init__(self, data_dir):
        self.indx = -1
        self.data_dir = Path(DATA_PATH) / data_dir
        self.source_code_dir = self.data_dir / "source"
        package.TestHelper.path = self.data_dir / "tests"
        self.ramdisk_dir = Path.home() / "ramdisk" / data_dir
        self.setup_ramdisk()

    def setup_ramdisk(self):
        if not self.ramdisk_dir.exists():
            os.makedirs(self.ramdisk_dir, exist_ok=True)
        
        if not os.path.ismount(self.ramdisk_dir):
            os.system(f"sudo mount -t tmpfs -o size=1G tmpfs {self.ramdisk_dir}")

        if not (self.ramdisk_dir / "source").exists():
            shutil.copytree(self.source_code_dir, self.ramdisk_dir / "source")
        if not (self.ramdisk_dir / "tests").exists():
            shutil.copytree(self.data_dir / "tests", self.ramdisk_dir / "tests")
        
        self.source_code_dir = self.ramdisk_dir / "source"
        package.TestHelper.path = self.ramdisk_dir / "tests"

    def load(self):
        self.packages = [Package(self.source_code_dir / str(x)) for x in sorted(map(int, os.listdir(self.source_code_dir))) if x != 852]  # 852 is weird....
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

    