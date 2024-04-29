
resource "random_integer" "sufix" {
  min = 1000
  max = 2000
  seed  = "chameleon_mountain"
}

data "azurerm_client_config" "current" {
}

data "external" "me" {
  program = ["az", "account", "show", "--query", "user"]
}

locals {
  tags = {
    Environment = "Demo"
    Owner       = lookup(data.external.me.result, "name")
  }
}

resource "azurerm_resource_group" "this" {
  name     = "${var.prefix}-rg-${random_integer.sufix.result}"
  location = var.region
  tags     = local.tags
}

resource "azurerm_databricks_workspace" "this" {
  name                        = "${var.prefix}-workspace-${random_integer.sufix.result}"
  resource_group_name         = azurerm_resource_group.this.name
  location                    = azurerm_resource_group.this.location
  sku                         = "premium"
  tags                        = local.tags
}

resource "azurerm_storage_account" "this" {
  name                     = "${var.prefix}storageacc${random_integer.sufix.result}"
  resource_group_name      = azurerm_resource_group.this.name
  location                 = azurerm_resource_group.this.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
  account_kind             = "StorageV2"
  is_hns_enabled           = "true"
  tags                     = local.tags
}

resource "azurerm_storage_data_lake_gen2_filesystem" "this" {
  name               = "${var.prefix}datalake${random_integer.sufix.result}"
  storage_account_id = azurerm_storage_account.this.id
}

resource "azurerm_storage_data_lake_gen2_path" "this" {
  path               = "stg-files"
  filesystem_name    = azurerm_storage_data_lake_gen2_filesystem.this.name
  storage_account_id = azurerm_storage_account.this.id
  resource           = "directory"
}

resource "null_resource" "write_env_file" {
  provisioner "local-exec" {
    command = <<-EOT
      echo AZURE_STORAGE_CONNECTION_STRING=${azurerm_storage_account.this.primary_connection_string} > ../.env
    EOT
  }
}