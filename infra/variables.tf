variable "resource_group_location" {
  type        = string
  default     = "westeurope"
  description = "Location of the resource group."
}

variable "resource_group_name" {
  type        = string
  default     = "cm_datavault"
  description = "Prefix of the resource group name that's combined with a random ID so name is unique in your Azure subscription."
}

variable "storage_account_name" {
  type       = string
  default    = "cmdatavaultstorage"
  description = "definion of name to storage account"
}

variable "storage_container_raw" {
  type        = string
  default     = "cm-landing"
  description = "definion of name to container that received events to eventhub topic."
}

variable "databricks_workspace" {
  type = string
  default = "cmdatabricks"
  description = "name of azure databricks workspace" 
}