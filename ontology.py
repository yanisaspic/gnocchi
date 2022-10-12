"""
Save the relevant data to characterize the information content of a corpus of ontology terms.

@ ASLOUDJ Yanis
10/10/2022
"""


from math import log
from goatools.base import get_godag
from goatools.gosubdag.gosubdag import GoSubDag
import pandas as pd


### V A R S
ontologies = ['go-basic.obo', 'hp.obo']
onto_roots = {'BP': 'GO:0008150', 'MF': 'GO:0003674', 'CC': 'GO:0005575', 'human_phenotype': 'HP:0000001'}


### F U N C
def get_term_leaves(godag):
    """Return a dict associating an ontology term id (key) to its leaves (value)."""
    onto_leaves = set()
    for term in godag:
        children = godag[term].get_all_children()
        if len(children) == 0:
            onto_leaves.add(term)
    term_leaves = {}
    for term in godag:
        term_leaves[term] = onto_leaves.intersection(godag[term].get_all_children())
    return term_leaves

def get_term_data(gosubdag, go_id, term_leaves):
    """Return a dict associating an ontology term id (key) to its data (value).
    Duplicate GODag terms (alternate ids) are ignored.

    Data includes:
        > usage data: name, namespace.
        > hierarchy data: level, depth, descendants, leaves, subsumers."""
    term = gosubdag.go2nt[go_id]
    term_data = {term.id: {
        'name': term.GO_name,
        'namespace': term.NS,
        'descendants': term.dcnt + 1,  # descendants: nodes below term. (+1) to compute Shannon entropy
        'level': term.level,            # level: shortest path to term node from root
        'depth': term.depth,            # depth: longest path to term node from root
        'leaves': len(term_leaves[go_id])}}

    try:    # subsumers: nodes term, term included (+1).
        term_data[term.id]['subsumers'] = len(gosubdag.rcntobj.go2ancestors[term.id]) + 1
    except KeyError:
        term_data[term.id]['subsumers'] = 1
    return term_data

def get_onto_df(obo):
    """Return a dataframe associating the terms of a .obo ontology (rows) to their respective data (columns)."""
    onto_dict = {}
    godag = get_godag(obo)
    gosubdag = GoSubDag(list(godag.keys()), godag)
    term_leaves = get_term_leaves(godag)
    for go_id in list(godag.keys()):
        onto_dict.update(get_term_data(gosubdag, go_id, term_leaves))
    return pd.DataFrame.from_dict(onto_dict, orient='index').sort_values(by=['namespace', 'descendants'], ascending=False)

def get_ic_sanchez(onto_df):
    """Return a pandas Series corresponding to the Information Content (cf. Sanchez et al. 2011) of the terms in the ontology dataframe."""
    root_terms = onto_df.namespace.apply(lambda x: onto_roots[x])
    max_leaves = root_terms.apply(lambda x: onto_df.loc[x].leaves)
    a = (onto_df.leaves / onto_df.subsumers + 1) / (max_leaves + 1)
    return a.apply(lambda x: -log(x))


### M A I N
onto_df = pd.DataFrame()
for obo in ontologies:
    onto_df = pd.concat([onto_df, get_onto_df(obo)])
onto_df['sanchez'] = get_ic_sanchez(onto_df)
onto_df.to_csv('ontology_direct_data.csv')