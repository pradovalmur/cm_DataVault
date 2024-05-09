import dlt
from pyspark.sql.functions import col
from pyspark.sql.functions import monotonically_increasing_id
from pyspark.sql.functions import to_date, date_format

mountPoint = "/mnt/data"
if not any(mount.mountPoint == mountPoint for mount in dbutils.fs.mounts()):
  try:
    dbutils.fs.mount(
        source = "wasbs://cmdatalake1251@cmstorageacc1251.blob.core.windows.net",
        mount_point = "/mnt/data",
        extra_configs = {"fs.azure.account.key.cmstorageacc1251.blob.core.windows.net":dbutils.secrets.get(scope = "lakehouse", key = "secret-sauce")}
    )
    print("mount succeeded!")
  except Exception as e:
    print("mount exception", e)        

@dlt.table        
def stg_investidors():
    try:
    
        df = spark.readStream.format("cloudFiles").option("cloudFiles.format", "json").load("/mnt/data/stg-files/investidors/")
        
        new_column_names = [col(old_column).alias(old_column.replace(' ', '_').lower()) for old_column in df.columns]
        
        df = df.select(*new_column_names)

        date_columns = ['data_de_adesao']

        for column in date_columns:
            df = df.withColumn(column, date_format(to_date(column, 'dd/MM/yyyy'), 'yyyy-MM-dd'))

        return df

    except Exception as e:
        print(f"Error {e}")

@dlt.table        
def stg_transaction():
    try:
    
        df = spark.readStream.format("cloudFiles").option("cloudFiles.format", "json").load("/mnt/data/stg-files/transaction/")

        new_column_names = [col(old_column).alias(old_column.replace(' ', '_').lower()) for old_column in df.columns]
        
        df = df.select(*new_column_names)

        date_columns = ['data_da_operacao', 'vencimento_do_titulo']

        for column in date_columns:
            df = df.withColumn(column, date_format(to_date(column, 'dd/MM/yyyy'), 'yyyy-MM-dd'))

        return df

    except Exception as e:
        print(f"Error {e}")


@dlt.view
def stock():
    return spark.sql("""SELECT distinct
                            monotonically_increasing_id() as stock_id,
                            concat(t.tipo_titulo,"-", t.vencimento_do_titulo),
                            t.tipo_titulo,
                            t.vencimento_do_titulo,
                            t.valor_do_titulo
                    FROM LIVE.stg_transaction as t
                      """)

@dlt.view
def transaction():
    return spark.sql("""
                    select 
                        monotonically_increasing_id() as transaction_id,
                        t.codigo_do_investidor,
                        t.data_da_operacao,
                        t.tipo_titulo,
                        t.vencimento_do_titulo,
                        concat(t.tipo_Titulo, '-', t.vencimento_do_titulo) as titulo,
                        t.quantidade ,
                        t.valor_da_operacao,
                        t.tipo_da_operacao,
                        t.canal_da_operacao
                    from LIVE.stg_transaction as t
                    """)

@dlt.view
def investidor():
    return spark.sql("""
                  select
                    i.codigo_do_investidor,
                    i.estado_civil,
                    i.genero,
                    i.profissao,
                    i.idade,
                    i.uf_do_investidor,
                    i.cidade_do_investidor,
                    i.pais_do_investidor
                  from LIVE.stg_investidors as i
                  """)
    

@dlt.view
def account():
    return spark.sql("""
                     select 
                        i.codigo_do_investidor,
                        i.data_de_adesao,
                        i.situacao_da_conta,
                        i.operou_12_meses 
                     from LIVE.stg_investidors as i
                     """)
