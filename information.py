"""
Quantify the information content of a corpus of ontology terms.

@ ASLOUDJ Yanis
10/10/2022
"""


from math import exp
from skbio.diversity.alpha import shannon
from goatools.base import get_godag
from goatools.gosubdag.gosubdag import GoSubDag
from goatools.godag_plot import plot_gos
from sys import stdout
import pandas as pd
import matplotlib.pyplot as plt


### F U N C
def get_corpus_statistics(onto_df):
    """Returns a dict associating information describers based on Shannon entropy, Sanchez IC and the level and depth of the terms."""
    return {
        'shannon': shannon(onto_df.descendants),
        # 'mean_level': onto_df.level.mean(),
        # 'mean_level/depth': onto_df['level/depth'].mean(),
        'sanchez': onto_df.sanchez.mean()
        # 'std_sanchez': onto_df.sanchez.std()
    }

def save_ontology(filename, godag):
    """save an ontology file."""
    ontology = open(filename, 'wt')
    ontology.write('format-version: 1.2\n\n')
    for term in godag:
        ontology.write('[Term]\n')
        ontology.write(f'id: {term}\n')
        ontology.write(f'name: {godag[term].name}\n')
        for parent in godag[term]._parents:
            try:
                ontology.write(f'is_a: {parent} ! {godag[parent].name}\n')
            except KeyError:
                pass
        ontology.write('\n')
    

def get_corpus_evolution(onto_df):
    """Returns a dict associating a decreasing corpus size to its information content."""
    corpus_evolution = {}
    while onto_df.shape[0]>1:
        corpus_evolution[onto_df.shape[0]] = get_corpus_statistics(onto_df)
        onto_df = onto_df.iloc[1:]
    corpus_df = pd.DataFrame.from_dict(corpus_evolution, orient='index').applymap(lambda x: exp(x))
    corpus_df = (corpus_df - corpus_df.min()) / (corpus_df.max() - corpus_df.min())
    corpus_df['dist'] = abs(corpus_df['shannon'] - corpus_df['sanchez'])
    corpus_df['delta'] = corpus_df['delta']
    return corpus_df

# ### M A I N
onto_df = pd.read_csv('ontology_direct_data.csv', index_col=0)
onto = onto_df[onto_df.namespace=='BP']
corpus_evolution = get_corpus_evolution(onto)
n_terms = corpus_evolution[corpus_evolution.dist == corpus_evolution.dist.min()].index[0]
removed_terms = set(onto.iloc[:-n_terms].index)
godag = get_godag('go-basic.obo')

deep_terms = set(removed_terms).intersection(set(godag.keys()))
for term in deep_terms:
    x=godag.pop(term)
save_ontology('saved.obo', godag)

# fig, axs = plt.subplots(2, 2)
# ### BP
# onto = onto_df[onto_df.namespace=='BP']
# corpus_evolution = get_corpus_evolution(onto)
# corpus_evolution.index = corpus_evolution.index.map(lambda x: 1 - x/corpus_evolution.index[0])
# corpus_evolution.plot(y=['shannon', 'mean_sanchez'], use_index=True, ax=axs[0, 0], title='BP')
# ### CC
# onto = onto_df[onto_df.namespace=='CC']
# corpus_evolution = get_corpus_evolution(onto)
# corpus_evolution.index = corpus_evolution.index.map(lambda x: 1 - x/corpus_evolution.index[0])
# corpus_evolution.plot(y=['shannon', 'mean_sanchez'], use_index=True, ax=axs[0, 1], legend=None, title='CC')
# ### MF
# onto = onto_df[onto_df.namespace=='reactome']
# corpus_evolution = get_corpus_evolution(onto)
# corpus_evolution.index = corpus_evolution.index.map(lambda x: 1 - x/corpus_evolution.index[0])
# corpus_evolution.plot(y=['shannon', 'mean_sanchez'], use_index=True, ax=axs[1, 0], legend=None, title='reactome')
# ### human_phenotype
# onto = onto_df[onto_df.namespace=='human_phenotype']
# corpus_evolution = get_corpus_evolution(onto)
# corpus_evolution.index = corpus_evolution.index.map(lambda x: 1 - x/corpus_evolution.index[0])
# corpus_evolution.plot(y=['shannon', 'mean_sanchez'], use_index=True, ax=axs[1, 1], legend=None, title='HPO')
# plt.show()