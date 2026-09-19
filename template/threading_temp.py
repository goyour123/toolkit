import requests
import threading

REQUEST_COUNT = 20
URL = "https://api.github.com"

def do_request(url, index, response_list):
    response = requests.get(url)
    print(response.status_code)
    response_list[index] = response

if __name__ == '__main__':
    thread_list = []
    response_list = [None] * REQUEST_COUNT
    for i in range(REQUEST_COUNT):
        t = threading.Thread(target=do_request, args=(URL, i, response_list))
        thread_list.append(t)
        t.start()

    for t in thread_list:
        t.join()

    print(response_list)
