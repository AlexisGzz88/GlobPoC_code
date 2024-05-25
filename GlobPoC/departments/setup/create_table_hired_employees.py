# Databricks notebook source
spark.sql("drop table if exists cl_silver.tb_hired_employees")
dbutils.fs.rm('dbfs:/mnt/portfolioagdl/process/GlobPoC/tb_hired_employees/', recurse=True)

# COMMAND ----------

# MAGIC %sql
# MAGIC create table if not exists cl_silver.tb_hired_employees(
# MAGIC id	int
# MAGIC ,name	string
# MAGIC ,datetime	string
# MAGIC ,department_id	int
# MAGIC ,job_id	int
# MAGIC )
# MAGIC using delta
# MAGIC location '/mnt/portfolioagdl/process/GlobPoC/tb_hired_employees/'
# MAGIC comment 'Table that contains the information of hired employees'

# COMMAND ----------


