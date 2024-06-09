# Databricks notebook source
spark.sql("drop table if exists cl_silver.tb_jobs")
dbutils.fs.rm('dbfs:/mnt/portfolioagdl/process/GlobPoC/tb_jobs/', recurse=True)

# COMMAND ----------

# MAGIC %sql
# MAGIC create table if not exists cl_silver.tb_jobs(
# MAGIC id	int
# MAGIC ,job	string
# MAGIC )
# MAGIC using delta
# MAGIC location '/mnt/portfolioagdl/process/GlobPoC/tb_jobs/'
# MAGIC comment 'Table that contains the information of hired jobs'

# COMMAND ----------


