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
    rpc_address: < ip de la máquina actual>
    broadcast_rpc_address: < ip de la máquina actual>
    ```
* Crear carpetas para data y commit logs:
    ```
    mkdir /var/lib/cassandra

    mkdir /var/log/cassandra
    ```

* `cassandra start` inicia el nodo del cluster de la máquina actual y `cassandra stop` detiene el proceso en la máquina actual (si no funciona, terminar proceso con `kill -9 <pid>`). 
* Para acceder al shell de Cassandra hay que escribir el siguiente comando: 
`cqlsh <IP que pertenezca al cluster al que se quiere conectar>`

## Multiples datacenter en Cassandra
* En `$CASSANDRA_HOME/conf/cassandra-rackdc.properties` (en cada nodo): Todos los nodos que pertenezcan al mismo datacenter deben tener el mismo nombre de datacenter, el rack no necesariamente es el mismo.
    
    `dc=<nombre datacenter>`

    `rack=rack1 (o el numero de rack que tenga)`

* En `$CASSANDRA_HOME/conf/cassandra-topology.properties`: Cada línea va con el siguiente formato -> `Cassandra Node IP=Data Center:Rack`. Por ejemplo:
    ```
    192.168.101.140=DC1:RAC1
    192.168.101.141=DC1:RAC1
    192.168.101.142=DC2:RAC1
    192.168.101.143=DC2:RAC1
    ```
* En `$CASSANDRA_HOME/conf/cassandra.yaml`:
Cambiar `endpoint_snitch` a `GossipingPropertyFileSnitch` (carga el archivo `cassandra-topology.properties` cuando está disponible).
* En la ubicación donde se definió `data_file_directories`
rm -rf `$CASSANDRA_DATA/data/system/*`
* Luego se reinicia el nodo para ver los cambios aplicados

# Cassandra-driver
Librería de python para manipular Cassandra desde Python.

### Instalación
`pip3 install cassandra-driver`

# Conector de Spark con Cassandra
Existe un conector de Spark con Cassandra creado por DataStax.
A partir de este se creó un port para que funcionara con Pyspark.
Si se ejecuta un script con `spark-submit` hay que hacerlo de la siguiente manera:

`spark-submit --packages anguenot:pyspark-cassandra:<version> --conf spark.cassandra.connection.host=<IPs del cluster de Cassandra separadas por comas> <nombre del script>.py`

Para más información ver:

[Spark-Cassandra Connector](https://github.com/datastax/spark-cassandra-connector)

[Pyspark Cassandra](https://github.com/anguenot/pyspark-cassandra)

# Sobre comandos en cqlsh

### ALTER KEYSPACE
Se puede cambiar el factor de replicación con `ALTER KEYSPACE <nombre> WITH REPLICATION = {'class': '<nombre:estrategia>', <opciones>}` donde las estrategias son `SimpleStrategy` (el mismo factor para todos los nodos) y `NetworkTopology` (cada datacenter tiene su propia replicación).

Hay que ejecutar `nodetool status -full` en cada nodo afectado después de cambiar la replicación.

El factor de replicación se ve afectado en el porcentaje de dominio (`Owns (effective`) que se muestra al ejecutar `nodetool status`. La suma de los porcentajes indica el factor de replicación, es decir, si suman 300% entonces el factor de replicación es 3.

### CREATE TABLE
Se crea una tabla de la siguiente forma:
```
CREATE TABLE < nombre_tabla> (
    col_1 type_1,
    ...,
    col_n type_n,
    PRIMARY KEY (pk1, ..., pkm)
    );
```
