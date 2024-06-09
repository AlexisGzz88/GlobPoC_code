# Databricks notebook source
# Ejemplo en un notebook de Databricks para obtener la URL del repositorio Git
import subprocess

def get_git_remote_url():
    result = subprocess.run(["git", "remote", "-v"], capture_output=True, text=True)
    return result.stdout

print(get_git_remote_url())

# COMMAND ----------

print(get_git_remote_url())

# COMMAND ----------


