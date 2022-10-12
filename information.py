"""
Quantify the information content of a corpus of ontology terms.

@ ASLOUDJ Yanis
10/10/2022
"""


from math import exp
from skbio.diversity.alpha import shannon
import pandas as pd
import matplotlib.pyplot as plt


def 