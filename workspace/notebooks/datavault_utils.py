# Databricks notebook source
import dlt


def check_and_create_mount(mount_point, source):

    

    try:
        # Check if the mount point already exists
        dbutils.fs.ls(mount_point)
        print(f"Mount point '{mount_point}' already exists.")
        return True
    except Exception as e:
        # Mount point doesn't exist, create it
        print(f"Mount point '{mount_point}' does not exist. Creating...")
        try:
            dbutils.fs.mount(source, mount_point, extra_configs=extra_configs)
            print(f"Mount point '{mount_point}' created successfully.")
            return True
        except Exception as e:
            print(f"Failed to create mount point '{mount_point}': {str(e)}")
            return False

storageAccountName = "charlesdatabricksadlsno"
blobContainerName = "aaa"
mountPoint = "/mnt/files/"
if not any(mount.mountPoint == mountPoint for mount in dbutils.fs.mounts()):
  try:
    dbutils.fs.mount(
      source = "wasbs://{}@{}.blob.core.windows.net".format(blobContainerName, storageAccountName),
      mount_point = mountPoint,
      extra_configs = {"fs.azure.account.key.cmstorageacc1251.blob.core.windows.net":dbutils.secrets.get(scope = "lakehouse", key = "secret-sauce")}
    )
    print("mount succeeded!")
  except Exception as e:
    print("mount exception", e)        

@dlt.table        
def stg_investidors():
    try:
    
        return (
            spark.readStream.format("cloudFiles")
            .option("cloudFiles.format", "json")
            .load("/mnt/files/investidors/")
        )

    except Exception as e:
        print(f"Error {e}")

@dlt.table        
def stg_transaction():
    try:
    
        return (
            spark.readStream.format("cloudFiles")
            .option("cloudFiles.format", "json")
            .load("/mnt/files/transaction/")
        )

    except Exception as e:
        print(f"Error {e}")


@dlt.view
def stock():
    None

@dlt.view
def transaction():
    None

@dlt.view
def investidor():
    None

@dlt.view
def account():
    None

