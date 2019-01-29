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
```
    &lt;configuration>
        &lt;property>
            &lt;name>fs.defaultFS&lt;/name>
            &lt;value>hdfs://masterNodo:9000&lt;/value>
        &lt;/property>
    &lt;/configuration>
```
* `/usr/local/hadoop/etc/hadoop/hdfs-site.xml`:
```
    &lt;configuration>
        &lt;property>
            &lt;name>dfs.replication&lt;/name>
            &lt;value>3&lt;/value>
        &lt;/property>
        &lt;property>
            &lt;name>dfs.namenode.name.dir&lt;/name>
            &lt;value>/usr/local/hadoop/hadoop_data/hdfs/namenode&lt;/value>
        &lt;/property>
        &lt;property>
            &lt;name>dfs.datanode.data.dir&lt;/name>
            &lt;value>/usr/local/hadoop/hadoop_data/hdfs/datanode&lt;/value>
        &lt;/property>
    &lt;/configuration>
```
* `/usr/local/hadoop/etc/hadoop/yarn-site.xml`:
```
    &lt;configuration>
        &lt;property>
            &lt;name>yarn.nodemanager.aux-services&lt;/name>
            &lt;value>mapreduce_shuffle&lt;/value>
        &lt;/property>
        &lt;property>
            &lt;name>yarn.nodemanager.aux-services.mapreduce.shuffle.class&lt;/name>
            &lt;value>org.apache.hadoop.mapred.ShuffleHandler&lt;/value>
        &lt;/property>
        &lt;property>
            &lt;name>yarn.resourcemanager.resource-tracker.address&lt;/name>
            &lt;value>dominioNodoMaster:8025&lt;/value>      
        &lt;/property>
        &lt;property>
            &lt;name>yarn.resourcemanager.scheduler.address&lt;/name>
            &lt;value>dominioNodoMaster:8030&lt;/value>      
        &lt;/property>
        &lt;property>
            &lt;name>yarn.resourcemanager.address&lt;/name>
            &lt;value>dominioNodoMaster:8050&lt;/value>       
        &lt;/property>
    &lt;/configuration>
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

### Integrar Spark con YARN

* En spark-defaults.conf setear spark.master a "yarn" (sin las comillas).

### Instalar PySpark

Ejecutar `pip install pyspark`. Es una librería de python.
El comando pyspark abre una shell de python con la librería de pyspark ya importada.

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