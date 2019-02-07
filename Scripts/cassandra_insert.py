#!/usr/bin/python3
import random
from cassandra.cluster import Cluster
from pyspark import SparkContext

# Configuracion para conectar al cluster
# se pueden omitir algunos nodos
ips = ['192.168.101.140', '192.168.101.141', '192.168.101.142', '192.168.101.143']
cluster = Cluster(ips)

def insert_data(data):
	from cassandra.cluster import Cluster
	from cassandra import AlreadyExists
	# Conexion al cluster de Cassandra al keyspace "test"
	session = Cluster(['192.168.101.140', '192.168.101.141', '192.168.101.142', '192.168.101.143']).connect("test")
	try:
		# Primero crea la tabla
		session.execute("CREATE TABLE cooperativa (id text PRIMARY KEY, cuerpo text)")
		# Inserta datos 
		insertar = session.prepare("INSERT INTO cooperativa (id, cuerpo) VALUES (?, ?)")
		for d in data.collect():
			session.execute(insertar, (d[0], d[1]))
	except AlreadyExists:
		# Inserta datos a la tabla ya existente
		insertar = session.prepare("INSERT INTO cooperativa (id, cuerpo) VALUES (?, ?)")
		for d in data.collect():
			session.execute(insertar, (d[0], d[1]))

if __name__ == '__main__':
	sc = SparkContext()
	rdd = sc.wholeTextFiles('hdfs:///user/hadoop/cooperativa/2015*')
	# Quita los textos vacios
	rdd = rdd.filter(lambda key: key[1] is not '')
	insert_data(rdd)