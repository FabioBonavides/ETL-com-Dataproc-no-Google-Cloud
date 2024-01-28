ETL com Dataproc - Google Cloud
===================================
## Submeter um job no Dataproc serverless [Apache spark]
### Digitar o seguinte código para iniciar o job no Dataproc:
```
gcloud dataproc batches submit pyspark gs://code-repositorio/local.py --batch=batch-01 --deps-bucket=code-repositorio --region=us-east1
```
O Dataproc irá consultar o script que está no arquivo local.py armazenado no bucket code-repositorio do GCP.

Overview
--------------------------
O presente script é um exemplo de processo ETL (Extract, Transform, Load) usando Apache Spark com PySpark. O script lê dados de dois arquivos JSON, realiza algumas explorações básicas de dados, enriquece os dados por meio de uma operação de junção SQL e, por fim, salva os dados enriquecidos no formato Parquet. O processo ETL envolve as seguintes etapas:

This Python script is an example of an ETL (Extract, Transform, Load) process using Apache Spark with PySpark. The script reads data from two JSON files, performs some basic data exploration, enriches the data through a SQL join operation, and finally, saves the enriched data in the Parquet format. The ETL process involves the following steps:

**Initialization:** Import necessary libraries, create a SparkSession, configure Spark parameters, and set the log level.

**Input:** Define file paths for input JSON files and read data into Spark DataFrames.

**Data Exploration:** Print information about the DataFrames, including the number of partitions, schema, sample data, and row count.

**Data Registration:** Register DataFrames as temporary SQL views.

**Enrichment:** Perform a SQL join operation on the registered views to create an enriched DataFrame.

**Output:** Save the enriched data to a Parquet file.

**Cleanup:** Stop the SparkSession.

Code Breakdown
---------------------------
## 1. Importar bibliotecas
```
from pyspark.sql import SparkSession
from pyspark import SparkConf
```
Ocorre a importação das bibliotecas necessárias, incluindo SparkSession e Sparkconf do PySpark.

## 2. Inicializar a SparkSession e Configurar os parâmetros.
```
spark = SparkSession \
        .builder \
        .appName("etl-yelp-py") \
        .getOrCreate()

print(SparkConf().getAll())
spark.sparkContext.setLogLevel("INFO")
```
A SparkSession é criada com a aplicação de nome "etl-yelp-py", e os parâmetros das condigurações são impressos. Além disso, o log level é "setado" como INFO.

## 3. Input - Read Data
```
get_device_file = "landing-zone/files/device/*.json"
get_subscription_file = "landing-zone/files/subscription/*.json"

df_device = spark.read \
    .format("json") \
    .option("inferSchema", "true") \
    .option("header", "true") \
    .json(get_device_file)

df_subscription = spark.read \
    .format("json") \
    .option("inferSchema", "true") \
    .option("header", "true") \
    .json(get_subscription_file)
```
Nessa parte, são definidos os caminhos para o acesso e a leitura dos arquivos em JSON (df_device e df_subscription).

## 4. Data Exploration
```
print(df_device.rdd.getNumPartitions())
print(df_subscription.rdd.getNumPartitions())

df_device.printSchema()
df_subscription.printSchema()

df_device.show()
df_subscription.show()

print(df_device.count())
print(df_subscription.count())
```
Imprimir informações sobre os DataFrames, incluindo o número de partições, esquema, sample data e contagem de número de linhas.

## 5. Data Registration
```
df_device.createOrReplaceTempView("vw_device")
df_subscription.createOrReplaceTempView("vw_subscription")
```
Ragistrar os DataFrames como um SQL views temporário.

## 6. Enrichment - SQL Join Operation (operação de Join)
```
df_join = spark.sql("""
    SELECT device.user_id,
            device.model, 
            device.platform, 
            device.manufacturer,
            subscription.payment_method,
            subscription.plan,
            subscription.subscription_term
    FROM vw_device AS device
    INNER JOIN vw_subscription AS subscription
    ON device.user_id = subscription.user_id
""")
```
Realiza um SQL join para unir os DataFrames e criar um novo DataFrame (df_join).

## 7. Output - Write Enriched Data to Parquet (gravar o novo DataFrame em formato Parquet) 
```
df_join.write.format("parquet").mode("overwrite").save("curated-zone/ds_yelp")
```
O dado enriquecido é salvo no formato Parquet no diretório especificado, ocorrendo o sobrescrição dos dados.

## 8. Stop SparkSession
```
spark.stop()
```
SparkSession é encerrada.

## Conclusão:
Este script PySpark apresenta um pipeline ETL básico para dados do Yelp, demonstrando a facilidade e o poder do PySpark no tratamento de transformações de dados em grande escala.

This PySpark script showcases a basic ETL pipeline for Yelp data, demonstrating the ease and power of PySpark in handling large-scale data transformations. 
