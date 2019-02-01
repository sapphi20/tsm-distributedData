# Configuratins related to Cassandra connector & Cluster
# import os
# Esto funcionaba con 1 IP, no sé si con varias
# os.environ['PYSPARK_SUBMIT_ARGS']='--packages com.datastax.spark:spark-cassandra-connector_2.11:2.3.0 --conf spark.cassandra.connection.host=192.168.101.140 pyspark-shell'
from pyspark import SparkContext, SparkConf
from pyspark.sql import SQLContext
#from pyspark_cassandra import CassandraSparkContext, Row
sc = SparkContext()
sqlContext = SQLContext(sc)

def load_and_get_table_df(keys_space_name, table_name):
    table_df = sqlContext.read\
        .format("org.apache.spark.sql.cassandra")\
        .options(table=table_name, keyspace=keys_space_name)\
        .load()
    return table_df

test1 = load_and_get_table_df("test", "test1")
test1.show()

