import sys
 
from pyspark import SparkContext, SparkConf
 
if __name__ == "__main__":
 
  # create Spark context with Spark configuration
  # conf = SparkConf().setAppName("Word Count - Python").set("spark.hadoop.yarn.resourcemanager.address", "192.168.101.140:8032")
  print(sys.version_info)
  sc = SparkContext()

  # read in text file and split each document into words
  words = sc.textFile("/user/hadoop/input.txt").flatMap(lambda line: line.split(" "))
 
  # count the occurrence of each word
  wordCounts = words.map(lambda word: (word, 1)).reduceByKey(lambda a,b:a +b)
 
  wordCounts.saveAsTextFile("/user/hadoop/output/") 
