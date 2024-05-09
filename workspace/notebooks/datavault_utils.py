import dlt
from pyspark.sql.functions import col
from pyspark.sql.functions import monotonically_increasing_id
from pyspark.sql.functions import to_date, date_format

@dlt.table(
    name="stg_investidors",
    comment=""
)       
def stg_investidors():

    df_investidors = spark.readStream.format("cloudFiles").option("cloudFiles.format", "json").option("cloudFiles.schemaLocation", "/mnt/data/investidors_schema").load("/mnt/data/stg-files/investidors/")
    
    new_column_names = [col(old_column).alias(old_column.replace(' ', '_').lower()) for old_column in df_investidors.columns]
    
    df_investidors = df_investidors.select(*new_column_names)

    return df_investidors

@dlt.table(
    name="stg_transactions",
    comment=""
)           
def stg_transaction():
    
    df_transactions = spark.readStream.format("cloudFiles").option("cloudFiles.format", "json").option("cloudFiles.schemaLocation", "/mnt/data/transactions_schema").load("/mnt/data/stg-files/transaction/")

    new_column_names = [col(old_column).alias(old_column.replace(' ', '_').lower()) for old_column in df_transactions.columns]
    
    df_transactions = df_transactions.select(*new_column_names)

    return df_transactions


@dlt.view
def stock():
    return spark.sql("""SELECT distinct
                            monotonically_increasing_id() as stock_id,
                            concat(t.tipo_titulo,"-", t.vencimento_do_titulo) as titulo,
                            t.tipo_titulo,
                            t.vencimento_do_titulo,
                            t.valor_do_titulo
                    FROM LIVE.stg_transactions as t
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
                    from LIVE.stg_transactions as t
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
    
@dlt.table(
    name="hub_stock",
    comment="This table is a Hub os stock options the hash key is a concatenate the name of titulo and expiration date" )
def hub_stock():    
    return spark.sql("""
                     select 
                         sha1(UPPER(TRIM(st.titulo))) as hk_titulo,
                         current_timestamp() as load_dts,
                         "stock" as source,
                         st.stock_id as stock_id
                     from live.stock as st
                     """)

@dlt.table(
  name="sat_stock",
  comment="")
def sat_stock():
    return spark.sql("""
                    select 
                        sha1(UPPER(TRIM(st.titulo))) as hk_titulo,
                        current_timestamp() as load_dts,
                        st.stock_id as stock_id,
                        st.vencimento_do_titulo as due_date,
                        st.valor_do_titulo as total_value,
                        st.tipo_titulo as type
                    from live.stock as st
                    """)

@dlt.table(
    name="link_operation",
    comment="")
def link_operation():
    return spark.sql("""
                     select 
                     sha1(concat(UPPER(TRIM(t.titulo)), UPPER(TRIM(t.codigo_do_investidor)), UPPER(TRIM(t.data_da_operacao)))) as hk_transaction,
                     current_timestamp() as load_dts,
                     sha1(UPPER(TRIM(t.titulo))) as hk_titulo,
                     sha1(UPPER(TRIM(t.codigo_do_investidor))) as hk_account
                     from live.transaction as t
                     """)

@dlt.table(
    name="sat_operation",
    comment="")
def sat_operation():
    return spark.sql("""
                     select 
                        sha1(concat(UPPER(TRIM(t.titulo)), UPPER(TRIM(t.codigo_do_investidor)), UPPER(TRIM(t.data_da_operacao)))) as hk_transaction,
                        current_timestamp() as load_dts,
                        t.quantidade as quantity,
                        t.valor_da_operacao as transaction_value,
                        case when  t.tipo_da_operacao = 'C' then 'Buy'
                             when t.tipo_da_operacao = 'V' then  'sell'
                        else 'other' end as type_operation,
                        case when t.canal_da_operacao = 'S' then 'Site'
                             when t.canal_da_operacao = 'H' then 'homebroker'
                        else 'other' end as channel
                     from live.transaction as t
                     """)
    
@dlt.table(
    name="hub_account",
    comment="")
def hub_account():
    return spark.sql("""
                    select 
                    sha1(UPPER(TRIM(acc.codigo_do_investidor))) as hk_account,
                    current_timestamp() as load_dts,
                    "account" as source,
                    acc.codigo_do_investidor as account_id
                    from live.account as acc
                    """)
    
@dlt.table(
    name="sat_account",
    comment="")
def dat_account():
    return spark.sql("""
                    select 
                        sha1(UPPER(TRIM(acc.codigo_do_investidor))) as hk_account,
                        current_timestamp() as load_dts,
                        acc.data_de_adesao as accession_date,
                        acc.situacao_da_conta as account_status,
                        acc.operou_12_meses as transactions_last_12_months
                    from live.account as acc   
                    """)
    
@dlt.table(
    name="link_account_investidor",
    comment="")
def link_account_investidor():
    return spark.sql("""
                     select 
                        sha1(UPPER(TRIM(acc.codigo_do_investidor))) as hk_account_investidor,
                        i.codigo_do_investidor as investidor_id,
                        acc.codigo_do_investidor as account_id
                     from live.account as acc
                     inner join live.investidor as i
                     """)
