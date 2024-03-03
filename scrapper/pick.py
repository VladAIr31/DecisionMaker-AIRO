import consts
import requests

def fetch_data_set(contest_id,size,start=1):
    url = f"{consts.CF_API}contest.status?contestId={contest_id}&asManager=false&from={start}&count={10 * size}" # attempt to optimize the number of request so we find size 
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
    else:
        raise f"Failed to retrieve data, status code: {response.status_code}"
    
    routes = []
    for submission in data['result']:
        if submission['verdict'] == 'OK' and "C++" in submission["programmingLanguage"]:
            routes.append(f"{contest_id}/submission/{submission['id']}")
        if len(routes) == size:
            break
        
    diff = size - len(routes)
    if diff > 0:
        routes += fetch_data_set(contest_id=contest_id,size=diff,start=start + size)
    
    
    return routes