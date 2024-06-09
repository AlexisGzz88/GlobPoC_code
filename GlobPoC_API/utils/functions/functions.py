# Databricks notebook source
def restore_backup_avro_delta(avro_input_path, delta_table_name):
    
    # Leer los archivos en formato Avro
    try:
        df = spark.read.format("avro").load(avro_input_path)
        print("dataframe en formato Avro creado correctamente.")
    except Exception as e:
        print(f"Error al intentar hacer la lectura de los archivos Avro: {e}")
        return
    
    # Muestra un ejemplo de los datos leidos
    df.printSchema()
    df.show()
    
    # Escribir el DataFrame en una tabla Delta
    try:
        df.write.format("delta").mode("overwrite").saveAsTable(delta_table_name)
        print(f"Datos guardados correctamente en la tabla Delta '{delta_table_name}'")
    except Exception as e:
        print(f"Error al escribir los datos en la tabla Delta: {e}")


# COMMAND ----------

def restore_backup_avro_parquet(avro_input_path, parquet_output_path):
    
    # Leer los archivos Avro
    try:
        df = spark.read.format("avro").load(avro_input_path)
        print("Archivos en formato Avro cargados correctamente.")
    except Exception as e:
        print(f"Error al intentar leer los archivos Avro: {e}")
        return
    
    # Mostrar el esquema y algunas filas del DataFrame para verificar la lectura
    df.printSchema()
    df.show()
    
    # Escribir el DataFrame en formato Parquet
    try:
        df.write.parquet(parquet_output_path)
        print(f"Datos guardados correctamente en formato Parquet en {parquet_output_path}")
    except Exception as e:
        print(f"Error al escribir los datos en formato Parquet: {e}")


# COMMAND ----------


