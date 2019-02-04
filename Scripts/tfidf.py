#!/usr/bin/python3

import pandas as pd

from pyspark import SparkContext
from pyspark.mllib.feature import HashingTF, IDF

import numpy as np


# Inicializa SparkContext
sc = SparkContext()

# Se lee un directorio que contiene una noticia (prueba)
# Tal vez podría seleccionar todo el directorio:
# sc.wholeTextFiles('hdfs:///user/hadoop/cooperativa')
rdd = sc.wholeTextFiles('hdfs:///user/hadoop/cooperativa/200910*')
#print("Reading directory: '2 de enero de 2014'")
print(rdd.collect()[0])
# Se filtran las tuplas con texto vacio
# y los textos se separan para obtener arreglos de palabras 
#rdd_filtered = rdd.filter(lambda key: key[1] is not '').map(lambda line: line[1].split(" "))
print("Start data filter")
rdd2_filtered = rdd.filter(lambda key: key[1] is not '').map(lambda line: line[1].split(" "))
print("End data filter")
hashing = HashingTF()
#Transforms the input document (list of terms) to term frequency vectors
# or transform the RDD of document to RDD of term frequency vectors.
print("Start computing Term Frequency Vectors")
test_tf = hashing.transform(rdd)
print("End computing Term Frequency Vectors")
# Computes the inverse document frequency
print("Start computing IDF")
test_idf = IDF().fit(test_tf)
test_tfidf = test_idf.transform(test_tf)
print("End computing IDF")

print("Vectors:")
for r in test_tfidf.collect():
    print(r)
