# Terraform - Deploy to multiple clouds
# terraform init
# terraform plan
# terraform apply

terraform {
  required_version = ">= 1.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.0"
    }
  }
  
  # Store state in S3 for team collaboration
  backend "s3" {
    bucket         = "softkillbot-terraform-state"
    key            = "prod/terraform.tfstate"
    region         = "us-east-1"
    encrypt        = true
    dynamodb_table = "terraform-locks"
  }
}

# AWS Provider
provider "aws" {
  region = var.aws_region
  default_tags {
    tags = {
      Project = "Softkillbot"
      ManagedBy = "Terraform"
      Environment = var.environment
    }
  }
}

# Google Cloud Provider
provider "google" {
  project = var.gcp_project
  region  = var.gcp_region
}

# Azure Provider
provider "azurerm" {
  features {}
  subscription_id = var.azure_subscription_id
}

# Variables
variable "environment" {
  description = "Environment (dev, staging, prod)"
  type        = string
  default     = "prod"
}

variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "us-east-1"
}

variable "gcp_project" {
  description = "GCP project ID"
  type        = string
}

variable "gcp_region" {
  description = "GCP region"
  type        = string
  default     = "us-central1"
}

variable "azure_subscription_id" {
  description = "Azure subscription ID"
  type        = string
}

variable "docker_image" {
  description = "Docker image URI"
  type        = string
}

variable "telegram_token" {
  description = "Telegram bot token"
  type        = string
  sensitive   = true
}

variable "sophia_token" {
  description = "Sophia API token"
  type        = string
  sensitive   = true
}

# Outputs
output "aws_service_url" {
  value = module.aws.service_url
  description = "AWS ECS service URL"
}

output "gcp_service_url" {
  value = module.gcp.service_url
  description = "GCP Cloud Run service URL"
}

output "azure_service_url" {
  value = module.azure.service_url
  description = "Azure Container Instances URL"
}

output "all_service_urls" {
  value = {
    aws   = module.aws.service_url
    gcp   = module.gcp.service_url
    azure = module.azure.service_url
  }
  description = "All deployed service URLs"
}

# AWS Module
module "aws" {
  source = "./modules/aws"
  
  environment      = var.environment
  region          = var.aws_region
  docker_image    = var.docker_image
  telegram_token  = var.telegram_token
  sophia_token    = var.sophia_token
}

# GCP Module
module "gcp" {
  source = "./modules/gcp"
  
  environment      = var.environment
  project         = var.gcp_project
  region          = var.gcp_region
  docker_image    = var.docker_image
  telegram_token  = var.telegram_token
  sophia_token    = var.sophia_token
}

# Azure Module
module "azure" {
  source = "./modules/azure"
  
  environment      = var.environment
  subscription_id = var.azure_subscription_id
  docker_image    = var.docker_image
  telegram_token  = var.telegram_token
  sophia_token    = var.sophia_token
}
