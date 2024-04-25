import consts
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import time

class Package:
    loaded = False
    def __str__(self):
        str = self.url
        if self.source_code:
            str += f"CODE:\n {self.source_code}\n"
        if self.tests:
            for i,test in enumerate(self.tests):
                str += f"test {i}: {test})"
            
        return str

    def __init__(self,url):
        self.url = url

    def fetch(self):
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service)

        full_url = f"{consts.CF_CONTEST}{self.url}"

        source_code = None
        tests = []
        try:
            driver.get(full_url)
            timeout = 10
            
            button = WebDriverWait(driver, timeout).until(
                EC.element_to_be_clickable((By.CLASS_NAME, "click-to-view-tests"))
            )
            button.click()
            
            pre_element = WebDriverWait(driver, timeout).until(
                EC.visibility_of_element_located((By.ID, "program-source-text"))
            )
            source_code = pre_element.text

            time.sleep(1)
                        
            input_views = WebDriverWait(driver, timeout).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, 'input-view'))
            )
                                    
            for input_view in input_views:
                input = input_view.find_element(By.CLASS_NAME, 'input').text
                output_view = input_view.find_element(By.XPATH, "./following-sibling::div[contains(@class, 'output-view')]")
                output = output_view.find_element(By.CLASS_NAME, 'output').text
                if input[-3:] != "..." and output[-3:] != "..." and input != '' and output != '':
                    tests.append({
                        "input"  : input,
                        "output" : output,
                    })
            
            
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            driver.quit()
        
        self.source_code = source_code
        self.tests = tests
        self.loaded = True
    
    def expand(self,dir):
        self.path = dir
                
        indir = dir / "input"
        outdir = dir / "output"
        
        if indir.exists() and outdir.exists():
            return
        
        os.mkdir(indir)
        os.mkdir(outdir)

        if not self.loaded:
            self.fetch()
        with open(dir / "main.cpp","w") as f:
            f.write(self.source_code)
                
        for indx,test in enumerate(self.tests):
            with open(indir / f"{indx}","w") as f:
                f.write(test["input"])
            with open(outdir / f"{indx}","w") as f:
                f.write(test["output"])
                
    def get_main(self):
        return self.path / "main.cpp"
    
    def get_input(self):
        inp = self.path / "input"
        return [inp / x for x in os.listdir(inp)]
    
    def get_output(self):
        out = self.path / "output"
        return [out / x for x in os.listdir(out)]
    
    def gen_in_out(self):
        for inp,out in zip(self.get_input(),self.get_output()):
            yield inp,out
