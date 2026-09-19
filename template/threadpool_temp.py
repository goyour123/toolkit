import requests
from concurrent.futures import ThreadPoolExecutor

REQUEST_COUNT = 20
URL = "https://api.github.com"

def do_request(url):
    response = requests.get(url, timeout=10)
    print(response.status_code)
    return response

if __name__ == '__main__':
    with ThreadPoolExecutor(max_workers=REQUEST_COUNT) as executor:
        response_list = list(executor.map(do_request, [URL] * REQUEST_COUNT))

    print(response_list)
