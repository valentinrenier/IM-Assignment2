import Levenshtein
from api import user_repos

def closest_word(word_list, target_word):
    if not word_list:
        return None 

    closest = min(word_list, key=lambda word: Levenshtein.distance(word, target_word))
    return closest

def get_repo_from_query(query_repo, repo_list):
    repo_name_list = [str(repo.name).lower() for repo in repo_list]
    mapped_repo = {}
    for r in repo_list:
        mapped_repo[str(r.name).lower()] = r
    

    repo = closest_word(repo_name_list, query_repo.lower())

    return mapped_repo.get(repo)

if __name__ == '__main__':
    word_list = user_repos

    target_word = 'de rmi'

    # print(closest_word(word_list, target_word))  # Sortie attendue : 'OS430'

    print(get_repo_from_query("tets", word_list).full_name)