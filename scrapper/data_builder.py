import consts
import requests
from bs4 import BeautifulSoup

def parse_response(html):
    soup = BeautifulSoup(html, 'html.parser')
    source = soup.find("pre", {"id":"program-source-text"})
    
    return {"source code" : source.text}

def create_package(url):
    url = f"{consts.CF_CONTEST}{url}"
    response = requests.get(url)
    
    if response.status_code == 200:
        parsed = parse_response(response.text)
    else:
        raise f"Failed to retrieve data, status code: {response.status_code}"
    
    return parsed