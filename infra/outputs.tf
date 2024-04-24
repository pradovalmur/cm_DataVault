output "resource_group_name" {
  value = azurerm_resource_group.cm_resource_group.name
}

output "connection_string" {
  value = azurerm_storage_account.cm_storage_account.primary_connection_string
  sensitive = true
}