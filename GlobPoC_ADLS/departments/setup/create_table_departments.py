# Databricks notebook source
spark.sql("drop table if exists cl_silver.tb_departments")
dbutils.fs.rm('dbfs:/mnt/portfolioagdl/process/GlobPoC/tb_departments/', recurse=True)

# COMMAND ----------

# MAGIC %sql
# MAGIC create table if not exists cl_silver.tb_departments(
# MAGIC id	int
# MAGIC ,department	string
# MAGIC )
# MAGIC using delta
# MAGIC location '/mnt/portfolioagdl/process/GlobPoC/tb_departments/'
# MAGIC comment 'Table that contains the information of departments'

# COMMAND ----------


