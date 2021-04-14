import requests
import os
from pprint import pprint

token = os.getenv('GITHUB_TOKEN', '')
owner = "freeCodeCamp"
repo = "freeCodeCamp"
query_url_issues = f"https://api.github.com/repos/{owner}/{repo}/issues"
query_url_branches = f"https://api.github.com/repos/{owner}/{repo}/branches"
query_url_commits = f"https://api.github.com/repos/{owner}/{repo}/commits"
params = {
    "state": "open",
}
headers = {'Authorization': f'token {token}'}
r_issues = requests.get(query_url_issues, headers=headers, params=params)
r_branches = requests.get(query_url_branches, headers=headers, params=params)
r_commits = requests.get(query_url_commits, headers=headers, params=params)

print('''============Issues==============''')

print('Issue id:',r_issues.json()[0]["id"])
# # add repo id
print("url:",r_issues.json()[0]["url"])
print(' Issue Title:',r_issues.json()[0]['title'])
print('Issue body:',r_issues.json()[0]["body"])
print('created at:',r_issues.json()[0]["created_at"])
print('updated at:',r_issues.json()[0]['updated_at'])
print('closed at:',r_issues.json()[0]['closed_at'])

print("==========issue event=====")
url=r_issues.json()[0]["events_url"]
w=requests.get(url)
# pprint(w.json())
print("issue_event_id:",w.json()[0]["id"])
#add repo id
print('url:',w.json()[0]["url"])
print('actor_user_id:',w.json()[0]["actor"]["id"])
print('event:',w.json()[0]["event"])
print('commit_id:',w.json()[0]["commit_id"])
print('commit_url:',w.json()[0]["commit_url"])
print('created at:',w.json()[0]["created_at"])
print("============label=======")
print('label_id:',r_issues.json()[0]["labels"][0]["id"])
print('label_name:',r_issues.json()[0]["labels"][0]["name"])
#add repo id
print("==========issue_label=====")
url2=r_issues.json()[0]["labels_url"]
print('issue label_id:',url2)
#issue label_id  extract from link
# print('issue label_id:',r.json()[0]["labels_url"])
print('issue_id:',r_issues.json()[0]["id"])
print('label_id:',r_issues.json()[0]["labels"][0]["id"])
"==========developers==========="
print('developers id:',r_issues.json()[0]["user"]["id"])
print('login:',r_issues.json()[0]["user"]["login"])
print('url:',r_issues.json()[0]["user"]["url"])
print('github_user_id:',r_issues.json()[0]["user"]["node_id"])
print("==============branch========")
url3=r_branches.json()[0]["commit"]["url"]
# pprint(url3)
w3=requests.get(url3)
print('branch_id:',w3.json()["node_id"])
#add repo id
print('link:',w3.json())
print('branch name:',r_branches.json()[0]["name"])
print("=========commit========")
url4=r_commits.json()[0]["url"]
w4=requests.get(url4)
print('commit_id:',w4.json()["files"][0]["sha"])
print('branch_id:',w3.json()["node_id"])
print('url:',r_commits.json()[0]["commit"]["url"])
print('sha:',r_commits.json()[0]["sha"])
print('author_user_id:',r_commits.json()[0]["author"]["id"])
print('author email:',r_commits.json()[0]["commit"]["author"]["email"])
print('author name:',r_commits.json()[0]["commit"]["author"]["name"])
print('commiter user_id:',r_commits.json()[0]["committer"]["id"])
print('committer_email:',r_commits.json()[0]["commit"]["committer"]["email"])
print('committer_name:',r_commits.json()[0]["commit"]["committer"]["name"])
print('message:',r_commits.json()[0]["commit"]["message"])





















