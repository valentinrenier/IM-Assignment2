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
last_intent = None
mapped_repo = None

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

def list_repo_contributors(repo):
    repo = g.get_repo(repo.full_name)
    print("repo to search", repo)
    contributors = repo.get_contributors()
    tts_result = ""
    for contributor in contributors:
        tts_result += f",{contributor.login}"
    return tts_result

def list_repo_commits(repo):
    repo = g.get_repo(repo.full_name)
    commits = repo.get_commits()
    tts_result = ""
    for commit in commits:
        tts_result += f",{commit.commit.message}"
    return tts_result

def get_number_of_commits(repo):
    global last_intent
    last_intent = 'list_repo_commits'
    global mapped_repo
    mapped_repo = {"repo": repo}

    repo = g.get_repo(repo.full_name)
    commits = repo.get_commits()
    return "Il y a " + str(len(list(commits))) + " commits dans le dépôt " + repo.full_name + ". Voulez-vous que j'énonce la liste des commits ?"

def create_repo(repo):
    try:
        g.get_user().create_repo(repo)
        return f"Le dépôt '{repo}' a été créé avec succès."
    except Exception as e:
        return f"Le dépôt '{repo}' n'a pas pu être créé. Erreur : {e.data['errors'][0]['message']}"

def greet():
    return "Bonjour, comment puis-je vous aider aujourd'hui ?"

def affirm():
    if last_intent:
        result = intent_functions.get(last_intent)(**mapped_repo)
        return result




intent_functions={'greet':greet, 'affirm':affirm, 'list_user_repos':list_user_repos, 'list_organizations':list_organizations, 'list_repo_contributors':list_repo_contributors, 'list_repo_commits':list_repo_commits, 'get_number_of_commits':get_number_of_commits, 'create_repo':create_repo}

if __name__ == "__main__":
    print(get_number_of_commits("robinlafage/RMI"))