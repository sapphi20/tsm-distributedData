# Instalación Spark
* Instalar Spark: https://archive.apache.org/dist/spark/spark-2.2.0/spark-2.2.0-bin-hadoop2.7.tgz
* Extraer el comprimido y mover carpeta a /usr/local (al igual que con Hadoop)
* Agregar a ~/.bashrc:
```
export SPARK_HOME=/usr/local/spark
export PATH=$SPARK_HOME/bin:$PATH
export LD_LIBRARY_PATH=/home/hadoop/hadoop/lib/native:$LD_LIBRARY_PATH
```
* Renombrar:
```mv /usr/local/spark/conf/spark-defaults.conf.template /usr/local/spark/conf/spark-defaults.conf```
* En `/usr/local/spark/conf/spark-env.sh` agregar:
```
export SPARK_LOCAL_IP=<IP de la máquina actual>
export SPARK_MASTER_HOST=<IP del master>
```

### Integrar Spark con YARN

* En spark-defaults.conf setear spark.master a "yarn" (sin las comillas). Por defecto trabaja en local.

### Instalar PySpark

Ejecutar `pip install pyspark`. Es una librería de python.
El comando pyspark abre una shell de python con la librería de pyspark ya importada. También se puede importar para hacer scripts (ejecutados con `spark-submit <nombre_script>.py`).
