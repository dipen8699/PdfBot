terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~>2.57.0"
    }
  }
}


provider "azurerm" {
  features {}
}

resource "azurerm_resource_group" "pdfbot" {
  name     = "v1.0"
  location = "East US"
  tags = {
    environment = "dev"
    source      = "Terraform"
  }
}


resource "azurerm_app_service_plan" "appPlan" {
  name                = "pdfbott_appPlan"
  location            = azurerm_resource_group.pdfbot.location
  resource_group_name = azurerm_resource_group.pdfbot.name

  sku {
    tier = "Basic"
    size = "B1"
  }

  kind     = "Linux"
  reserved = true
}

resource "azurerm_app_service" "appService" {
  name                = "pdfbottService"
  location            = azurerm_resource_group.pdfbot.location
  resource_group_name = azurerm_resource_group.pdfbot.name
  app_service_plan_id = azurerm_app_service_plan.appPlan.id

  site_config {
    always_on     = false
    http2_enabled = true
  }
}
