# Databricks notebook source
import pandas as pd

from pyspark.sql.types import StructType, StructField, StringType, IntegerType
from pyspark.sql import DataFrame

# COMMAND ----------

# MAGIC %fs mounts

# COMMAND ----------

files = dbutils.fs.ls('dbfs:/mnt/portfolioagdl/inbound/GlobPoC/AlexisGzz88/ProjectAzure/main/GlobPoC/')
display(files)

# COMMAND ----------

#Se define el esquema de la tabla
schema = StructType([
    StructField("id", IntegerType(), True),
    StructField("job", StringType(), True)
])

# COMMAND ----------

# Ruta al directorio montado donde están los archivos CSV
file_path = "dbfs:/mnt/portfolioagdl/inbound/GlobPoC/AlexisGzz88/ProjectAzure/main/GlobPoC/jobs.csv"

# Leer archivos CSV en un DataFrame de Spark
df_spark = spark.read.csv(file_path, header=True, schema=schema)

# Mostrar esquema y número de filas leídas
df_spark.printSchema()
total_count = df_spark.count()
print(f"Total filas: {total_count}")

# COMMAND ----------

display(df_spark)

# COMMAND ----------


# Ruta de la tabla Delta existente
delta_table_path = "/mnt/portfolioagdl/process/GlobPoC/tb_jobs/"

# Truncar la tabla
spark.sql("TRUNCATE TABLE cl_silver.tb_jobs")

# Tamaño del lote
batch_size = 1000

# Función para insertar un lote en la tabla Delta existente
def insert_batch(batch_df):
    num_records = batch_df.count()
    batch_df.write.format("delta").mode("append").save(delta_table_path)
    print(f"Lote {batch_num}: {num_records} registros insertados con éxito")

# Dividir el DataFrame en lotes y realizar la inserción por lotes
total_records = df_spark.count()
num_batches = (total_records // batch_size) + (1 if total_records % batch_size != 0 else 0)

for batch_num in range(num_batches):
    start_index = batch_num * batch_size
    end_index = min(start_index + batch_size, total_records)
    
    # Seleccionar el lote de datos
    batch_df = df_spark.limit(end_index).subtract(df_spark.limit(start_index))
    
    # Insertar el lote en la tabla Delta
    insert_batch(batch_df)


# COMMAND ----------

# MAGIC %sql
# MAGIC select count(*)
# MAGIC from cl_silver.tb_jobs

# COMMAND ----------


