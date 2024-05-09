
resource "random_integer" "sufix" {
  min = 1000
  max = 2000
  seed  = "chameleon_mountain"
}

data "azurerm_client_config" "current" {}

data "external" "me" {
  program = ["az", "account", "show", "--query", "user"]
}

data external account_info {
  program  = ["az", "ad", "signed-in-user", "show", "--query", "{object_id:id}", "-o", "json",]
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

resource "azurerm_key_vault" "this" {
  name                       = "${var.prefix}keyvault${random_integer.sufix.result}"
  location                   = azurerm_resource_group.this.location
  resource_group_name        = azurerm_resource_group.this.name
  tenant_id                  = data.azurerm_client_config.current.tenant_id
  sku_name                   = var.sku_name
  soft_delete_retention_days = 7

  access_policy {
    tenant_id = data.azurerm_client_config.current.tenant_id
    object_id = data.external.account_info.result.object_id
    
    key_permissions = ["Get", "Create", "Delete", "List", "Restore", "Recover", "UnwrapKey", "WrapKey", "Purge", "Encrypt", "Decrypt", "Sign", "Verify", "Release", "Rotate", "GetRotationPolicy", "SetRotationPolicy"]
    secret_permissions = ["Backup", "Delete", "Get", "List", "Purge", "Recover", "Restore", "Set"]
    storage_permissions = ["Backup", "Delete", "DeleteSAS", "Get", "GetSAS", "List", "ListSAS", "Purge", "Recover", "RegenerateKey", "Restore", "Set", "SetSAS", "Update"]

  }

}

resource "azurerm_key_vault_secret" "this" {
  name         = "secret-sauce"
  value        = azurerm_storage_account.this.primary_access_key
  key_vault_id = azurerm_key_vault.this.id
}

resource "null_resource" "write_env_file" {
  provisioner "local-exec" {
    command = <<-EOT
      echo AZURE_STORAGE_CONNECTION_STRING=${azurerm_storage_account.this.primary_connection_string} > ../.env
    EOT
  }
}

