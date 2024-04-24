terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~>3.0"
    }
    random = {
      source  = "hashicorp/random"
      version = "~>3.0"
    }
  }
}

provider "azurerm" {
  features {}

  client_id       = jsondecode(file("${path.module}/secrets.json"))["client_id"]
  client_secret   = jsondecode(file("${path.module}/secrets.json"))["client_secret"]
  subscription_id = jsondecode(file("${path.module}/secrets.json"))["subscription_id"]
  tenant_id       = jsondecode(file("${path.module}/secrets.json"))["tenant_id"]
}