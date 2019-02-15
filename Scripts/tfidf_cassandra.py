#!/usr/bin/python3
from pyspark import SparkContext
from pyspark.mllib.feature import HashingTF, IDF
from pyspark.sql import SQLContext
from pyspark_cassandra import CassandraSparkContext, Row
import pandas

# Configuracion
sc = CassandraSparkContext()
sqlContext = SQLContext(sc)

# Carga una tabla en un keyspace determinado
# retorna un dataframe (que después se puede pasar a un RDD)
def load_and_get_table_df(keys_space_name, table_name):
    table_df = sqlContext.read\
        .format("org.apache.spark.sql.cassandra")\
        .options(table=table_name, keyspace=keys_space_name)\
        .load()
    return table_df

# Convierte datos de un RDD a un DataFrame
def rdd_to_df(data):
	new_data = data.map(lambda row: (row, ))
	return sqlContext.createDataFrame(new_data)

# Pasos que procesan data para el calculo de tfidf
def tfidf(data):
	hashing = HashingTF()
	tf = hashing.transform(data)
	idf = IDF().fit(tf)
	tfidf = idf.transform(tf)
	return tfidf

if __name__ == '__main__':
	# Carga la tabla en un dataframe
	tabla = load_and_get_table_df("test", "cooperativa")
	# Convierte dataframe a RDD y quita los saltos de linea
	tabla = tabla.rdd.map(tuple).map(lambda line: line[1])
	# Nos deja con solo los cuerpos de las noticias
	# Comienza calculo de TF-IDF
	tfidf = tfidf(tabla)
	#Convierte RDD a DataFrame de spark
	tfidf_df = rdd_to_df(tfidf)
	# Convierte el DataFrame a uno de pandas
	tfidf_pd = tfidf_df.toPandas()
	# Guarda el pandas a un pickle
	tfidf_pd.to_pickle("tfidf.pkl")
