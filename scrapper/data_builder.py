import consts
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time

class Package:
    
    def set_source(self,source_code):
        self.source_code = source_code
    def set_tests(self,tests):
        self.tests = tests

    def __str__(self):
        str = f"CODE:\n {self.source_code}\n"
        for i,test in enumerate(self.tests):
            str += f"test {i}: {test})"
            
        return str

def create_package(url):
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)

    full_url = f"{consts.CF_CONTEST}{url}"

    source_code = None
    tests = []
    try:
        driver.get(full_url)
        
        button = driver.find_element(By.CLASS_NAME, "click-to-view-tests")
        button.click()
        
        pre_element = driver.find_element(By.ID, "program-source-text")
        source_code = pre_element.text
        
        time.sleep(1)    
        
        input_views = driver.find_elements(By.CLASS_NAME, 'input-view')
        
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
    ans = Package()
    
    ans.set_source(source_code)
    ans.set_tests(tests)

    return ans