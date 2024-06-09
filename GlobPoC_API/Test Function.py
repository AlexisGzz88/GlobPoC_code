# Databricks notebook source
# MAGIC %run "../GlobPoC_API/utils/functions/functions"

# COMMAND ----------

# Test ejecucución función
avro_input_path = '/mnt/portfolioagdl/archive/GlobPoc/tb_jobs/'
delta_table_name = 'cl_silver.tb_jobs'

restore_backup_avro_delta(avro_input_path, delta_table_name)
