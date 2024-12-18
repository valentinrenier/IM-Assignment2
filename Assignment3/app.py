from selenium import webdriver
from selenium.webdriver.common.by import By
from github import Github
from github import Auth
from secret import token
from flask import Flask, jsonify, request
import requests

app = Flask(__name__)
repos = None
driver = None
currentRepo = 0

@app.route('/gesture', methods=['POST'])
def gesture():
    #Changer ici avec le nom des gestes reconnus
    functions = {
        "swipe_right": nextRepo,
        "swipe_left": previousRepo,
        "glasses": showContributors,
        "zooming": showCommits,
        "cross": closeDetails,
        "like": star
    }


    data = request.get_json()
    geste = data['recognized']
    print(geste)
    functions[geste]()

    return jsonify({"message": "Geste reçu avec succès", "geste": geste}), 200


def nextRepo():
    global currentRepo
    global repos
    currentRepo = (currentRepo + 1) % repos.totalCount
    driver.get(f"https://github.com/{getRepo(currentRepo).full_name}")

def previousRepo():
    global currentRepo
    global repos
    currentRepo = (currentRepo - 1) % repos.totalCount
    driver.get(f"https://github.com/{getRepo(currentRepo).full_name}")

def showContributors():
    global currentRepo
    global driver
    driver.get(f"https://github.com/{getRepo(currentRepo).full_name}/graphs/contributors")

def showCommits():
    global currentRepo
    global driver
    driver.get(f"https://github.com/{getRepo(currentRepo).full_name}/commits/main")

def closeDetails():
    global currentRepo
    global driver
    driver.get(f"https://github.com/{getRepo(currentRepo).full_name}")

def star():
    global currentRepo
    global driver
    repo = getRepo(currentRepo)
    url = f"https://api.github.com/user/starred/{repo.full_name}"

    # Effectuer la requête pour s'abonner
    try : 
        response = repo._requester.requestJsonAndCheck(
            "PUT", url, input={"subscribed": True, "ignored": False}
        )
    except : 
        print(f'Failed : {response}')

    driver.get(f"https://github.com/{getRepo(currentRepo).full_name}")
    
    

def init():
    auth = Auth.Token(token)

    try :
        g = Github(auth=auth)
    except :
        print('Could not authenticate')

    global repos
    repos = g.get_user().get_repos()

    global driver
    driver = webdriver.Chrome()

    driver.get("https://github.com/login")
    loginField = driver.find_element(By.ID, "login_field")
    passwordField = driver.find_element(By.ID, "password")
    submitButton = driver.find_element(By.NAME, "commit")

    loginField.send_keys("valentinrenier142@gmail.com")
    passwordField.send_keys("dbgm99dvsa2w6s2")
    submitButton.click()

    driver.get(f"https://github.com/{getRepo(0).full_name}")

def getRepo(i):
    global repos
    repo = repos[i]
    return repo


if __name__ == '__main__':
    init()
    app.run(port=5000, debug=False)
