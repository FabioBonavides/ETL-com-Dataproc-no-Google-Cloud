
# import libraries
from pyspark.sql import SparkSession
from pyspark import SparkConf

# main 
if __name__ == '__main__':
 
    # Initialize Spark session
    spark = SparkSession.builder.appName("etl-yelp-py").getOrCreate()

    # Print configured Spark parameters
    print(SparkConf().getAll())

    # Set log level
    spark.sparkContext.setLogLevel("INFO")

    # Define input files
    get_device_file = "landing-zone/files/device/*.json"
    get_subscription_file = "landing-zone/files/subscription/*.json"

    # 1 = input
    # Read data
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
 
    # Print number of partitions
    print(df_device.rdd.getNumPartitions())
    print(df_subscription.rdd.getNumPartitions())

    # Print schema of dataframes
    df_device.printSchema()
    df_subscription.printSchema()

    # Show data
    df_device.show()
    df_subscription.show()

    # Count rows
    print(df_device.count())
    print(df_subscription.count())

    # SQL - Register dataframes into SQL engine
    df_device.createOrReplaceTempView("vw_device")
    df_subscription.createOrReplaceTempView("vw_subscription")

    # 2 = enrichment
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

    # Show enriched data
    df_join.show()

    # 3 = output
    df_join.write.format("parquet").mode("overwrite").save("curated-zone/ds_yelp")

    # Stop Spark session
    spark.stop()
