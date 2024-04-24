
# DataVault 2.0

In this project I intend to show a Data Vault 2.0 modeling using Azure Databricks, with the Medalion architecture (Broze, SIlver and Gold). 

In this project, as a data source, I am using data from the Brazilian Government's Open Data Portal, where I use transaction data from the national treasury. 

Read more [Dados.gov.br] (https://dados.gov.br/dados/busca?termo=tesouro)

## Main features

- Injestao de dados no azure blob storage, em formato json para universalidade de utilizacao, usando python.
- Delta Live Table configuration in databricks for automated data injection
- Creation of a framework for creating a dataplatform team
- Data modeling in the Datavault 2.0 model

![Table Schema](imagens/Stock_operations_datavault.png)


## How to use

- After cloning this repo, create a folder called *data* and place the downloaded CSVs in it. 
- create an *.env* file in the root of the project and place the connectionString of the storage blob in it (AZURE_STORAGE_CONNECTION_STRING= *xxxxxx*)
- Use pip install typer, to run the ingestion function
- with the command below, define the ingestion of transactions or investors:
    <p>python ingestions\ingestion.py  ingestion-investidor</p>
    <p>python ingestions\ingestion.py  ingestion-operation</p>


###Work in progress.

Read more [Linkedin](https://www.linkedin.com/in/valmur-prado-39b81522/).
Read more [Typer](https://typer.tiangolo.com/)
