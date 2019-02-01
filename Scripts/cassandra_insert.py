#!/usr/bin/python3
import random
from cassandra.cluster import Cluster

# Configuracion para conectar al cluster
# se pueden omitir algunos nodos
ips = ['192.168.101.140', '192.168.101.141', '192.168.101.142', '192.168.101.143']
cluster = Cluster(ips)

if __name__ == '__main__':
	# Establece conexion con una sesion
	# connect toma un argumento opcional con el keyspace a eleccion
	session = cluster.connect('test')
	rand_list = [random.randint(0, 100) for i in range(100)]
	# El metodo execute ejecuta queries
	for j in range(100):
		session.execute("INSERT INTO test1 (col1, col2) VALUES (%(col1)s, %(col2)s)"
			,{'col1': str(j), 'col2': rand_list[j]})