import requests

def download_json(base_url, endpoint):
    url = f"{base_url}/{endpoint}.json"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()
