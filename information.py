"""
Quantify the information content of a corpus of ontology terms.

@ ASLOUDJ Yanis
10/10/2022
"""


from math import exp
from skbio.diversity.alpha import shannon
import pandas as pd
import matplotlib.pyplot as plt


### F U N C
def get_corpus_statistics(onto_df):
    """Returns a dict associating information describers based on Shannon entropy, Sanchez IC and the level and depth of the terms."""
    return {
        'shannon': shannon(onto_df.descendants),
        # 'mean_level': onto_df.level.mean(),
        # 'mean_level/depth': onto_df['level/depth'].mean(),
        'mean_sanchez': onto_df.sanchez.mean()
        # 'std_sanchez': onto_df.sanchez.std()
    }

def get_corpus_evolution(onto_df):
    """Returns a dict associating a decreasing corpus size to its information content."""
    corpus_evolution = {}
    while onto_df.shape[0]>1:
        corpus_evolution[onto_df.shape[0]] = get_corpus_statistics(onto_df)
        onto_df = onto_df.iloc[1:]
    corpus_df = pd.DataFrame.from_dict(corpus_evolution, orient='index')
    return (corpus_df - corpus_df.min()) / (corpus_df.max() - corpus_df.min())


### M A I N
fig, axs = plt.subplots(2, 2)
onto_df = pd.read_csv('ontology_direct_data.csv', index_col=0)
### BP
onto = onto_df[onto_df.namespace=='BP']
print(onto)
corpus_evolution = get_corpus_evolution(onto)
corpus_evolution.index = corpus_evolution.index.map(lambda x: 1 - x/corpus_evolution.index[0])
print(corpus_evolution)
corpus_evolution.plot(y=['shannon', 'mean_sanchez'], use_index=True, ax=axs[0, 0], title='BP')
### CC
onto = onto_df[onto_df.namespace=='CC']
corpus_evolution = get_corpus_evolution(onto)
corpus_evolution.index = corpus_evolution.index.map(lambda x: 1 - x/corpus_evolution.index[0])
corpus_evolution.plot(y=['shannon', 'mean_sanchez'], use_index=True, ax=axs[0, 1], legend=None, title='CC')
### MF
onto = onto_df[onto_df.namespace=='MF']
corpus_evolution = get_corpus_evolution(onto)
corpus_evolution.index = corpus_evolution.index.map(lambda x: 1 - x/corpus_evolution.index[0])
corpus_evolution.plot(y=['shannon', 'mean_sanchez'], use_index=True, ax=axs[1, 0], legend=None, title='MF')
### human_phenotype
onto = onto_df[onto_df.namespace=='human_phenotype']
corpus_evolution = get_corpus_evolution(onto)
corpus_evolution.index = corpus_evolution.index.map(lambda x: 1 - x/corpus_evolution.index[0])
corpus_evolution.plot(y=['shannon', 'mean_sanchez'], use_index=True, ax=axs[1, 1], legend=None, title='HPO')
plt.show()