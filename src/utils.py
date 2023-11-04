from rapidfuzz import fuzz, process, utils as fuzz_utils

import numpy as np
import re

def full_process(s):
    return re.sub(r'\W', '', s.lower())

def to_lower(s):
    return s.lower()

def remove_brackets(text):
    return re.sub(r'\[.*?\]', '', text).strip()

def loose_scorer(query: str, choice: str, score_cutoff: bool = None):
    exact_match_bonus = 1000  # Some high value to ensure exact matches are prioritized
    # Check for exact match
    if query == choice:
        return exact_match_bonus
    
    return fuzz.partial_ratio(query, choice, processor=to_lower)
    
    
def strict_scorer(query: str, choice: str, score_cutoff: bool = None):
    exact_match_bonus = 1000  # Some high value to ensure exact matches are prioritized
    
    # TODO: Maybe move this after exact match check, in case this is not wanted for exact matches
    query = remove_brackets(query)
    choice = remove_brackets(choice)

    # Check for exact match
    if query == choice:
        return exact_match_bonus

    score = fuzz.token_sort_ratio(query, choice, processor = fuzz_utils.default_process)
    
    length_difference = abs(len(query) - len(choice))
    if length_difference < 10:
        return score
    
    token_set_ratio = fuzz.token_set_ratio(query, choice, processor = fuzz_utils.default_process)
    print("token set ratio:", token_set_ratio)
    #if token_set_ratio > 80:
    partial = (fuzz.partial_token_sort_ratio(query, choice, processor = fuzz_utils.default_process) - length_difference * 0.2)
    print("partial score:", partial)
    score = 0.25 * score + 0.75 * partial
        
    return score
    
    # + fuzz.ratio(query, choice)  #partial_ratio
    #score = fuzz.WRatio(query, choice, score_cutoff=score_cutoff) - length_penalty * 0.1
    # base = fuzz.ratio(query, choice, processor=to_lower)
    # tsr = fuzz.token_sort_ratio(query, choice, processor=to_lower)
    # partial = fuzz.partial_ratio(query, choice, processor=to_lower) - length_difference * 0.2
    # ptsr = fuzz.partial_token_sort_ratio(query, choice, processor=to_lower) - length_difference * 0.2
    #fuzz.partial_ratio_alignment
    
    #print(query + " - " + choice + ":\t\tscores - base: ", base, " tsr: ", tsr, " parptsrtial: ", partial, " ptsr: ", ptsr, " tsetr: ", tsetr)
    #return max(base, tsr, partial, ptsr) # base + tsr + partial + ptsr

# get best match from search in a list:
def best_match(name, titles, count = 1):
    # print("all titles:", titles)
    results = process.extract(name, titles, scorer=strict_scorer, limit=count)#, score_cutoff=50)
    if len(results) == 0:
        return None

    #print("results:", results)

    #title_to_index = {title: idx for idx, title in enumerate(titles)}
    best_titles, best_scores, best_indices = zip(*results[:count])
    #best_indices = [title_to_index[title] for title in best_titles]

    #best_index = np.argmax([result[1] for result in results])
    return list(best_indices), list(best_scores)


def match_mods(*mods):
    # throw error, if only one mod is given:
    if len(mods) < 2:
        raise ValueError("At least two mods must be given")
    
    # calculates single score for two mods or mod lists
    elif len(mods) == 2:
        mod0 = mods[0]
        mod1 = mods[1]
        
        # calculate score matrix for one or two mod lists
        if isinstance(mod0, list) or isinstance(mod1, list):
            # convert both to a list, if they are not lists already:
            mod0 = mods[0] if isinstance(mods[0], list) else [mods[0]]
            mod1 = mods[1] if isinstance(mods[1], list) else [mods[1]]
            
            scores =  np.zeros((len(mod0), len(mod1)))
            for i in range(len(mod0)):
                for j in range(len(mod1)):
                    scores[i,j] = strict_scorer(mod0[i].name, mod1[j].name)
            return scores               
        
        # calculate score for two mods
        else:
            score = strict_scorer(mod0.name, mod1.name)
            return score
    
    # calculate score matrix for multiple mods
    else:
        # Iterate over all combination of mods and calculate a score:
        scores = np.zeros((len(mods), len(mods)))
        for i in range(len(mods)):
            for j in range(i+1, len(mods)):
                # calculate score
                score = strict_scorer(mods[i].name, mods[j].name)
                scores[i, j] = score
                scores[j, i] = score
                
        return scores
        