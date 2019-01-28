#!/usr/bin/python3

import pandas as pd

from pyspark import SparkContext
import wordbatch
from wordbatch.extractors import WordBag
from wordbatch.batcher import Batcher
import numpy as np


def normalize_text(text):
    """ Funcion de normalizacion """

    return text


print("Leyendo corpus de archivo PANDA ....")
# Lee todas las noticias que estan en un archivo PANDA
corpus = pd.read_pickle("corpus.pan")

# Elimino: Duplicados, Cuerpos con None, Cuerpos de largo <= 300
corpus.drop_duplicates(inplace= True)
corpus = corpus[ corpus['Cuerpo'].notnull() & (corpus['Cuerpo'].str.len()>2000) ]
corpus.reset_index(drop=True, inplace= True)

# Imprime cantiadad de noticias
print("Listo, cantidad de noticias....")
print(corpus.shape)

# Calculo TF-IDF
n_docs = len(corpus['Cuerpo'].tolist())
n_cpu = 2
batch_size = int(n_docs/n_cpu)
_n_words = 500

extractor=(WordBag, {"hash_ngrams": 1, "hash_ngrams_weights": [1.0, 1.0],\
                     "hash_size": 2**22, "norm": "l2", "tf": 1.0,"idf": 1.0})

wb = wordbatch.WordBatch(normalize_text,\
                         extractor= extractor,\
                         procs= n_cpu,\
                         minibatch_size= batch_size,\
                         use_sc=True)

#WORBBAG_ITEM_DESC_PARAMS = {'hash_ngrams': 2, 'hash_ngrams_weights': [1.0, 1.0],
#                            'hash_size': 2 ** 26, 'norm': 'l2', 'tf': 1.0, 'idf': None}
#wb = wordbatch.WordBatch(normalize_text, extractor=(WordBag, WORBBAG_ITEM_DESC_PARAMS),\
#                         procs= n_cpu)

#wb = wordbatch.WordBatch(normalize_text,\
#                         extractor= extractor, procs = n_cpu )
                         
#procs= n_cpu, n_words= 500, minibatch_size= batch_size)
sc = SparkContext()
wb.dictionary_freeze = True
#b = Batcher(procs=n_cpu, minibatch_size=batch_size, use_sc=True)

#lista = wb.lists2rddbatches(lists=[corpus['Cuerpo'].tolist()], sc=sc)
lists = [corpus['Cuerpo'].tolist()]
lista = sc.parallelize(lists)

## Funciona con transform, pero no con fit_transform... hay que ver el porque
X = wb.fit_transform(lists, reset= False)
wb.nonZeroIndex = np.array(np.clip(X.getnnz(axis=0) - 1, 0, 1), dtype = bool)
X = X[:, wb.nonZeroIndex]
# EJEMPLO
print("Ejemplo....")
#s0 = "En un partido muy deslucido y que sólo al final tuvo emociones, Audax Italiano sacó"
#documents = ["Human machine interface for lab abc computer applications",
#              "A survey of user opinion of computer system response time",
#              "The EPS user interface management system",
#              "System and human system engineering testing of EPS",
#              "Relation of user perceived response time to error measurement",
#              "The generation of random binary unordered trees",
#              "The intersection graph of paths in trees",
#              "Graph minors IV Widths of trees and well quasi ordering",
#              "Graph minors A survey"]
test_tfidf = wb.transform(documents)[:,wb.nonZeroIndex]
print(test_tfidf)