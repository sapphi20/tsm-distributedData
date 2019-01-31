# Instalación Hadoop
* Instalar java-jdk (de preferencia Java 1.8):
	`sudo apt-get install default-jdk`
* Descargar hadoop common: http://apache.forsale.plus/hadoop/common/hadoop-2.9.0/hadoop-2.9.0.tar.gz
* Extraer hadoop-2.9.0.tar.gz -> mover a `/usr/local/hadoop`
* (agregar en namenode)- /etc/hosts --> agregar IPs y usuarios de nodos
* /etc/hostname poner nombre dominio nodo. (para cada nodo es diferente).
* En `/usr/local/hadoop/etc/hadoop/hadoop-env.sh`:
`export JAVA_HOME=/usr/lib/jvm/java-7-openjdk-amd64` (con nombre de directorio java)
* `~/.bashrc` --> agregar al path de root el directorio de java/bin (para poder correr jps):
    
    ```
    export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64
    export PATH=$JAVA_HOME/bin:$PATH
    ```

### HADOOP Variables (en ~/.bashrc, para todas las máquinas)
```
export HADOOP_HOME=/usr/local/hadoop
export HADOOP_CONF_DIR=$HADOOP_HOME/etc/hadoop
export HADOOP_DATA_HOME=$HADOOP_HOME/hadoop_data/hdfs
PATH=$PATH:$HADOOP_HOME/bin:$HADOOP_HOME/sbin
```
### Configuración archivos .xml (aplica para todos los nodos, ya sean master o slave):

* `/usr/local/hadoop/etc/hadoop/core-site.xml`: 
```xml
    <configuration>
        <property>
            <name>fs.defaultFS</name>
            <value>hdfs://masterNodo:9000</value>
        </property>
    </configuration>
```
* `/usr/local/hadoop/etc/hadoop/hdfs-site.xml`:
```xml
    <configuration>
        <property>
            <name>dfs.replication</name>
            <value>3</value>
        </property>
        <property>
            <name>dfs.namenode.name.dir</name>
            <value>/usr/local/hadoop/hadoop_data/hdfs/namenode</value>
        </property>
        <property>
            <name>dfs.datanode.data.dir</name>
            <value>/usr/local/hadoop/hadoop_data/hdfs/datanode</value>
        </property>
    </configuration>
```
* `/usr/local/hadoop/etc/hadoop/yarn-site.xml`:
```xml
    <configuration>
        <property>
            <name>yarn.nodemanager.aux-services</name>
            <value>mapreduce_shuffle</value>
        </property>
        <property>
            <name>yarn.nodemanager.aux-services.mapreduce.shuffle.class</name>
            <value>org.apache.hadoop.mapred.ShuffleHandler</value>
        </property>
        <property>
            <name>yarn.resourcemanager.resource-tracker.address</name>
            <value>dominioNodoMaster:8025</value>      
        </property>
        <property>
            <name>yarn.resourcemanager.scheduler.address</name>
            <value>dominioNodoMaster:8030</value>      
        </property>
        <property>
            <name>yarn.resourcemanager.address</name>
            <value>dominioNodoMaster:8050</value>       
        </property>
    </configuration>
```
* `/usr/local/hadoop/etc/hadoop/mapred-site.xml` (copiar de `mapred-site.xml.template`):

```xml
<configuration>
    <property>
        <name>mapred.job.tracker</name>
        <value>masterNodo:54311</value>           
    </property>
</configuration>
```
* En nameNode:
    - `/usr/local/hadoop/etc/hadoop/masters` poner dominioNodoMaster
    - `/usr/local/hadoop/etc/hadoop/slaves` poner los n dominioNodoSlave.
    - `/usr/local/hadoop/etc/hadoop/hdfs-site.xml` borrar property con name `dfs.datanode.data.dir`

* En cada dataNode:

    - /etc/hostname poner nombre dominio. (tal vez ya se hizo)

### Para crear las carpetas del HDFS
#### En nameNode:
    sudo rm -rf /usr/local/hadoop/hadoop_data/
    sudo mkdir -p /usr/local/hadoop/hadoop_data/hdfs/namenode
    sudo chown -R usermaster:usermaster /usr/local/hadoop/   

#### En cada slaveNode:

    sudo rm -rf /usr/local/hadoop/hadoop_data/
    sudo mkdir -p /usr/local/hadoop/hadoop_data/hdfs/datanode
    sudo chown -R usermaster:usermaster /usr/local/hadoop/

Solo si el ip no es el que queremos, hay que cambiar ip: 
`vim /etc/network/interfaces` y reiniciar servicios: `service networking restart`.
En `/usr/local/hadoop/etc/hadoop/hdfs-site.xml` borrar property `dfs.namenode.name.dir`

#### En nameNode:

* Generar una key:
    `ssh-keygen -f ~/.ssh/id_rsa -t rsa -P ""`
(también se puede usar rda).
* Copiar la RSA al directorio SSH (parece que no es necesario para cubies clonadas, ya esta el archivo /home/usermaster/.ssh/authorized_keys)
* Copiar a todos los usuarios, master y slaves:
    * Conectar con ssh (ir cerrando conexiones -exit-) a cada maquina (incluidas master y slaves) 
    * Agregar hosts, en `/etc/hosts` agregar IPs y hostnames de datanodes (y namenode)
    * `hadoop namenode -format`
    * `start-dfs.sh` o `start-all.sh`
    
#### En slaveNodes que no hayan sido agregados al ejecutar start-dfs.sh
* Sólo para agregar nueva máquina una vez el servicio está andando, hay que partir servicio datanode y luego nodemanager:
    ```        
    hadoop-daemon.sh start datanode
    yarn-daemon.sh start nodemanager
    ```

### Algunos comandos útiles:

* hdfs dfsadmin -report
* `hdfs dfs -ls /directorio`: lista los archivos en `directorio` de HDFS.
* Copiar un archivo desde el sistema local al HDFS:
`hdfs dfs -copyFromLocal /archivo/en/equipo/local /ubicacion/en/hdfs`
* Imprimir un archivo en pantalla: 
`hdfs dfs -cat archivo`
* `hdfs dfsadmin -safemode leave`

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

* En spark-defaults.conf setear spark.master a "yarn" (sin las comillas).

### Instalar PySpark

Ejecutar `pip install pyspark`. Es una librería de python.
El comando pyspark abre una shell de python con la librería de pyspark ya importada. También se puede importar para hacer scripts (ejecutados con `spark-submit <nombre_script>.py`).

# Wordbatch


## Dependencias necesarias
* Cython
* Numpy
* Scikit-learn
* Scipy
* nltk
* Py4J
* py-lz4framed
* python-Levenshtein

# Ejecutar trabajos de MapReduce en Hadoop
hadoop jar $HADOOP_HOME/hadoop-streaming-2.9.2-sources.jar \
    -input myInputDirs \
    -output myOutputDir \
    -mapper /bin/cat \
    -reducer /bin/wc

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


## Conector de Spark con Cassandra
Hay que tener `git` y `sbt` instalado.

Luego se clona el repositorio: `git clone https://github.com/anguenot/pyspark-cassandra.git`

Luego se ejecuta lo siguiente (se va a demorar un rato):
```
cd pyspark-cassandra
sbt compile 
```