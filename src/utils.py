import numpy as np
from fuzzywuzzy import fuzz, process


# get best match from search in a list:
def best_match(name, titles, count = 1):
    results = process.extractBests(name, titles, scorer=fuzz.partial_ratio, limit=count, score_cutoff=20)
    if len(results) == 0:
        return None

    title_to_index = {title: idx for idx, title in enumerate(titles)}
    best_titles, best_scores = zip(*results[:count])
    best_indices = [title_to_index[title] for title in best_titles]

    #best_index = np.argmax([result[1] for result in results])
    return list(best_indices), list(best_scores)