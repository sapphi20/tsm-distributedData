# Scripts para procesamiento de datos

Algunas cosas que realicé para la práctica 1 en TecnoSmart SpA.

### Test

Contiene dos videos con pruebas de Spark con Hadoop y un log de ejemplo:

* `test_tfidf.mp4`: Prueba de script con Spark en Python para las noticias del 1 de enero de 2014 de diario Cooperativa obtenidos a partir de un corpus de pandas. Se usó para ver el consumo de CPU, memoria RAM y tráfico de red entre los datanodes.
* `test_tfidf_2.mp4`: Lo mismo que el video
* `log_test_1.txt`: Registro de Spark + prints del script copiados desde lo obtenido en la terminal por la salida estándar.

También hay un video de prueba (`test_cassandra1.mp4`) donde se calcula TF-IDF viendo el rendimiento en `htop` y `bmon`.

### Scripts

* `corpus_to_hdfs.py`: Script que transforma el corpus de noticias de diario Cooperativa a varios archivos que son almacenados en el sistema de archivos distribuido de Hadoop. Utiliza `Beautiful Soup` para quitar los tags de HTML y `pyspark` para traspasar los datos al DFS.
* `test1.py`: Script con Wordbatch para TF-IDF (no distribuido)
* `tfidf_wordbatch.py`: Intento de script utilizando Wordbatch con Spark. No funciona.
* `tfidf.py`: Script que realiza cálculos, sobre Apache Spark, de TF-IDF con el módulo `mllib` de `pyspark`. Esto fue antes de empezar a usar Cassandra, así que obtiene los datos de Hadoop.
* `cassandra_insert.py`: Script de prueba que utiliza `cassandra-driver` para insertar datos a Cassandra.
* `tfidf_cassandra.py`: Script que realiza cálculo de TF-IDF con Spark sobre Cassandra. También guarda los resultados en un archivo de `pandas`.
* `wordcount.py`: Ejemplo simple de uso de pyspark.

### Readme

Contiene instrucciones para instalar y configurar Hadoop, Spark y Cassandra.