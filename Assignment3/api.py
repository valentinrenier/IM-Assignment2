from selenium import webdriver
import time
from github import Github
from github import Auth
from secret import token

repos = None

def main():
    auth = Auth.Token(token)

    try :
        g = Github(auth=auth)
    except :
        print('Could not authenticate')

    global repos
    repos = g.get_user().get_repos()

    driver = webdriver.Chrome()

    for i in range(repos.totalCount):
        driver.get(f"https://github.com/{getRepo(i).full_name}")
        time.sleep(5)

def getRepo(i):
    global repos
    repo = repos[i]
    return repo

if __name__ == "__main__":
    main()
