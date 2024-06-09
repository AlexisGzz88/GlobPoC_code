# Databricks notebook source
dbutils.secrets.listScopes()

# COMMAND ----------

dbutils.secrets.list(scope = 'GlobPoC-scope')

# COMMAND ----------

dbutils.secrets.get(scope = 'GlobPoC-scope', key='Github-Token')

# COMMAND ----------

import requests
import base64
import pandas as pd

from pyspark.sql.types import StructType, StructField, StringType, IntegerType
from pyspark.sql import DataFrame

# COMMAND ----------


# Obtener el token de GitHub desde Azure Key Vault a través de Databricks Secrets
GITHUB_TOKEN = dbutils.secrets.get(scope = 'GlobPoC-scope', key='Github-Token')

# Reemplaza con el propietario del repositorio y el nombre del repositorio
REPO_OWNER = "AlexisGzz88"
REPO_NAME = "GlobPoC"
# Reemplaza con la ruta del archivo dentro del repositorio
FILE_PATH = "departments - departments.csv"

# Construir la URL para acceder al archivo
url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/contents/{FILE_PATH}"

# Encabezados para la solicitud, incluyendo el token de acceso
headers = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3.raw"
}

# Hacer la solicitud GET para obtener el archivo
response = requests.get(url, headers=headers)

# Verificar si la solicitud fue exitosa
if response.status_code == 200:
    # Convertir el contenido del archivo CSV en un DataFrame de Pandas
    file_content = response.text
    # Usar pd.read_csv para leer el contenido del archivo CSV en un DataFrame de Pandas
    from io import StringIO
    data = StringIO(file_content)
    df = pd.read_csv(data)
    print(df.head())
else:
    print(f"Error al acceder al archivo: {response.status_code}, {response.json()}")


# COMMAND ----------

#Se define el esquema de la tabla
schema = StructType([
    StructField("id", IntegerType(), True),
    StructField("department", StringType(), True)
])

# COMMAND ----------

df_spark = spark.createDataFrame(df, schema=schema)

# COMMAND ----------

display(df_spark)

# COMMAND ----------


# Ruta de la tabla Delta existente
delta_table_path = "/mnt/portfolioagdl/process/GlobPoC/tb_departments/"

# Truncar la tabla
spark.sql("TRUNCATE TABLE cl_silver.tb_departments")

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
# MAGIC from cl_silver.tb_departments

# COMMAND ----------

backup_path = "/mnt/portfolioagdl/archive/GlobPoc/tb_departments"

# COMMAND ----------

df_spark.write.format("avro").save(backup_path)

# COMMAND ----------

files = dbutils.fs.ls('dbfs:/mnt/portfolioagdl/archive/GlobPoc/')
display(files)
