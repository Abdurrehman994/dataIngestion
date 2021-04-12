import pprint
import time
import csv
try:
    import requests
    import pandas as pd
    from bs4 import BeautifulSoup
except Exception as e :
    print("some modules are missing {}".format(e))
def get_repository(url):
    r=requests.get(url)
    dom=BeautifulSoup(r.content,'lxml')
    a1=dom.find_all('div', class_="row")
    base_url="https://gitstar-ranking.com/"
    for _,i in enumerate(a1):
        count = 0

        for a in i.findAll("a"):
            count += 1
            new_url=base_url+a["href"]
            y = requests.get(new_url)
            dom = BeautifulSoup(y.content, 'html.parser')
            a1 = dom.find_all('div', class_="repository_value text-center")
            # print(a1[1].text.strip())
            my_list = []
            for k in a.text.strip():
                my_list.append(k)
            string = "".join(my_list)
            string2 = string.split('\n')
            repo_id = string2[0].split('.')
            repo_id = repo_id[0]
            repo_name = string2[2]
            repo_rating = string2[10]
            try:
                with open('repos.csv', 'a', newline='') as csvfile:
                    writer = csv.writer(csvfile, delimiter=",")
                    # spamwriter = csv.writer(csvfile, delimiter=',',quotechar='|', quoting=csv.QUOTE_MINIMAL)

                    print(f'repo_url: {new_url} repo_id:{repo_id} repo_name: {repo_name}, rating: {repo_rating} rank: {a1[1].text.strip()}')
                    writer.writerow([new_url, repo_name, repo_id, repo_rating, a1[1].text.strip()])
            except:
                print('Error!!!')

            # print(a.text.strip(),'......................')
        break
url='https://gitstar-ranking.com/repositories'
n=1
h=1
with open('repos.csv', 'a', newline='') as csvfile:
    writer = csv.writer(csvfile, delimiter=",")
    # spamwriter = csv.writer(csvfile, delimiter=',',quotechar='|', quoting=csv.QUOTE_MINIMAL)
    writer.writerow(['Repo URL', 'Repo Name', 'Repo ID','Rating','Repo Rank'])
while h!=50:
    if n!=1:
        url = 'https://gitstar-ranking.com/repositories'
        new_url=url+'?page='+str(h)
        print(new_url)
        get_repository(new_url)
        time.sleep(5)
        n=n+1
        h=h+1
    if n==1:
        get_repository(url)
        time.sleep(5)
        n = n + 1
        h = h + 1


