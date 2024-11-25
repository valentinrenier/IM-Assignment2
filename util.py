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


def extract_entities(response):
    entities = {}
    for entity in response['entities']:
        entities[entity['entity']] = entity['value']
    return entities


if __name__ == '__main__':
    word_list = user_repos

    target_word = 'de rmi'

    # print(closest_word(word_list, target_word))  # Sortie attendue : 'OS430'

    # print(get_repo_from_query("tets", word_list).full_name)

    response = {'text': 'Crée une nouvelle branche mabranch au dépôt im', 'intent': {'name': 'create_branch', 'confidence': 0.998471200466156}, 'entities': [{'entity': 'branch', 'start': 26, 'end': 34, 'confidence_entity': 0.8365484354829154, 'value': 'mabranch', 'extractor': 'CRFEntityExtractor'}, {'entity': 'repo', 'start': 44, 'end': 46, 'confidence_entity': 0.9743376976455499, 'value': 'im', 'extractor': 'CRFEntityExtractor'}, {'entity': 'branch', 'start': 26, 'end': 34, 'confidence_entity': 0.9748420119285583, 'value': 'mabranch', 'extractor': 'DIETClassifier'}], 'text_tokens': [[0, 4], [5, 8], [9, 17], [18, 25], [26, 34], [35, 37], [38, 43], [44, 46]], 'intent_ranking': [{'name': 'create_branch', 'confidence': 0.998471200466156}, {'name': 'create_repo', 'confidence': 0.0014085480943322182}, {'name': 'list_user_repos', 'confidence': 4.9417107220506296e-05}, {'name': 'greet', 'confidence': 1.5940000594127923e-05}, {'name': 'affirm', 'confidence': 1.5703937606303953e-05}, {'name': 'deny', 'confidence': 1.1071388144046068e-05}, {'name': 'list_branches', 'confidence': 1.0287419172527734e-05}, {'name': 'delete_repo', 'confidence': 7.494434157706564e-06}, {'name': 'list_organizations', 'confidence': 4.33687500844826e-06}, {'name': 'get_number_of_commits', 'confidence': 3.3187093322339933e-06}]}
    print(extract_entities(response))