"""
Quantify the informativeness of a corpus using Shannon entropy.

@ ASLOUDJ Yanis
10/10/2022
"""


from goatools.base import get_godag
from goatools.gosubdag.gosubdag import GoSubDag
from skbio.diversity.alpha import shannon
from math import exp
import matplotlib.pyplot as plt


def sanchez():
    """
    Return the IC score of an ontology term as proposed by Sanchez et al. (2011)
    """

# get a dict associating each term to its absolute frequency
godag = get_godag('go-basic.obo')
go_ids_selected = list(godag.keys())
gosubdag = GoSubDag(go_ids_selected, godag)
nts = [gosubdag.go2nt[go] for go in go_ids_selected]

corpus = {}

for term in nts:
    namespace = term.NS
    corpus[term.GO_name] = term.dcnt + 1
    try:
        print(gosubdag.rcntobj.go2ancestors[term.id])
    except KeyError:
        
test_corpus = list(corpus.values())
test_corpus.sort(reverse=True)


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