import time
import csv
import threading

try:
    import requests
    import pandas as pd
    from bs4 import BeautifulSoup
except Exception as e:
    print("some modules are missing {}".format(e))

file = open('reposs.csv', "a", newline='')
with file:
    write = csv.writer(file)
    write.writerow(['Repo ID', 'Repo URL ', 'Repo Name', 'Rating', 'Repo Rank'])


def get_repository(pageNo, url):
    r = requests.get(url)
    dom = BeautifulSoup(r.content, 'lxml')
    a1 = dom.find_all('div', class_="row")
    base_url = "https://gitstar-ranking.com/"
    for _, i in enumerate(a1):
        count = 0

        for a in i.findAll("a"):
            # Getting the Repo_name and its Value
            repo_id = ''
            count += 1
            new_url = base_url + a["href"]
            y = requests.get(new_url)
            repo_name_extend = new_url.split('//')
            repo_name = repo_name_extend[-1]
            dom = BeautifulSoup(y.content, 'html.parser')
            a1 = dom.find_all('div', class_="repository_value text-center")
            my_list = []
            for k in a.text.strip():
                my_list.append(k)
            string = "".join(my_list)
            string2 = string.split('\n')
            repo_rating = string2[10]
            # print(repo_rating)

            base_url_repo = 'https://github.com/'
            repo_url = base_url_repo + repo_name
            repo_content = "NONE"
            # Getting Repository ID
            for tries in range(100):
                y = requests.get(repo_url)
                html = BeautifulSoup(y.content, 'lxml')
                meta = html.find('head')
                dLink = meta.find('meta', attrs={'name': 'hovercard-subject-tag'})
                if dLink is not None:
                    repo_content = dLink.get('content')
                    p = repo_content.split(":")
                    repo_id = p[1]
                    break
                if dLink is None:
                    time.sleep(2)

            try:
                # Saving Data into CSV
                print('URL: ', repo_url)

                file = open('reposs.csv', "a", newline='')
                with file:
                    write = csv.writer(file)
                    write.writerow([repo_id, repo_url, repo_name, repo_rating, a1[1].text.strip()])

            except:

                print('Error!!!')

        break


url = 'https://gitstar-ranking.com/repositories'
n = 1
h = 1

threads = list()
k = 0
# Starting of the Time
# Apply Threading
start_time = time.time()
while h != 51:
    if n != 1:
        url = 'https://gitstar-ranking.com/repositories'
        url = url + '?page=' + str(h)

    k += 1
    n += 1
    h += 1
    print('Thread No', k, 'is opening for url', url)

    x = threading.Thread(target=get_repository, args=(k, url))
    x.start()
    threads.append(x)

for index, thread in enumerate(threads):
    thread.join()
print('Execution Completed in: ', time.time() - start_time, ' Seconds')
