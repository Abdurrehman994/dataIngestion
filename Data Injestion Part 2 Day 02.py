import requests
import os
from pprint import pprint
import psycopg2
import time
conn = psycopg2.connect("""dbname=demo user=postgres password=postgre123""")
cur = conn.cursor()
token=''
token = os.getenv('GITHUB_TOKEN', 'YOUR TOKEN')
owner = "freeCodeCamp"
repo = "freeCodeCamp"
# query_url_issues = f"https://api.github.com/repos/{owner}/{repo}/issues"
query_url_branches = f"https://api.github.com/repos/{owner}/{repo}/branches"
query_url_commits = f"https://api.github.com/repos/{owner}/{repo}/commits"

headers = {'Authorization': f'token {token}'}
# r_issues = requests.get(query_url_issues, headers=headers)
r_branches = requests.get(query_url_branches, headers=headers)
r_commits = requests.get(query_url_commits, headers=headers)
#


# print('''============Issues==============''')
url = f"https://api.github.com/repos/{owner}/{repo}/issues?simple=yes&per_page=100&page=1"
res=requests.get(url,headers={"Authorization": token})
data = f"https://api.github.com/repos/{owner}/{repo}"
data=requests.get(data,headers={"Authorization": token})
data = data.json()
# pprint(data)
repository_id = data['id']
# print(repository_id)

repos=res.json()
while 'next' in res.links.keys():
  res=requests.get(res.links['next']['url'],headers={"Authorization": token})
  repos.extend(res.json())
pprint(len(repos))

# First_Table = []
# Second_Table = []
# Third_Table = []
# Fourth_Table = []
# Fifth_Table = []
# Sixth_Table = []
# Seventh_Table = []
# pprint(repos)
# # # Fifth Table
#
cur.execute("CREATE TABLE issues (issue_id integer,repository_id integer,issue_url varchar,issue_title varchar,issue_body varchar,issue_created_at varchar,issue_updated_at varchar,issue_closed_at varchar);")
cur.execute("CREATE TABLE issue_event(issue_event_id varchar ,repository_id integer,issue_event_url varchar,actor_user_id varchar,event varchar,commit_id varchar,commit_url varchar,created_at varchar);")
cur.execute("CREATE TABLE label (label_id varchar,branch_name varchar, repository_id integer);")
cur.execute("CREATE TABLE issue_label (issue_label_id varchar,issue_id integer,label_id varchar);")
cur.execute("CREATE TABLE developer (developer_id integer,developer_login varchar, developer_url varchar,github_user_id varchar);")
cur.execute("CREATE TABLE branches ( branch_name varchar,repository_id integer);")
cur.execute("CREATE TABLE commits (commit_id varchar, commit_url varchar,author_user_id varchar,author_email varchar,committer_email varchar,committer_name varchar,committer_message varchar);")
# print("==========developers===========")
developer_id=data["owner"]["id"]
developer_login=data["owner"]["login"]
developer_url=data["owner"]["html_url"]
#branches and commits
url3 = data["branches_url"]
url3 = str(url3).split('{')[0]
w3 = requests.get(url3)
w3 = w3.json()
Sixth_Table = []
for branch in w3:
    branch_name = branch['name']
    print('branch',branch_name)
    commits_url = branch["commit"]["url"]
    # print('commits_url', commits_url)
    w = requests.get(commits_url)
    w = w.json()
    commit_id = w['sha']
    author_email = w['commit']['author']['email']
    author_name = w['commit']['author']['name']
    author_user_id = w['author']['id']
    committer_user_id = w['committer']['id']
    committer_email = w['commit']['committer']['email']
    committer_name = w['commit']['committer']['name']
    message = w['commit']['message']
    cur.execute("INSERT INTO branches (branch_name,repository_id) VALUES (%s,%s)",(branch_name,repository_id))
    cur.execute("INSERT INTO commits (commit_id, commit_url,author_user_id,author_email,committer_email,committer_name,committer_message) VALUES (%s,%s,%s,%s,%s,%s,%s)",
        (commit_id, commits_url, author_user_id, author_email, committer_email, committer_name,message))
cur.execute("SELECT * FROM branches;")
cur.execute("SELECT * FROM commits;")
# print('2 tables')
# conn.commit()
# cur.close()
# conn.close()


for i in range(len(repos)):
    # First Table
    temp_body = []
    issue_id=repos[i]["id"]
    # print('issue id',issue_id)
    issue_url = repos[i]["url"]
    issue_title = repos[i]['title']
    issue_body = str(repos[i]["body"]).replace('\n','').replace('\r','').replace('\t','')
    issue_created_at = repos[i]["created_at"]
    issue_updated_at = repos[i]['updated_at']
    issue_closed_at = repos[i]['closed_at']
    cur.execute("INSERT INTO issues (issue_id ,repository_id,issue_url ,issue_title,issue_body ,issue_created_at,issue_updated_at,issue_closed_at) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)", (issue_id,repository_id, issue_url, issue_title,issue_body,issue_created_at,issue_updated_at,issue_closed_at))
    cur.execute("SELECT * FROM issues;")
# conn.commit()
# cur.close()
# conn.close()
    event_url = repos[i]["events_url"]
    w = requests.get(event_url)
    # time.sleep(5)
    w = w.json()
    # print(len(w))
    for k in w:
        time.sleep(5)
        Second_Table = []
        issue_event_id = k["id"]
        issue_event_url = k["url"]
        actor_user_id = k["actor"]["id"]
        event = k["event"]
        commit_id = k["commit_id"]
        commit_url = k["commit_url"]
        created_at = k["created_at"]
        print('created',created_at)
        cur.execute("INSERT INTO issue_event(issue_event_id ,repository_id,issue_event_url ,actor_user_id,event ,commit_id ,commit_url,created_at) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)", (issue_event_id,repository_id, issue_event_url,actor_user_id,event,commit_id,commit_url,created_at))
        cur.execute("SELECT * FROM issue_event;")
# conn.commit()
# cur.close()
# conn.close()


    # print("============label=======")
    # Label Represents the whole issue
    lables_Array = repos[i]["labels"]
    # print('labels array:',lables_Array)
    for m in lables_Array:
        label_id = m["id"]
        label_name = m["name"]
        cur.execute("INSERT INTO label (label_id,branch_name, repository_id) VALUES (%s,%s,%s)",(label_id,label_name,repository_id))
    cur.execute("SELECT * FROM label;")

    # print("==========issue_label=====")
    Fourth_Table = []
    for m in lables_Array:
        issue_label_id=m["node_id"]
        label_id = m["id"]
        label_name = m["name"]
        cur.execute("INSERT INTO issue_label (issue_label_id ,issue_id ,label_id ) VALUES (%s,%s,%s)",(issue_label_id,issue_id,label_id))
    cur.execute("SELECT * FROM issue_label;")
#     # print("==========developers===========")
    github_user_id = repos[i]["user"]["id"]
    cur.execute("INSERT INTO developer (developer_id ,developer_login ,developer_url,github_user_id ) VALUES (%s,%s,%s,%s)",(developer_id,developer_login,developer_url,github_user_id))
cur.execute("SELECT * FROM developer;")
conn.commit()
cur.close()
conn.close()

    # Fifth_Table.append([developer_id,developer_login,developer_url,github_user_id])
    # print('Fifth Table: ',Fifth_Table)
    # Sixth Table
    # print("==============branch========")
    # r_branches = r_branches.json()
    # url3 = r_branches[i]["commit"]["url"]
    # w3 = requests.get(url3)
    # w3 = w3.json()
    # add repo id
    # branch_name = r_branches[i]["name"]
    # Sixth_Table.append([url3,repository_id,branch_name])
    # Seventh Table
    # print("=========commit========")
    # r_commits = r_commits.json()
    # url4 = r_commits[i]["url"]
    # w4 = requests.get(url4)
    # w4 = w4.json()
    # commit_id = w4["files"][i]["sha"]
    # branch_id = w3["node_id"]
    # url = r_commits[i]["commit"]["url"]
    # sha = r_commits[i]["sha"]
    # author_user_id = repos[i]["user"]["node_id"]
    # author_email = r_commits[i]["commit"]["author"]["email"]
    # author_name = r_commits[i]["commit"]["author"]["name"]
    # commiter_user_id = r_commits[i]["committer"]["id"]
    # committer_email = r_commits[i]["commit"]["committer"]["email"]
    # committer_name = r_commits[i]["commit"]["committer"]["name"]
    # message = r_commits[i]["commit"]["message"]
    # Seventh_Table.append([commit_id,branch_id,url,sha,author_user_id,author_email,author_name,commiter_user_id,committer_email,committer_name,message])
    # print(f'issue id:{issue_id} issue url: {issue_url} issue title: {issue_title} issue body: {issue_body} issue_created_at: {issue_created_at} issue updated at: {issue_updated_at} issue closed at: {issue_closed_at}')
# for l in data_List:
#     print(l)



