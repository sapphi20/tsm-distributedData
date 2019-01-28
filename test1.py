#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import pandas as pd

import wordbatch
from wordbatch.extractors import WordBag, WordHash
from wordbatch.models import FTRL
from wordbatch.batcher import Batcher
from pyspark import SparkContext, SparkConf
import numpy as np




def normalize_text(text):
    """ Funcion de normalizacion """

    return text

    # Get plain text from HTML
    ##soup = BeautifulSoup(text, 'html.parser')
    
    # kill all script and style elements
    ##for script in soup(["script", "style"]):
    ##    script.extract()    # rip it out    
    
    # get text
    ##text = soup.get_text()
    
    # break into lines and remove leading and trailing space on each
    #lines = (line.strip() for line in text.splitlines())
    # break multi-headlines into a line each
    #chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    # drop blan
    #k lines
    #text = '\n'.join(chunk for chunk in chunks if chunk)
    
    # split into words
    ##tokens = nltk.tokenize.word_tokenize(text,language='spanish', preserve_line=False)
    # convert to lower case
    ##tokens = [w.lower() for w in tokens]    
    
    # remove punctuation from each word
    ##table = str.maketrans('', '', string.punctuation)
    ##stripped = [w.translate(table) for w in tokens]
    
    # remove remaining tokens that are n<<<<<<<<<<<<<<<<<<<<<
    ##words = [word for word in stripped if word.isalpha()]
    
    # stop word and remove accent
    ##def strip_accents(s):
    ##    return ''.join(c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn')
    ##stop_words = set(spanish_stopwords)
    ##words = [strip_accents(w) for w in words if not w in stop_words]
    
    # Lematizar
    ##wordsLem = []
    ##stemmer = SnowballStemmer("spanish")
    ##out = ""
    ##for word in words:
        #out += stemmer.stem(word)+" "
    ##    wordsLem.append(stemmer.stem(word))
    
    ##return u" ".join(wordsLem)





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
                         minibatch_size= batch_size)

#WORBBAG_ITEM_DESC_PARAMS = {'hash_ngrams': 2, 'hash_ngrams_weights': [1.0, 1.0],
#                            'hash_size': 2 ** 26, 'norm': 'l2', 'tf': 1.0, 'idf': None}
#wb = wordbatch.WordBatch(normalize_text, extractor=(WordBag, WORBBAG_ITEM_DESC_PARAMS),\
#                         procs= n_cpu)

#wb = wordbatch.WordBatch(normalize_text,\
#                         extractor= extractor, procs = n_cpu )
                         
#procs= n_cpu, n_words= 500, minibatch_size= batch_size)
#wb.use_sc = True
wb.dictionary_freeze = True
# b = Batcher(procs=n_cpu, minibatch_size=batch_size, use_sc=True)
# lista = pd.DataFrame([corpus['Cuerpo'].tolist()])
# lista = b.lists2rddbatches(lists=[corpus['Cuerpo'].tolist()], sc=sc)
# lista = lista.toDF()

## Funciona con transform, pero no con fit_transform... hay que ver el porque
X = wb.fit_transform(corpus['Cuerpo'].tolist(), reset= False)
wb.nonZeroIndex = np.array(np.clip(X.getnnz(axis=0) - 1, 0, 1), dtype = bool)
X = X[:, wb.nonZeroIndex]
# EJEMPLO
print("Ejemplo....")
#s0 = "En un partido muy deslucido y que sólo al final tuvo emociones, Audax Italiano sacó"
documents = ["Human machine interface for lab abc computer applications",
              "A survey of user opinion of computer system response time",
              "The EPS user interface management system",
              "System and human system engineering testing of EPS",
              "Relation of user perceived response time to error measurement",
              "The generation of random binary unordered trees",
              "The intersection graph of paths in trees",
              "Graph minors IV Widths of trees and well quasi ordering",
              "Graph minors A survey"]
test_tfidf = wb.transform(documents)[:,wb.nonZeroIndex]
print(test_tfidf)
