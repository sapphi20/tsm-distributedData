# Instalación Cassandra
* Tener instalado java como se describió en la instalación de Hadoop
* Descargar y extraer Cassandra: https://www-us.apache.org/dist/cassandra/3.0.17/apache-cassandra-3.0.17-bin.tar.gz
* Mover carpeta a `/usr/local` (o al directorio de preferencia, ahora `$CASSANDRA_HOME`).
* Agregar a ~/.bashrc:

    ```
    export CASSANDRA_HOME=/usr/local/cassandra
    export PATH=$PATH:$CASSANDRA_HOME/bin
    ```

* En `$CASSANDRA_HOME/conf/cassandra.yaml` hay que editar los siguientes campos: 
   
    `seeds: "<lista de IP de los nodos que se conectarán, separados por coma>"` (sí va con las comillas)
    ```
    listen_address: < ip de la máquina actual>
    rpc_addres: < ip de la máquina actual>
    broadcast_rpc_address: < ip de la máquina actual>
    ```

* `cassandra start` inicia el nodo del cluster de la máquina actual y `cassandra stop` detiene el proceso en la máquina actual. 

## Cassandra-driver
Librería de python para manipular Cassandra desde Python.

### Instalación
`pip3 install cassandra-driver`

## Conector de Spark con Cassandra
Existe un conector de Spark con Cassandra creado por DataStax.
A partir de este se creó un port para que funcionara con Pyspark.
Si se ejecuta un script con `spark-submit` hay que hacerlo de la siguiente manera:

`spark-submit --packages anguenot:pyspark-cassandra:<version> --conf spark.cassandra.connection.host=<IPs del cluster de Cassandra separadas por comas> <nombre del script>.py`

Para más información ver:

[Spark-Cassandra Connector](https://github.com/datastax/spark-cassandra-connector)

[Pyspark Cassandra](https://github.com/anguenot/pyspark-cassandra)
