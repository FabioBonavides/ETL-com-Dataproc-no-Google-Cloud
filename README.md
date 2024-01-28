ETL com Dataproc - Google Cloud
===================================
## Submeter um job no Dataproc serverless [Apache spark]
#### Digitar o seguinte código para iniciar o job no Dataproc:
gcloud dataproc batches submit pyspark gs://code-repositorio/local.py --batch=batch-01 --deps-bucket=owshq-code-repositorio --region=us-east1

O Dataproc irá consultar o script que está no arquivo local.py armazenado no bucket code-repositorio do GCP.

=======================================

Overview

This Python script is an example of an ETL (Extract, Transform, Load) process using Apache Spark with PySpark. The script reads data from two JSON files, performs some basic data exploration, enriches the data through a SQL join operation, and finally, saves the enriched data in the Parquet format. The ETL process involves the following steps:

--Initialization:-- Import necessary libraries, create a SparkSession, configure Spark parameters, and set the log level.

Input: Define file paths for input JSON files and read data into Spark DataFrames.

Data Exploration: Print information about the DataFrames, including the number of partitions, schema, sample data, and row count.

Data Registration: Register DataFrames as temporary SQL views.

Enrichment: Perform a SQL join operation on the registered views to create an enriched DataFrame.

Output: Save the enriched data to a Parquet file.

Cleanup: Stop the SparkSession.


