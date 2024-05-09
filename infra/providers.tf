terraform {
  required_providers {
    azurerm = {
      source = "hashicorp/azurerm"
      version = "3.102.0"
    }
    random = "~> 2.2"
  }
}

provider "azurerm" {
  features {}
  
}
