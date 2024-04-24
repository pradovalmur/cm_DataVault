import os
import pandas as pd
import json
import typer
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
from dotenv import load_dotenv

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

# Definir o aplicativo Typer
app = typer.Typer()

@app.command()
def ingestion_investidor():
    # Defina suas credenciais e informações do Blob Storage da Azure
    azure_storage_connection_string = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
   

    # Conectar ao Blob Storage da Azure
    blob_service_client = BlobServiceClient.from_connection_string(azure_storage_connection_string)
    container_client = blob_service_client.get_container_client("cm-landing")


    # Ler o CSV e filtrar os dados com base na coluna especificada
    df = pd.read_csv("./data/Investidores_Tesouro_Direto.csv", sep= ';',encoding='latin1')

    df['Data de Adesao'] = pd.to_datetime(df['Data de Adesao'], dayfirst=True).dt.strftime('%Y-%m-%d')

    # Aplicar filtro para registros criados após 2015
    df_filtered = df[df['Data de Adesao'] > "2015-01-01"]

    # Agrupar o DataFrame por uma coluna específica (por exemplo, a coluna de datas)
    grouped_data = df_filtered .groupby('Data de Adesao')

    # Iterar sobre cada grupo de dados
    for group_name, group_df in grouped_data:
        # Converter o grupo em uma lista de dicionários
        data_list = group_df.to_dict(orient='records')
        
        # Converter a lista de dicionários em JSON
        json_data = json.dumps(data_list)
        
        # Nome do arquivo JSON no Blob Storage (incluindo o caminho da pasta desejada)
        folder_path = f"investidors/{group_name}/"  # Substitua 'pasta' pelo nome da sua pasta desejada
        blob_name = f"{folder_path}data_{group_name}.json"
        
        # Enviar o arquivo JSON para o Blob Storage
        blob_client = container_client.get_blob_client(blob_name)
        blob_client.upload_blob(json_data, overwrite=True)

    typer.echo("Dados de investidorenviados com sucesso para o Blob Storage!")

@app.command()
def ingestion_operation():
    # Defina suas credenciais e informações do Blob Storage da Azure
    azure_storage_connection_string = os.getenv("AZURE_STORAGE_CONNECTION_STRING")

    # Conectar ao Blob Storage da Azure
    blob_service_client = BlobServiceClient.from_connection_string(azure_storage_connection_string)
    container_client = blob_service_client.get_container_client("cm-landing")


    # Ler o CSV e filtrar os dados com base na coluna especificada
    df = pd.read_csv("./data/OperacoesTesouroDireto.csv", sep= ';',encoding='latin1')

    df['Data da Operacao'] = pd.to_datetime(df['Data da Operacao'], dayfirst=True).dt.strftime('%Y-%m-%d')

    # Aplicar filtro para registros criados após 2015
    df_filtered = df[df['Data da Operacao'] > "2020-01-01"]

    # Agrupar o DataFrame por uma coluna específica (por exemplo, a coluna de datas)
    grouped_data = df_filtered.groupby('Data da Operacao')

    # Iterar sobre cada grupo de dados
    for group_name, group_df in grouped_data:
        # Converter o grupo em uma lista de dicionários
        data_list = group_df.to_dict(orient='records')
        
        # Converter a lista de dicionários em JSON
        json_data = json.dumps(data_list)
        
        # Nome do arquivo JSON no Blob Storage (incluindo o caminho da pasta desejada)
        folder_path = f"transaction/{group_name}/"  # Substitua 'pasta' pelo nome da sua pasta desejada
        blob_name = f"{folder_path}data_{group_name}.json"
        
        # Enviar o arquivo JSON para o Blob Storage
        blob_client = container_client.get_blob_client(blob_name)
        blob_client.upload_blob(json_data, overwrite=True)

    typer.echo("Dados de transactions enviados com sucesso para o Blob Storage!")   

# Executar o aplicativo Typer
if __name__ == "__main__":
    app()
