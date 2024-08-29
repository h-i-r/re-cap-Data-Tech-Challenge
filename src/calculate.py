from pyspark.sql import SparkSession
import pyspark.sql.functions as F
import string
from pyspark.sql.window import Window
import itertools

def calculate_revenue_churn(csv_filename):

    # Initiate Spark Session
    spark = SparkSession.builder.appName("Acme_Corp_Data").getOrCreate()
    sc = spark.sparkContext
    sc.setLogLevel('OFF')

    # Load File
    df = spark.read.csv(csv_filename, header=True, inferSchema=True)

    # Month
    df = df.withColumn('Month', F.trunc("invoice_date", "month"))

    # Contract ID (assign unique names to the contract_ids)
    letters = string.ascii_uppercase
    numbers = string.digits
    contract_codes = [''.join(p) for p in itertools.product(letters + numbers, repeat=2)]

    if len(contract_codes) < df.select('contract_id').distinct().count():
        raise ValueError("Not enough unique codes generated")

    unique_contracts = df.select('contract_id').distinct()

    window = Window.orderBy('contract_id')
    unique_contracts_with_codes = unique_contracts.withColumn(
        'contract_codes',
        F.lit(contract_codes).getItem(F.row_number().over(window) - 1))

    df = df.join(unique_contracts_with_codes, on='contract_id', how='left'
                 ).withColumnRenamed('contract_codes', 'Contract ID')

    # Net Revenue
    window = Window.partitionBy(['Month', 'Contract ID'])
    df = df.withColumn('Net Revenue', F.sum('original_billing_amount').over(window))

    # Churned Amount
    window = Window.partitionBy("Contract ID").orderBy("Month")
    df = df.withColumn("Previous Revenue", F.coalesce(F.lag("Net Revenue").over(window), F.lit(0)))
    df = df.withColumn("Churned Amount", F.when(
        (F.col("Previous Revenue") > 0) & (F.col("Net Revenue") <= 0),
        F.col("Previous Revenue")
    ).otherwise(F.lit(0)))

    df.select('Month', 'Contract ID', 'Net Revenue', 'Churned Amount').show(3)



