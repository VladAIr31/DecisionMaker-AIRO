import consts
import requests

def fetch_data_set(contest_id,size):
    url = f"{consts.CF_API}contest.status?contestId={contest_id}&asManager=false&from=1&count={size}"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
    else:
        raise f"Failed to retrieve data, status code: {response.status_code}"
    
    routes = []
    for submission in data['result']:
        if submission['verdict'] == 'OK' and "C++" in submission["programmingLanguage"]:
            routes.append(f"{contest_id}/submission/{submission['id']}")
    
    return routes