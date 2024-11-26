import Levenshtein

def closest_word(word_list, target_word):
    if not word_list:
        return None 
    
    closest = min(word_list, key=lambda word: Levenshtein.distance(word, target_word))
    return closest

def get_repo_from_query(query_repo, repo_list):
    mapped_repo = {}
    if repo_list == []:
        return None
    if isinstance(repo_list[0],str) :
        repo_name_list = [repo.lower() for repo in repo_list]
        for r in repo_list:
            mapped_repo[r.lower()] = r
    else :
        repo_name_list = [str(repo.name).lower() for repo in repo_list]
        for r in repo_list:
            mapped_repo[str(r.name).lower()] = r
    

    repo = closest_word(repo_name_list, query_repo.lower())

    return mapped_repo.get(repo)


def extract_entities(response):
    entities = {}
    for entity in response['entities']:
        entities[entity['entity']] = entity['value']
    return entities

