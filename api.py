from github import Github
from github import Auth
from secret import token

# using an access token
auth = Auth.Token(token)

# Public Web Github
try :
    g = Github(auth=auth)
except :
    print('Could not authenticate')

user_repos = g.get_user().get_repos()

def list_user_repos():
    repo_list = []
    tts_result = ""
    for repo in user_repos:
        repo_list.append(repo.name)
    for s in repo_list :
        if isinstance(s, str):
            tts_result += f",{s}"
    return tts_result

def list_organizations():
    orgs_list = []
    tts_result = ""
    for org in g.get_user().get_orgs():
        orgs_list.append(org.name)
    for s in orgs_list :
        if isinstance(s, str):
            tts_result += f",{s}"
    return tts_result

def list_repo_contributors(repo_name):
    repo = g.get_repo(repo_name)
    print("repo to search", repo)
    contributors = repo.get_contributors()
    tts_result = ""
    for contributor in contributors:
        tts_result += f",{contributor.login}"
    return tts_result

def list_repo_commits(repo_name):
    repo = g.get_repo(repo_name)
    commits = repo.get_commits()
    tts_result = ""
    for commit in commits:
        tts_result += f",{commit.commit.message}"
    return tts_result

def greet():
    return "Bonjour, comment puis-je vous aider aujourd'hui ?"



if __name__ == "__main__":
    print(list_repo_commits('robinlafage/RMI'))