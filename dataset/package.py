import json
import os

TEST_DICT = {
    'Îmbarcare avion': 'avion',
    'URL Shortener': 'url_shortener',
    'Poțiuni': 'potiuni',
    'Fancy Font Text': 'activation_code',
    'Emu War': 'emu_war',
    'Snowflake': 'snowflake',
    'Rebound': 'rebound',
    'N-body problem': 'n-body_problem',
    'Piramida': 'piramida',
    'Club': 'club',
    'Cel mai lung tren din lume': 'cel_mai_lung_tren_din_lume',
    'Joc Video': 'joc_video',
    'Free Practice 3': 'fp3',
    'Promovare': 'promovare',
    'Is this AI?': 'is_this_AI'
}

class TestHelper:
    path = None # set by dataset
    _cache = {}  # Class-level cache to store directory listings

    def __init__(self, problem):
        self.problem = problem
        self.dir = TestHelper.path / TEST_DICT[problem] / "tests"
        if problem not in TestHelper._cache:
            TestHelper._cache[problem] = [self.dir / "input" / x for x in sorted(os.listdir(self.dir / "input"))]

    def listdir_generator(self):
        for filename in TestHelper._cache[self.problem]:
            yield filename


class Package:
    loaded = False
    def __init__(self,path):
        self.path = path
        self.main = self.path / "main.cpp"
        
    def __str__(self):
        return f"Package at {self.path}"
        
    def load(self):
        with open(self.path / "metadata",'r') as f:
            self.metadata = json.loads(f.read().replace('\'','\"'))
            self.test_helper = TestHelper(self.metadata["Problem"])

        self.loaded = True

    def get_main(self):
        return self.main
    
    def tests(self):
        return self.test_helper.listdir_generator()
    
    def get_problem(self):
        return self.metadata["Problem"]