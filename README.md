
# DataVault 2.0

In this project I intend to show a Data Vault 2.0 modeling using Azure Databricks, with the Medalion architecture (Broze, SIlver and Gold). 

In this project, as a data source, I am using data from the Brazilian Government's Open Data Portal, where I use transaction data from the national treasury. 

Read more [Dados.gov.br](https://dados.gov.br/dados/busca?termo=tesouro)

## Main feature

- Terraform Code to deploy resources  on Azure.

![resources](images/scalidraw_architecture)

- Injection of data into azure blob storage, in json format for universal use, using python.
- Delta Live Table configuration in databricks for automated data injection
- Creation of a framework for creating a dataplatform team
- Data modeling in the Datavault 2.0 model

![Table Schema](imagens/Stock_operations_datavault.png)


## How to use

- First of all, if you want to use terraform, you need to configure azure cli locally, with the connection.
- Execute the terraforming plan, to check which features will be created.
- Then terrafomr apply to actually create the resources. 
- After cloning this repo, create a folder called *data* and place the downloaded CSVs in it. 
- create an *.env* file in the root of the project and place the connectionString of the storage blob in it (AZURE_STORAGE_CONNECTION_STRING= *xxxxxx*)
- Use pip install typer, to run the ingestion function
- with the command below, define the ingestion of transactions or investors:
    <p>python ingestions\ingestion.py  ingestion-investidor</p>
    <p>python ingestions\ingestion.py  ingestion-operation</p>


###Work in progress.

Read more [Linkedin](https://www.linkedin.com/in/valmur-prado-39b81522/)<br>

Read more [Typer](https://typer.tiangolo.com/)

