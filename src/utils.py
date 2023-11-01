from fuzzywuzzy import fuzz, process


def custom_scorer(query, choice):
    exact_match_bonus = 1000  # Some high value to ensure exact matches are prioritized
    length_penalty = abs(len(query) - len(choice))

    # Check for exact match
    if query == choice:
        return exact_match_bonus

    # + fuzz.ratio(query, choice) 
    score = fuzz.partial_ratio(query, choice) - length_penalty * 0.1
    return score


# get best match from search in a list:
def best_match(name, titles, count = 1):
    results = process.extractBests(name, titles, scorer=custom_scorer, limit=count, score_cutoff=20)
    if len(results) == 0:
        return None

    title_to_index = {title: idx for idx, title in enumerate(titles)}
    best_titles, best_scores = zip(*results[:count])
    best_indices = [title_to_index[title] for title in best_titles]

    #best_index = np.argmax([result[1] for result in results])
    return list(best_indices), list(best_scores)