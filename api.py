from github import Github
from github import Auth
from secret import token
import inspect

# using an access token
auth = Auth.Token(token)

# Public Web Github
try :
    g = Github(auth=auth)
except :
    print('Could not authenticate')

user_repos = g.get_user().get_repos()
next_intent = None
mapped_repo = None

def list_user_repos():
    repo_list = []
    tts_result = ""
    global user_repos
    user_repos = g.get_user().get_repos()
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
    print(orgs_list)
    for s in orgs_list :
        if isinstance(s, str):
            tts_result += f",{s}" 
    return tts_result

def list_repo_contributors(repo):
    print("repo to search", repo)
    contributors = repo.get_contributors()
    tts_result = ""
    for contributor in contributors:
        tts_result += f",{contributor.login}"
    return tts_result

def list_repo_commits(repo):
    commits = repo.get_commits()
    tts_result = ""
    for commit in commits:
        tts_result += f",{commit.commit.message}"
    return tts_result

def get_number_of_commits(repo):
    global next_intent
    next_intent = 'list_repo_commits'
    global mapped_repo
    mapped_repo = {"repo": repo}

    commits = repo.get_commits()
    return "Il y a " + str(len(list(commits))) + " commits dans le dépôt " + repo.full_name + ". Voulez-vous que j'énonce la liste des commits ?"

def create_repo(repo):
    try:
        g.get_user().create_repo(repo)
        global user_repos
        user_repos = g.get_user().get_repos()
        return f"Le dépôt '{repo}' a été créé avec succès."
    except Exception as e:
        return f"Le dépôt '{repo}' n'a pas pu être créé. Erreur : {e.data['errors'][0]['message']}"

def delete_repo(repo):
    global next_intent
    next_intent = 'confirm_delete_repo'
    global mapped_repo
    mapped_repo = {"repo": repo}

    return f"Voulez-vous vraiment supprimer le dépôt {repo.full_name} ?"

def confirm_delete_repo(repo):
    try:
        repo.delete()
        global user_repos
        user_repos = g.get_user().get_repos()
        return f"Le dépôt '{repo.full_name}' a été supprimé avec succès."
    except Exception as e:
        return f"Le dépôt '{repo.full_name}' n'a pas pu être supprimé. Erreur : {e.data['errors'][0]['message']}"

def list_branches(repo):
    branches = repo.get_branches()
    tts_result = ""
    for branch in branches:
        tts_result += f",{branch.name}"
    return tts_result

def create_branch(repo, branch):
    try:
        repo.create_git_ref(ref=f"refs/heads/{branch}", sha=repo.get_branch('master').commit.sha)
        return f"La branche '{branch}' a été créée avec succès dans le dépôt '{repo.full_name}'."
    except Exception as e:
        return f"La branche '{branch}' n'a pas pu être créée. Erreur : {e.data['errors'][0]['message']}"

def repository_report(repo):
    contributors = repo.get_contributors()
    commits = repo.get_commits()
    branches = repo.get_branches()
    languages = repo.get_languages()
    creation_date = repo.created_at.strftime("%d/%m/%Y")
    description = f"La description du dépôt est : {repo.description}" if repo.description else ""

    return f"Le dépôt {repo.full_name}, créé le {creation_date}, contient {len(list(contributors))} contributeurs, {len(list(commits))} commits, {len(list(branches))} branches et est écrit en {len(list(languages))} langages différents. {description}"

def list_repo_languages(repo):
    languages = repo.get_languages()
    tts_result = "Les langages utilisés dans ce dépôt sont :"
    for language in languages:
        tts_result += f",{language}"
    return tts_result

def greet():
    return "Bonjour, comment puis-je vous aider aujourd'hui ?"

def affirm():
    if next_intent:
        signature = inspect.signature(intent_functions.get(next_intent))
        if len(signature.parameters) > 0 :
            result = intent_functions.get(next_intent)(**mapped_repo)
        else : 
            result = intent_functions.get(next_intent)()
        return result

def deny():
    try :
        global next_intent
        if next_intent:
            next_intent = None
    except :
        print('Next_intent is not set')
    return "Action annulée avec succès"

def not_sure_of_the_intent(intent, parameter):
    global next_intent
    next_intent = intent
    global mapped_repo
    if not parameter is None :
        mapped_repo = {"repo": parameter['repo']}
    return f'Je ne suis pas sûr d\'avoir compris, voulez vous effectuer l\'action {intent}'

def intent_not_understood():
    return "Je suis désolé, mais je n'ai pas réussi à interpréter votre demande. Pouvez vous répéter s'il vous plaît ?"




intent_functions={'greet':greet, 
                  'affirm':affirm, 
                  'list_user_repos':list_user_repos, 
                  'list_organizations':list_organizations, 
                  'list_repo_contributors':list_repo_contributors, 
                  'list_repo_commits':list_repo_commits, 
                  'get_number_of_commits':get_number_of_commits, 
                  'create_repo':create_repo, 'delete_repo':delete_repo, 
                  'confirm_delete_repo':confirm_delete_repo, 
                  'list_branches':list_branches, 
                  'deny':deny,
                  'not_sure_of_the_intent':not_sure_of_the_intent,
                  'intent_not_understood':intent_not_understood,
                  'create_branch':create_branch,
                  'repository_report':repository_report,
                  'list_repo_languages':list_repo_languages}

if __name__ == '__main__':
    print(repository_report(g.get_repo('imaccount/test')))