#!/usr/bin/python3
from cassandra.cluster import Cluster

# Configuracion para conectar al cluster
# se pueden omitir algunos nodos
ips = ['192.168.101.140', '192.168.101.141', '192.168.101.142', '192.168.101.143']
cluster = Cluster(ips)

def insert_data():
	from cassandra.cluster import Cluster
	from cassandra import AlreadyExists
	# Conexion al cluster de Cassandra al keyspace "test"
	session = Cluster(['192.168.101.140', '192.168.101.141', '192.168.101.142', '192.168.101.143']).connect("test")
	try:
		# Primero crea la tabla
		session.execute("CREATE TABLE test1 (id int PRIMARY KEY, col1 text)")
		# Inserta datos 
		insertar = session.prepare("INSERT INTO test1 (id, col1) VALUES (?, ?)")
		for i in range(10):
			session.execute(insertar, (i, 'hola' + str(i)))
			print(i)
	except AlreadyExists:
		# Inserta datos a la tabla ya existente
		insertar = session.prepare("INSERT INTO test1 (id, col1) VALUES (?, ?)")
		for i in range(10):
			session.execute(insertar, (i, 'hola' + str(i)))
			print(i)
if __name__ == '__main__':
	insert_data()
