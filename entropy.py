"""
Quantify the information content of a corpus of ontology terms using Shannon entropy.

@ ASLOUDJ Yanis
10/10/2022
"""


from goatools.base import get_godag
from goatools.gosubdag.gosubdag import GoSubDag
import pandas as pd

from skbio.diversity.alpha import shannon
from math import exp
import matplotlib.pyplot as plt


def get_term_leaves(gosubdag, go_id):
    return

def get_term_data(gosubdag, go_id):
    """Return a dict associating an ontology term id (key) to its data (value).
    Duplicate GODag terms (alternate ids) are ignored.

    Data includes:
        > usage data: name, namespace.
        > hierarchy data: level, depth, descendants, leaves, subsumers."""
    term = gosubdag.go2nt[go_id]
    term_data = {term.id: {
        'name': term.GO_name,
        'namespace': term.NS,
        'level': term.level,            # level: shortest path to term node from root
        'depth': term.depth,            # depth: longest path to term node from root
        'descendants': term.dcnt + 1}}  # descendants: nodes below term. (+1) to compute Shannon entropy

    # subsumers: nodes term, term included (+1).
    try:
        term_data[term.id]['subsumers'] = len(gosubdag.rcntobj.go2ancestors[term.id])
    except KeyError:
        term_data[term.id]['subsumers'] = 0
    term_data[term.id]['subsumers'] += 1

    return term_data

def get_onto_df(ontology):
    """Return a dataframe associating the terms of an ontology (rows) to their respective data (columns)."""
    onto_dict = {}
    godag = get_godag(ontology)
    go_ids_selected = (list(godag.keys()))
    gosubdag = GoSubDag(go_ids_selected, godag)
    for go_id in go_ids_selected:
        onto_dict.update(get_term_data(gosubdag, go_id))
    return pd.DataFrame.from_dict(onto_dict, orient='index')

onto_df = get_onto_df('go-basic.obo')
print(onto_df)

# check if removing the most frequent terms increase Shannon entropy / check terms
l_entropy = []
l_terms = []
n_terms_total = len(test_corpus)
print(n_terms_total)
best_entropy = exp(shannon(test_corpus))
curr_entropy = best_entropy
l_entropy.append(curr_entropy)
l_terms.append(1-len(test_corpus)/n_terms_total)
while len(test_corpus)>1:
    test_corpus.pop(0)
    curr_entropy = exp(shannon(test_corpus))
    l_entropy.append(curr_entropy)
    l_terms.append(1-len(test_corpus)/n_terms_total)


# display the behavior of the Shannon entropy 
plt.plot(l_terms, l_entropy)
plt.show()