import Levenshtein
from api import get_user_repos

def closest_word(word_list, target_word):
    if not word_list:
        return None 

    closest = min(word_list, key=lambda word: Levenshtein.distance(word, target_word))
    closest_score = Levenshtein.distance(closest, target_word)
    return closest, closest_score

def get_repo_from_query(query, repo_list):
    repo_name_list = [str(repo.name).lower() for repo in repo_list]
    mapped_repo = {}
    for r in repo_list:
        mapped_repo[str(r.name).lower()] = r
    
    query = query.lower()

    terms = query.split()
    min = 100
    repo = None

    for i in range(len(terms)-1):
        term = f"{terms[i]} {terms[i+1]}"
        tmp, tmpMin = closest_word(repo_name_list, term)
        print(f"term : {term} | tmp : {tmp} | tmpMin : {tmpMin}")
        if tmpMin <= min:
            min = tmpMin
            repo = tmp

    return mapped_repo.get(repo)

if __name__ == '__main__':
    word_list = get_user_repos()

    target_word = 'de rmi'

    # print(closest_word(word_list, target_word))  # Sortie attendue : 'OS430'

    print(get_repo_from_query("Qui a contribué à IM Assignment 2", word_list).full_name)