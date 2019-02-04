from pyspark import SparkContext, SparkConf
from pyspark.mllib.feature import HashingTF, IDF
from pyspark.sql import SQLContext
from pyspark_cassandra import CassandraSparkContext, Row
sc = CassandraSparkContext()
sqlContext = SQLContext(sc)

# Carga una tabla en un keyspace a un Dataframe
def load_and_get_table_df(keys_space_name, table_name):
    table_df = sqlContext.read\
        .format("org.apache.spark.sql.cassandra")\
        .options(table=table_name, keyspace=keys_space_name)\
        .load()
    return table_df

# Inserta datos desde HDFS leidos con wholeTextFiles (para obtener pares llave-valor)
# en una tabla dentro del cluster de Cassandra
def insert_data(data):
	from cassandra.cluster import Cluster
	# Conexion al cluster de Cassandra al keyspace "test"
	session = Cluster(['192.168.101.140']).connect("test")
	try:
		# Inserta datos a la tabla ya existente
		insertar = session.prepare("INSERT INTO corpus (id, cuerpo) VALUES (?, ?)")
		for d in data.collect():
			session.execute(insertar, (d[0], d[1]))
	except:
		# Primero crea la tabla
		session.execute("CREATE TABLE corpus (id text PRIMARY KEY, cuerpo text)")
		# Luego inserta datos
		insertar = session.prepare("INSERT INTO corpus (id, cuerpo) VALUES (?, ?)")
		for d in data.collect():
			session.execute(insertar, (d[0], d[1]))

def tfidf(data):
	hashing = HashingTF()
	tf = hashing.transform(data)
	idf = IDF().fit(tf)
	tfidf = idf.transform(tf)

if __name__ == '__main__':
	rdd = sc.wholeTextFiles('hdfs:///user/hadoop/cooperativa/200910*')
	# Quita los textos vacios
	rdd = rdd.filter(lambda key: key[1] is not '')
	# Inserta filas a tablas en cassandra
	insert_data(rdd)
	# Carga la tabla en un dataframe
	tabla = load_and_get_table_df("test", "corpus")
	# Convierte dataframe a RDD
	tabla = tabla.rdd.map(tuple)
	# Comienza calculo de TF-IDF
	tfidf(tabla)
	for r in tfidf.collect():
		print(r)