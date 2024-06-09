# Databricks notebook source
# MAGIC %fs mounts

# COMMAND ----------

files = dbutils.fs.ls('dbfs:/mnt/portfolioagdl/inbound/GlobPoC/AlexisGzz88/ProjectAzure/main/Champions_League/')
display(files)

# COMMAND ----------

from pyspark.sql import SparkSession

# Crear sesión de Spark
spark = SparkSession.builder.appName("BatchProcessing").getOrCreate()

# Ruta al directorio montado donde están los archivos CSV
file_path = "dbfs:/mnt/portfolioagdl/inbound/GlobPoC/AlexisGzz88/ProjectAzure/main/Champions_League/hired_employees.csv"

# Leer archivos CSV en un DataFrame de Spark
df = spark.read.csv(file_path, header=True, inferSchema=True)

# Mostrar esquema y número de filas leídas
df.printSchema()
df.count()


# COMMAND ----------

from pyspark.sql import SparkSession

# Crear sesión de Spark
spark = SparkSession.builder.appName("BatchProcessing").getOrCreate()

# Ruta al directorio montado donde están los archivos CSV
file_path = "dbfs:/mnt/portfolioagdl/inbound/GlobPoC/AlexisGzz88/ProjectAzure/main/Champions_League/hired_employees.csv"

# Leer archivos CSV en un DataFrame de Spark
df = spark.read.csv(file_path, header=True, inferSchema=True)

# Mostrar esquema y número de filas leídas
df.printSchema()
total_count = df.count()
print(f"Total filas: {total_count}")


# COMMAND ----------

def insert_to_db(batch_df):
    # Implementa la lógica para insertar en tu base de datos
    # Ejemplo con pyodbc para insertar en SQL Server
    import pyodbc

    conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=<server>;DATABASE=<database>;UID=<user>;PWD=<password>')
    cursor = conn.cursor()

    for row in batch_df.collect():
        cursor.execute("INSERT INTO <tabla> (col1, col2, col3) VALUES (?, ?, ?)", row.col1, row.col2, row.col3)

    conn.commit()
    cursor.close()
    conn.close()


# COMMAND ----------

batch_size = 1000
num_batches = (total_count + batch_size - 1) // batch_size  # Calcula el número de lotes necesarios

for i in range(num_batches):
    start = i * batch_size
    end = start + batch_size
    batch_df = df.limit(end).subtract(df.limit(start))  # Obtener el lote actual
    insert_to_db(batch_df)  # Inserta el lote en la base de datos

    print(f"Lote {i+1}/{num_batches} procesado e insertado.")


# COMMAND ----------


