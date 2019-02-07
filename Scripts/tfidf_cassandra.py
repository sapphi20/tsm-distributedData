#!/usr/bin/python3
from pyspark import SparkContext, SparkConf
from pyspark.mllib.feature import HashingTF, IDF
from pyspark.sql import SQLContext
from pyspark_cassandra import CassandraSparkContext, Row

# Configuracion
sc = CassandraSparkContext()
sqlContext = SQLContext(sc)
'''
# Carga una tabla en un keyspace a un Dataframe
def load_and_get_table_df(keys_space_name, table_name):
    table_df = sqlContext.read\
        .format("org.apache.spark.sql.cassandra")\
        .options(table=table_name, keyspace=keys_space_name)\
        .load()
    return table_df
'''
# Inserta datos desde HDFS leidos con wholeTextFiles (para obtener pares llave-valor)
# en una tabla dentro del cluster de Cassandra



if __name__ == '__main__':
	rdd = sc.wholeTextFiles('hdfs:///user/hadoop/cooperativa/2012*')
	# Quita los textos vacios
	rdd = rdd.filter(lambda key: key[1] is not '')
	# Inserta filas a tablas en cassandra
	# insert_data(rdd)
	
	# Carga la tabla en un dataframe
	###tabla = load_and_get_table_df("test", "corpus")
	tabla = sc.cassandraTable("test", "cooperativa")
	# Convierte dataframe a RDD y quita los saltos de linea
	#tabla = tabla.rdd.map(tuple)
	print(type(tabla))
	'''
	# Comienza calculo de TF-IDF
	hashing = HashingTF()
	tf = hashing.transform(tabla)
	idf = IDF().fit(tf)
	tfidf = idf.transform(tf)

	for r in tfidf.collect():
		print(r)
	'''