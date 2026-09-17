import requests
import threading

def do_request(url, index, response_list):
    response = requests.get(url)
    print(response.status_code)
    response_list[index] = response

if __name__ == '__main__':
    thread_list = []
    response_list = [None] * len(range(0, 20))
    for i in range(0, 20):
        t = threading.Thread(target=do_request, args=("https://api.github.com", i, response_list))
        thread_list.append(t)
        t.start()

    for t in thread_list:
        t.join()

    print(response_list)
