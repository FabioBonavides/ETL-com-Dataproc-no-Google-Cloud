ETL com Dataproc - Google Cloud
===================================
## Submeter um job no Dataproc serverless [Apache spark]
### Digitar o seguinte código para iniciar o job no Dataproc:
gcloud dataproc batches submit pyspark gs://code-repositorio/local.py --batch=batch-01 --deps-bucket=owshq-code-repositorio --region=us-east1
