# Configuratins related to Cassandra connector & Cluster
import os
from pyspark import SparkContext
from pyspark.sql import SQLContext

os.environ['PYSPARK_SUBMIT_ARGS'] =\
'--packages com.datastax.spark:spark-cassandra-connector_2.11:2.3.0\
--conf spark.cassandra.connection.host=192.168.101.140, 192.168.101.141,\
192.168.101.142, 192.168.101.143 pyspark-shell'

sc = SparkContext("local", "movie lens app")
sqlContext = SQLContext(sc)

# Loads and returns data frame por a table including key space given
def load_and_get_table_df(keys_space_name, table_name):
    table_df = sqlContext.read\
        .format("org.apache.spark.sql.cassandra")\
        .options(table=table_name, keyspace=keys_space_name)\
        .load()
    return table_df

movies = load_and_get_table_df("movie_lens", "movies")
ratings = load_and_get_table_df("movie_lens", "ratings")

movies.show()