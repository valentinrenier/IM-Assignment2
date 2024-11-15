from github import Github
from github import Auth

# using an access token
auth = Auth.Token("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")

# Public Web Github
try :
    g = Github(auth=auth)
except :
    print('Could not authenticate')

def list_user_repos():
    repo_list = []
    tts_result = ""
    for repo in g.get_user().get_repos():
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

def greet():
    return "Bonjour, comment puis-je vous aider aujourd'hui ?"