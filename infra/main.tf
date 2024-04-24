

resource "azurerm_resource_group" "cm_resource_group" {
  location = var.resource_group_location
  name     = var.resource_group_name
}


resource "azurerm_storage_account" "cm_storage_account" {
  name = var.storage_account_name
  resource_group_name = azurerm_resource_group.cm_resource_group.name
  location = azurerm_resource_group.cm_resource_group.location
  account_tier = "Standard"
  account_replication_type = "LRS" 

  tags = {
    environment = "dev"
  }

}

resource "azurerm_storage_container" "cm_storage_container" {
  name = var.storage_container_raw
  storage_account_name = azurerm_storage_account.cm_storage_account.name
  container_access_type = "private"
}

resource "azurerm_databricks_workspace" "cm_databricks" {
  name                = var.databricks_workspace
  resource_group_name = azurerm_resource_group.cm_resource_group.name
  location            = azurerm_resource_group.cm_resource_group.location
  sku                 = "standard"

  tags = {
    environment = "dev"
  }
}

resource "null_resource" "write_env_file" {
  provisioner "local-exec" {
    command = <<-EOT
      echo "AZURE_STORAGE_CONNECTION_STRING=${azurerm_storage_account.cm_storage_account.primary_connection_string}" > ./.env
    EOT
  }
}