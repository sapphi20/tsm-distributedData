import pandas as pd
from bs4 import BeautifulSoup
from pyspark import SparkContext

pd.options.display.max_colwidth = 100
sc = SparkContext()

corpus = pd.read_pickle('corpus.pan')
# Elimina duplicados, Cuerpos con None, Cuerpos de largo mayor a 2000
corpus.drop_duplicates(inplace= True)
corpus = corpus[ corpus['Cuerpo'].notnull() & (corpus['Cuerpo'].str.len()>2000) ]

#solo tiene la ID y el cuerpo de la noticia
corpus = corpus[['ID', 'Cuerpo']]

for i in range(0, corpus.shape[0]):
    try:
        id_noticia = corpus['ID'].tolist()[i]
        print('Copiando noticia %s' %id_noticia)
        dir_archivo = 'hdfs:///user/hadoop/cooperativa/%s' % id_noticia
        c = corpus['Cuerpo'].tolist()[i]
        # soup = BeautifulSoup(c, 'html.parser')
        # Texto sin tags de HTML se pasa a un RDD de spark
        cuerpo = sc.parallelize([soup.get_text()]) #cuerpo de la noticia sin tags
        cuerpo.saveAsTextFile(dir_archivo)
    except:
        continue
